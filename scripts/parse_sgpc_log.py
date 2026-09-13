#!/usr/bin/env python
"""解析 SGPC 官方 main.py 的 stdout 日志，给出三种 test 精度。

官方脚本只在 `epoch % 50 == 0` 或 `val_acc == best_val` 时打印一行
    Epoch 0031 | Loss: 0.1607 | Val: 0.8644 | Test: 0.7838 | Best Test: 0.8108
其中 `Best Test` 是训练全程 test 的最大值（用 test 选模），不是论文/常规协议。
本脚本输出：
  oracle_best_test : 官方打印的 Best Test 最终值
  val_selected_test: 首次达到全程最高 val 的那个 epoch 的 test（常规协议）
  val_selected_last: 最后一次达到最高 val 的 epoch 的 test（平局取后）
  last_printed_test: 最后一行打印的 test

用法: python scripts/parse_sgpc_log.py results/sgpc/runs/*.log [--csv out.csv]
"""
import argparse
import csv
import re
import sys

LINE = re.compile(
    r"^Epoch (\d+) \| Loss: ([\d.]+) \| Val: ([\d.]+) \| Test: ([\d.]+) \| Best Test: ([\d.]+)"
)
META = re.compile(r"^\[repro\] (\w+)=(.*)$")
SGPC_KV = re.compile(r"^\[sgpc\] (config|summary) (.+)$")


def _kv(s):
    out = {}
    for part in s.split():
        if "=" in part:
            k, v = part.split("=", 1)
            out[k] = v
    return out


def parse(path):
    meta, rows, sgpc = {}, [], {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = META.match(line.strip())
            if m:
                meta[m.group(1)] = m.group(2)
                continue
            m = SGPC_KV.match(line.strip())
            if m:
                sgpc.update(_kv(m.group(2)))
                continue
            m = LINE.match(line.strip())
            if m:
                ep, loss, val, test, best = m.groups()
                rows.append((int(ep), float(loss), float(val), float(test), float(best)))
            elif line.startswith("Early stopping at epoch"):
                meta["early_stop_epoch"] = line.strip().split()[-1]
    if not rows and "val_selected_test" not in sgpc:
        return None
    if rows:
        max_val = max(r[2] for r in rows)
        first = next(r for r in rows if r[2] == max_val)
        last = [r for r in rows if r[2] == max_val][-1]
        best_val = round(max_val * 100, 2)
        val_selected_epoch = first[0]
        val_selected_test = round(first[3] * 100, 2)
        val_selected_last_epoch = last[0]
        val_selected_last = round(last[3] * 100, 2)
        oracle_best_test = round(rows[-1][4] * 100, 2)
        last_printed_test = round(rows[-1][3] * 100, 2)
        last_epoch = rows[-1][0]
    else:
        best_val = val_selected_epoch = val_selected_test = ""
        val_selected_last_epoch = val_selected_last = ""
        oracle_best_test = last_printed_test = last_epoch = ""
    if "val_selected_test" in sgpc:
        val_selected_test = round(float(sgpc["val_selected_test"]) * 100, 2)
        oracle_best_test = round(float(sgpc.get("oracle_best_test", 0)) * 100, 2)
        val_selected_epoch = int(float(sgpc.get("val_selected_epoch", 0)))
        best_val = round(float(sgpc.get("best_val", 0)) * 100, 2)
        last_epoch = int(float(sgpc.get("last_epoch", last_epoch or 0)))
    return {
        "log": path,
        "run_id": meta.get("run_id", ""),
        "dataset": meta.get("dataset", ""),
        "commit": meta.get("repo_commit", "")[:12],
        "patch": meta.get("tracked_patch_sha256", meta.get("tracked_patch", ""))[:12],
        "split": sgpc.get("split", ""),
        "seed": sgpc.get("seed", ""),
        "spec": sgpc.get("spec", ""),
        "epochs_printed": len(rows),
        "last_epoch": last_epoch,
        "early_stop_epoch": meta.get("early_stop_epoch", ""),
        "best_val": best_val,
        "val_selected_epoch": val_selected_epoch,
        "val_selected_test": val_selected_test,
        "val_selected_last_epoch": val_selected_last_epoch,
        "val_selected_last": val_selected_last,
        "oracle_best_test": oracle_best_test,
        "last_printed_test": last_printed_test,
        "runtime_seconds": meta.get("runtime_seconds", ""),
        "exit_code": meta.get("exit_code", ""),
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
    keys = list(results[0].keys())
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(results)
    show = ["dataset", "split", "seed", "spec", "run_id", "val_selected_epoch", "val_selected_test", "oracle_best_test", "last_printed_test", "early_stop_epoch", "runtime_seconds"]
    print("\t".join(show))
    for r in results:
        print("\t".join(str(r[k]) for k in show))


if __name__ == "__main__":
    main()
