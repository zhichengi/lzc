#!/usr/bin/env python
"""按数据集汇总 SGPC 多划分 / 多种子结果（val 选模与 oracle）。"""
import argparse
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_sgpc_log import parse


def mean_std(xs):
    if not xs:
        return "", ""
    if len(xs) == 1:
        return f"{xs[0]:.2f}", "—"
    return f"{statistics.mean(xs):.2f}", f"{statistics.stdev(xs):.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--csv", default="")
    args = ap.parse_args()
    rows = [r for r in (parse(p) for p in args.logs) if r]
    groups = defaultdict(list)
    for r in rows:
        groups[r["dataset"].split()[0] or r["dataset"]].append(r)
    print("dataset\tn\tval_mean\tval_std\toracle_mean\toracle_std")
    out = []
    for name in sorted(groups):
        vals = [float(r["val_selected_test"]) for r in groups[name] if r["val_selected_test"] != ""]
        oras = [float(r["oracle_best_test"]) for r in groups[name] if r["oracle_best_test"] != ""]
        vm, vs = mean_std(vals)
        om, os_ = mean_std(oras)
        print(f"{name}\t{len(vals)}\t{vm}\t{vs}\t{om}\t{os_}")
        out.append({
            "dataset": name,
            "n": len(vals),
            "val_mean": vm,
            "val_std": vs,
            "oracle_mean": om,
            "oracle_std": os_,
        })
    if args.csv and out:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
            w.writeheader()
            w.writerows(out)


if __name__ == "__main__":
    main()
