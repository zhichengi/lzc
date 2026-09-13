#!/usr/bin/env python
"""解析 IGNN 单次运行日志，给出逐划分精度与汇总。

`repro/run_ignn.sh` 每个 run 建一个目录 `results/ignn/runs/<UTC时间戳>_<标签>/`，
内含 `run.log` / `command.txt` / `metadata.txt`。`run.log` 关键行：

    run_dir=/.../20260913T141111Z_official_actor_c_custom_r10
    started_utc=2026-09-13T14:11:13+00:00
    command=.../python -u -m main ... --dataset actor --source pyg ... --repeat 10
    [I ... the_utils.common:35] split num: 10; random splits train:val:test =48:32:20
    [I ... __main__:210] actor_pyg 0 res: 0.37105263157894736
    ...
    [I ... __main__:214] Results:       Acc:37.43±0.97  Train cost: 7.13s
    finished_utc=2026-09-13T14:12:00+00:00
    exit_code=0

两种划分提示要区分（决定这数字能不能当协议结果）：
  * `public split train:val:test`  → 读的是数据集自带 public mask
  * `random splits train:val:test` → 读的是 48/32/20 随机划分（论文主协议）
注意这两段在日志里可能是**两行**（custom 运行）或**一行带分号**（public 运行），
所以两者分别匹配。
若出现 `No fixed splits found ... splitsx<N>.npy, generating...`，说明**没有加载
官方固定划分**，而是现场随机生成，该 run 的划分不能当协议结果（`repeat=1` 的烟雾
测试必然如此）。

用法: python scripts/parse_ignn_log.py results/ignn/runs/*/run.log [--csv out.csv]
     python scripts/parse_ignn_log.py results/ignn/runs/*official*custom_r10/run.log
"""
import argparse
import csv
import re
import statistics
import sys
from pathlib import Path

RUN_DIR = re.compile(r"^run_dir=(.*)$")
STARTED = re.compile(r"^started_utc=(.*)$")
FINISHED = re.compile(r"^finished_utc=(.*)$")
EXIT = re.compile(r"^exit_code=(\d+)$")
COMMAND = re.compile(r"^command=(.*)$")
SPLIT_NUM = re.compile(r"split num:\s*(\d+)")
SPLIT_KIND = re.compile(
    r"(public split|random splits)\s*train:val:test\s*=\s*([\d.:]+)"
)
NO_FIXED = re.compile(r"No fixed splits found in (\S+?), generating")
PER_SPLIT = re.compile(r"__main__:\d+\]\s*(\S+)\s+(\d+)\s+res:\s*([\d.]+)")
RESULTS = re.compile(r"__main__:\d+\]\s*Results:\s*Acc:([\d.]+)±([\d.]+)")

# 从命令行取超参，便于分辨 run 的配置
ARG_RE = re.compile(r"--([a-z_0-9]+)\s+(\S+)")


def parse(path):
    meta, per_split, no_fixed = {}, [], []
    split_kind = split_ratio = split_num = ""
    acc = std = ""
    exit_code = ""
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    for line in text.splitlines():
        line = line.strip()
        for rgx, key in ((RUN_DIR, "run_dir"), (STARTED, "started_utc"),
                         (FINISHED, "finished_utc"), (COMMAND, "command")):
            m = rgx.match(line)
            if m:
                meta[key] = m.group(1).strip()
        m = EXIT.match(line)
        if m:
            exit_code = m.group(1)
        m = SPLIT_NUM.search(line)
        if m:
            split_num = m.group(1)
        m = SPLIT_KIND.search(line)
        if m:
            split_kind, split_ratio = m.group(1), m.group(2)
        m = NO_FIXED.search(line)
        if m:
            no_fixed.append(m.group(1))
        m = PER_SPLIT.search(line)
        if m:
            per_split.append((m.group(1), int(m.group(2)), float(m.group(3))))
        m = RESULTS.search(line)
        if m:
            acc, std = m.group(1), m.group(2)
    if not meta.get("run_dir") and not per_split:
        return None

    cmd = meta.get("command", "")
    args = {k: v for k, v in ARG_RE.findall(cmd)}
    label = Path(meta.get("run_dir", path)).name
    vals = [v * 100 for _, _, v in per_split]
    recomputed = f"{statistics.mean(vals):.2f}" if vals else ""
    recomputed_std = f"{statistics.stdev(vals):.2f}" if len(vals) > 1 else ""

    return {
        "label": label,
        "run_dir": meta.get("run_dir", str(Path(path).parent)),
        "dataset": args.get("dataset", per_split[0][0] if per_split else ""),
        "source": args.get("source", ""),
        "model": args.get("model", ""),
        "repeat": args.get("repeat", ""),
        "public": args.get("public", ""),
        "seed": args.get("seed", ""),
        "n_layers": args.get("n_layers", ""),
        "h_feats": args.get("h_feats", ""),
        "lr": args.get("lr", ""),
        "split_num": split_num,
        "split_kind": split_kind,
        "split_ratio": split_ratio,
        "no_fixed_split": "yes" if no_fixed else "",
        "n_parsed": len(per_split),
        "acc": acc,
        "acc_std": std,
        "recomputed_acc": recomputed,
        "recomputed_std": recomputed_std,
        "exit_code": exit_code,
        "started_utc": meta.get("started_utc", ""),
        "finished_utc": meta.get("finished_utc", ""),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--csv", default="")
    ap.add_argument("--only-fixed", action="store_true",
                    help="只保留未出现 No fixed splits 的 run（即可当协议结果的）")
    args = ap.parse_args()
    rows = [r for r in (parse(p) for p in args.logs) if r]
    if args.only_fixed:
        rows = [r for r in rows if not r["no_fixed_split"]]
    if not rows:
        print("no parsable log", file=sys.stderr)
        sys.exit(1)
    rows.sort(key=lambda r: (r["dataset"], r["label"]))
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {args.csv}")
    show = ["label", "dataset", "source", "repeat", "public", "split_kind",
            "split_ratio", "no_fixed_split", "n_parsed", "acc", "acc_std",
            "exit_code"]
    print("\t".join(show))
    for r in rows:
        print("\t".join(str(r[k]) for k in show))
    return 0


if __name__ == "__main__":
    sys.exit(main())
