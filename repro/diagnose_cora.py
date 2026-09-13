"""诊断 Cora 复现精度偏低：合成图结构、标签、多数类基线。相对路径，从工作区根运行。"""
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "gctd" / "src"))

from utils.args import get_args
from utils.utils import set_seed, load_configs, get_loaders, get_gnn
from utils.data_handling import load_data
from models.gctd import GCTD
from utils.losses import tensor_squared


def main():
    import wandb
    wandb.init(mode="disabled")
    set_seed(42)
    sys.argv = ["diagnose", "--dataset", "cora", "--reduction_rate", "0.013", "--no_wandb", "--num_workers", "0"]
    args = load_configs(get_args())
    args.data_dir = "data"
    # get_args 已读 sys.argv；再补齐
    data, multi_view, vals = load_data(args)
    y_full = data.y_full.cpu()
    print("=== 原图 Cora ===")
    print("N", args.N, "y", Counter(y_full.tolist()))
    print("majority", y_full.bincount().max().item() / len(y_full))
    test_y = y_full[data.test_idx]
    print("test majority", test_y.bincount().max().item() / len(test_y), "n_test", len(test_y))
    train_y = y_full[data.train_idx]
    print("train n", int(data.train_idx.sum()), "classes", Counter(train_y.tolist()))

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    rec_loaders = get_loaders(multi_view, vals, args)
    gctd = GCTD(data, device, args).to(device)
    gctd.train()
    opt = torch.optim.Adam(gctd.parameters(), lr=args.lr_rec, weight_decay=args.wd)
    loss_fn = torch.nn.MSELoss()
    norm = tensor_squared(vals)
    best, stop, prev = 1e10, 0, 1e10
    best_state = None
    for epoch in range(1, 201):
        err = 0.0
        for si, loader in enumerate(rec_loaders):
            for batch in loader:
                batch = [batch[0].to(device), batch[1].to(device), batch[2].to(device)]
                rec = gctd.forward(si, batch)
                rec_err = loss_fn(rec, batch[2]) / norm
                err = err + rec_err
                opt.zero_grad()
                rec_err.backward()
                opt.step()
        if err < best:
            best, stop, best_state = err, 0, {k: v.detach().cpu().clone() for k, v in gctd.state_dict().items()}
        else:
            stop += 1
        if stop == 10 or abs(prev - float(err)) < args.atol:
            print(f"condense stop epoch={epoch} err={float(err):.6e}")
            break
        prev = float(err)
    gctd.load_state_dict(best_state)
    gctd.to(device)
    reduced = gctd.to_data_obj()

    print("=== 合成图 ===")
    n = reduced.num_nodes
    e = reduced.edge_index.size(1)
    print("nodes", n, "N_prime", int(args.N * args.reduction_rate), "edges", e, "density", e / (n * n))
    print("self-loops", int((reduced.edge_index[0] == reduced.edge_index[1]).sum()))
    print("y", Counter(reduced.y.tolist()))
    print("train/val/test", int(reduced.train_mask.sum()), int(reduced.val_mask.sum()), int(reduced.test_mask.sum()))
    ty = reduced.y[reduced.train_mask]
    print("train y", Counter(ty.tolist()))
    # 同 (class) 特征是否完全相同
    x = reduced.x
    uniq = len(torch.unique(x, dim=0))
    print("unique feature rows", uniq, "/", n)
    if int(reduced.train_mask.sum()) > 0:
        xt = x[reduced.train_mask]
        print("unique train feature rows", len(torch.unique(xt, dim=0)), "/", int(reduced.train_mask.sum()))
        # 无图线性分类：合成 train → 原 test
        clf = LogisticRegression(max_iter=1000)
        clf.fit(xt.numpy(), ty.numpy())
        pred_tr = clf.predict(xt.numpy())
        print("logreg fit synthetic train", accuracy_score(ty.numpy(), pred_tr))
        pred_te = clf.predict(data.feat_full[data.test_idx].numpy())
        print("logreg synthetic-train → original-test", accuracy_score(test_y.numpy(), pred_te))

    # 2-hop 邻居是否几乎全图
    from torch_geometric.utils import to_dense_adj
    adj = to_dense_adj(reduced.edge_index, max_num_nodes=n)[0]
    deg = adj.sum(1)
    print("degree min/mean/max", float(deg.min()), float(deg.mean()), float(deg.max()))


if __name__ == "__main__":
    import os
    os.chdir(ROOT / "gctd")
    main()
