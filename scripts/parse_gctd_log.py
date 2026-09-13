#!/usr/bin/env python
"""解析 GCTD 单次运行日志，给出压缩图统计与 GCN 评测精度。

日志由 `repro/run_gctd.sh` 生成（`train.py` 的 stdout 同时落盘）。关键行：

    Namespace(..., dataset='pubmed', reduction_rate=0.0008, ..., seed=42, x_dim=500, out_dim=3, N=19717)
    rec early stopping epoch 4
    [repro] rec attempt=0 lr_rec=0.01 core_max=9.596594e-10 best_err=9.804979e-04
    [repro] core collapsed, retry 1 with lr_rec=0.001
    [repro] edge_mode=topk12 thresh=0.4390 adj min/mean/max=... edges=24 density=0.1067
    [repro] feat_from_cluster=0 unique_x=4/15 mask_quota(train/val/test)=[14, 0, 1] assigned=[14, 0, 1]
    condensation time (s): 138.411821236
    test loss 0.5986268520355225 | test acc79.70 | best_val_acc 80.00

注意：
  * `test acc` 是在**原图** test 上、用**原图 val** 选最优 checkpoint 得到的（协议同论文）。
  * 塌缩重试会改变实际使用的 `lr_rec`：本脚本给出最终生效值 `lr_rec_used`。

用法: python scripts/parse_gctd_log.py results/gctd/runs/*.log [--csv out.csv]
"""
import argparse
import csv
import re
import sys

NAMESPACE = re.compile(r"^Namespace\((.*)\)\s*$")
KV = re.compile(r"(\w+)=('([^']*)'|[^,)]+)")
ATTEMPT = re.compile(
    r"^\[repro\] rec attempt=(\d+) lr_rec=([\d.eE+-]+) core_max=([\d.eE+-]+) best_err=([\d.eE+-]+)"
)
EDGE = re.compile(r"^\[repro\] edge_mode=(\S+) thresh=([\d.]+)")
EDGE_FULL = re.compile(
    r"edges=(\d+) density=([\d.]+)"
)
UNIQUE = re.compile(r"^\[repro\] feat_from_cluster=(\d+) unique_x=(\d+)/(\d+)")
COND_TIME = re.compile(r"^condensation time \(s\): ([\d.]+)")
RESULT = re.compile(
    r"^test loss ([\d.]+) \| test acc([\d.]+) \| best_val_acc ([\d.]+)"
)
EARLY = re.compile(r"^rec early stopping epoch (\d+)")


def parse(path):
    meta, attempts, early = {}, [], []
    edge_mode = edges = density = ""
    unique_x = n_synth = ""
    cond_time = None
    test_acc = best_val = ""
    saw_any = False
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            m = NAMESPACE.match(line)
            if m:
                for kv in KV.finditer(m.group(1)):
                    meta[kv.group(1)] = kv.group(2).strip("'")
                continue
            m = ATTEMPT.match(line)
            if m:
                attempts.append(
                    {
                        "attempt": int(m.group(1)),
                        "lr_rec": float(m.group(2)),
                        "core_max": float(m.group(3)),
                        "best_err": float(m.group(4)),
                    }
                )
                saw_any = True
                continue
            m = EDGE.match(line)
            if m:
                edge_mode, thresh = m.group(1), m.group(2)
                meta["edge_thresh_used"] = thresh
                m2 = EDGE_FULL.search(line)
                if m2:
                    edges, density = m2.group(1), m2.group(2)
                continue
            m = UNIQUE.match(line)
            if m:
                meta["feat_from_cluster"] = m.group(1)
                unique_x, n_synth = m.group(2), m.group(3)
                continue
            m = COND_TIME.match(line)
            if m:
                cond_time = m.group(1)
                continue
            m = EARLY.match(line)
            if m:
                early.append(m.group(1))
                continue
            m = RESULT.match(line)
            if m:
                test_acc, best_val = m.group(2), m.group(3)
                continue
    if not meta.get("dataset") or not test_acc:
        return None
    last = attempts[-1] if attempts else {}
    return {
        "log": path,
        "dataset": meta.get("dataset", ""),
        "reduction_rate": meta.get("reduction_rate", ""),
        "seed": meta.get("seed", ""),
        "rec_epochs": meta.get("rec_epochs", ""),
        "gnn_epochs": meta.get("gnn_epochs", ""),
        "n_synth": n_synth,
        "unique_x": unique_x,
        "rec_attempts": len(attempts),
        "lr_rec_used": ("%.1e" % last["lr_rec"]) if last else "",
        "core_max": ("%.3e" % last["core_max"]) if last else "",
        "edge_mode": edge_mode,
        "edges": edges,
        "density": density,
        "condensation_s": cond_time or "",
        "test_acc": test_acc,
        "best_val_acc": best_val,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--csv", default="")
    args = ap.parse_args()
    results = [r for r in (parse(p) for p in args.logs) if r]
    if not results:
        print("no parsable log", file=sys.stderr)
        sys.exit(1)
    results.sort(key=lambda r: (r["dataset"], int(r["seed"] or 0)))
    keys = list(results[0].keys())
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(results)
    show = [
        "dataset", "reduction_rate", "seed", "rec_epochs", "test_acc", "best_val_acc",
        "lr_rec_used", "rec_attempts", "n_synth", "edges", "density", "condensation_s",
    ]
    print("\t".join(show))
    for r in results:
        print("\t".join(str(r[k]) for k in show))


if __name__ == "__main__":
    main()
