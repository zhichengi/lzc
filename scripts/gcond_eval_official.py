#!/usr/bin/env python
"""R-GCTD-3：用 GCTD 的评测链路跑 GCond 官方压缩图（外部对照）。

目的不是复现 GCond，而是回答一个问题：**「合成图训 GCN、原图 val 选模、原图 test 评测」
这条评测链路本身，在一个已知方法（GCond）的官方压缩图上能否打出公认数字？**

- 若 GCond 官方图在这里能得到接近论文 Table 2 的数字（Cora 1.3% = 79.8 ± 1.3），
  说明 GCTD 与论文的差距在**压缩/学习侧**，而不是评测侧。
- 若同样打不出来，说明问题在评测/环境侧。

数据来源：GCond 官方仓库自带的 `saved_ours/adj_cora_<r>_<seed>.pt` 与
`feat_cora_<r>_<seed>.pt`，即论文 Table 2 所用的原始产物。
`r=0.25`（Cora，140 个训练标签 → 35 个超点）对应论文的 1.3% 压缩比。

评测链路完全复用 GCTD：
  * GCN：`repro/gctd/src/models/other_arcs.py:MyGCN`（2 层，hidden 256）
  * 原图 val/test：`NeighborLoader(original_dataset, num_neighbors=[-1,-1])`
  * 合成图 train：`NeighborLoader(synth_data, ..., input_nodes=train_mask)`
  * Adam(lr=1e-3, wd=1e-3)，600 epoch
  * 选模：原图 val（`--select val_loss` 与 GCTD 一致；`val_acc` 与 GCond 一致）

用法（在仓库根）：
    bash repro/run_gcond_eval.sh                # 默认 cora r=0.25 seeds 0-4
"""

import argparse
import csv
import os
import sys
from copy import deepcopy
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.loader import NeighborLoader

REPO = Path(__file__).resolve().parent.parent
GCTD_SRC = REPO / "repro" / "gctd" / "src"
sys.path.insert(0, str(GCTD_SRC))

from models.other_arcs import MyGCN  # noqa: E402
from utils.data_handling import prepare_data  # noqa: E402


def synth_labels_from_train(y_train, n_synth):
    """复刻 GCond 的 generate_labels_syn（按类频次比例分配，最后一类补齐）。"""
    from collections import Counter

    counter = Counter(y_train.tolist())
    n = len(y_train)
    ratio = n_synth / n
    total = n_synth
    sorted_counter = sorted(counter.items(), key=lambda kv: kv[1])
    labels, assigned = [], 0
    for ix, (c, num) in enumerate(sorted_counter):
        if ix == len(sorted_counter) - 1:
            k = total - assigned
        else:
            k = max(int(num * ratio), 1)
        labels += [c] * k
        assigned += k
    return labels


def build_synth_data(adj, feat, labels, epsilon, device):
    """把 GCond 的稠密 adj 按 epsilon 截断成边表，构造 PyG Data。"""
    adj = adj.clone()
    if epsilon > 0:
        adj[adj < epsilon] = 0
    idx = adj.nonzero(as_tuple=False)
    edge_index = idx.t().contiguous()
    edge_weight = adj[idx[:, 0], idx[:, 1]]
    n = feat.shape[0]

    from torch_geometric.data import Data

    d = Data()
    d.x = feat.float()
    d.y = torch.tensor(labels, dtype=torch.long)
    d.edge_index = edge_index
    d.edge_weight = edge_weight.float()
    d.train_mask = torch.ones(n, dtype=torch.bool)
    return d, int(edge_index.shape[1]), n


def evaluate(orig, synth, args, device):
    train_loader = NeighborLoader(
        synth, num_neighbors=[-1] * 2, batch_size=synth.num_nodes,
        input_nodes=synth.train_mask,
    )
    val_loader = NeighborLoader(
        orig, num_neighbors=[-1] * 2,
        batch_size=int(orig.val_mask.sum()), input_nodes=orig.val_mask,
    )
    test_loader = NeighborLoader(
        orig, num_neighbors=[-1] * 2,
        batch_size=int(orig.test_mask.sum()), input_nodes=orig.test_mask,
    )

    x_dim = synth.x.shape[1]
    out_dim = int(orig.y.max()) + 1
    gnn = MyGCN(x_dim, args.hidden, out_dim).to(device)
    opt = torch.optim.Adam(gnn.parameters(), lr=args.lr, weight_decay=args.wd)

    def run_eval(loader):
        gnn.eval()
        y_pred, y_true, total, seen = [], [], 0.0, 0
        for batch in loader:
            batch = batch.to(device)
            bs = batch.batch_size
            out = gnn(batch.x, batch.edge_index, batch.edge_weight, args)[:bs]
            loss = F.cross_entropy(out, batch.y[:bs])
            y_pred.extend(out.argmax(-1).cpu().numpy())
            y_true.extend(batch.y[:bs].cpu().numpy())
            total += float(loss) * bs
            seen += bs
        from sklearn.metrics import accuracy_score

        return total / max(seen, 1), accuracy_score(y_true, y_pred), out

    best_state, best_val_loss, best_val_acc = deepcopy(gnn.state_dict()), 1e9, 0.0
    for _ in range(args.epochs):
        gnn.train()
        opt.zero_grad()
        for batch in train_loader:
            batch = batch.to(device)
            bs = batch.batch_size
            out = gnn(batch.x, batch.edge_index, batch.edge_weight, args)[:bs]
            loss = F.cross_entropy(out, batch.y[:bs])
            loss.backward()
        opt.step()

        val_loss, val_acc, _ = run_eval(val_loader)
        better = (val_loss < best_val_loss) if args.select == "val_loss" \
            else (val_acc > best_val_acc)
        if better:
            best_val_loss, best_val_acc = val_loss, val_acc
            best_state = deepcopy(gnn.state_dict())

    gnn.load_state_dict(best_state)
    _, test_acc, _ = run_eval(test_loader)
    return test_acc * 100, best_val_acc * 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gc-dir", default=str(REPO / "repro" / "gcond" / "saved_ours"))
    ap.add_argument("--data-dir", default=str(REPO / "repro" / "gctd" / "data"))
    ap.add_argument("--dataset", default="cora")
    ap.add_argument("--rate", default="0.25", help="GCond 侧的 r（cora 0.25 = 论文 1.3%）")
    ap.add_argument("--paper-value", default="79.8", help="论文 Table 2 对应数字，仅用于打印")
    ap.add_argument("--seeds", default="0 1 2 3 4")
    ap.add_argument("--epsilon", type=float, default=0.05,
                    help="GCond 的 to_edge_index 截断阈值；cora/citeseer 用 0.05")
    ap.add_argument("--hidden", type=int, default=256)
    ap.add_argument("--epochs", type=int, default=600)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--wd", type=float, default=1e-3)
    ap.add_argument("--select", default="val_loss", choices=["val_loss", "val_acc"])
    ap.add_argument("--weighted", type=int, default=1)
    ap.add_argument("--dropout", type=float, default=0.0)
    ap.add_argument("--gpu-id", type=int, default=0)
    ap.add_argument("--csv", default="")
    args = ap.parse_args()

    device = torch.device("cpu")
    if torch.cuda.is_available():
        device = torch.device(f"cuda:{args.gpu_id}")

    print(f"[gcond-eval] gcond={args.gc_dir} data={args.data_dir} "
          f"dataset={args.dataset} r={args.rate} select={args.select} eps={args.epsilon}")

    handler = prepare_data(args.data_dir, args.dataset)
    orig = handler.dataset
    y_train = orig.y[orig.train_mask]
    print(f"[gcond-eval] original: N={orig.num_nodes} E={orig.num_edges} "
          f"train/val/test={int(orig.train_mask.sum())}/"
          f"{int(orig.val_mask.sum())}/{int(orig.test_mask.sum())}")

    rows = []
    for s in args.seeds.split():
        adj_p = os.path.join(args.gc_dir, f"adj_{args.dataset}_{args.rate}_{s}.pt")
        feat_p = os.path.join(args.gc_dir, f"feat_{args.dataset}_{args.rate}_{s}.pt")
        if not (os.path.exists(adj_p) and os.path.exists(feat_p)):
            print(f"[gcond-eval] seed {s}: missing {adj_p} / {feat_p}, skip")
            continue
        adj = torch.load(adj_p, map_location="cpu")
        feat = torch.load(feat_p, map_location="cpu")
        labels = synth_labels_from_train(y_train, feat.shape[0])
        synth, n_edges, n_nodes = build_synth_data(adj, feat, labels, args.epsilon, device)
        density = n_edges / (n_nodes * n_nodes)

        test_acc, val_acc = evaluate(orig, synth, args, device)
        print(f"[gcond-eval] seed {s}: n_synth={n_nodes} edges={n_edges} "
              f"density={density:.4f} best_val_acc={val_acc:.2f} test_acc={test_acc:.2f}")
        rows.append({
            "dataset": args.dataset, "gc_rate": args.rate, "seed": s,
            "n_synth": n_nodes, "edges": n_edges, "density": f"{density:.4f}",
            "epsilon": args.epsilon, "select": args.select,
            "best_val_acc": f"{val_acc:.2f}", "test_acc": f"{test_acc:.2f}",
        })

    if not rows:
        print("[gcond-eval] no runs", file=sys.stderr)
        return 1

    accs = [float(r["test_acc"]) for r in rows]
    mean = float(np.mean(accs))
    std = float(np.std(accs, ddof=1)) if len(accs) > 1 else 0.0
    print(f"\n[gcond-eval] GCond official condensed graph on {args.dataset} "
          f"r={args.rate}, evaluated by GCTD harness")
    print(f"[gcond-eval] n={len(accs)} mean={mean:.2f} std={std:.2f} "
          f"paper={args.paper_value}")

    if args.csv:
        Path(args.csv).parent.mkdir(parents=True, exist_ok=True)
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"[gcond-eval] wrote {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
