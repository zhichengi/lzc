#!/usr/bin/env python
"""解析 GBN 的 NC 运行日志，给出逐 iter 精度与汇总。

外层日志由 `scripts/repro_wrap.sh` 生成（`results/gbn/runs/<stamp>_<label>_pid<pid>.log`），
内含官方 `main.py` 的 stdout。关键行：

    [repro] run_id=20260913_222959_official_Texas_r10_pid290777
    [repro] repo_commit=72ad3692916ecc60f2c78d5bd01a55d7c6297a4f
    INFO - 09/13/26 22:33:12 - 0:02:10 - test_acc= 84.62%, weighted_f1= ...,macro_f1= ...%
    INFO - ... Best ACCs: [83.08, 84.62, ...]
    INFO - ... Evaluation Acc is  84.02% ±  4.19%

注意：
  * 官方用 `np.std(...)`（**总体**标准差，ddof=0）汇总 `Evaluation Acc is`。
    本脚本同时给出 `std_ddof0`（与官方一致）与 `std_ddof1`（样本标准差，与
    本项目其它线的 `*_multiseed_summary.csv` 口径一致）。
  * 每条 `test_acc=` 会被 logger 打印两次（stdout + 文件），所以逐 iter 数值以
    `Best ACCs` 行或去重后为准。

用法:
    python scripts/parse_gbn_log.py results/gbn/runs/*official_*_r10*.log
    python scripts/parse_gbn_log.py results/gbn/runs/*official_*_r10*.log --csv results/gbn/nc_table_summary.csv
"""
import argparse
import csv
import re
import statistics
import sys
from pathlib import Path

RUN_ID = re.compile(r"^\[repro\] run_id=(\S+)")
COMMIT = re.compile(r"^\[repro\] repo_commit=(\S+)")
COMMAND = re.compile(r"^\[repro\] command=(.*)$")
EXIT = re.compile(r"^\[repro\] exit_code=(\d+)")
RUNTIME = re.compile(r"^\[repro\] runtime_seconds=(\d+)")
BEST_ACCS = re.compile(r"Best ACCs:\s*\[([^\]]*)\]")
EVAL_ACC = re.compile(r"Evaluation Acc is\s+([\d.]+)%\s*±\s*([\d.]+)%")
TEST_ACC = re.compile(r"test_acc=\s*([\d.]+)%")

DS_ARG = re.compile(r"--dataset\s+(\S+)")
# 消融运行的标签形如 ablate_<mode>_<DS>_r10。
# mode 名里含下划线（gamma0_beta0 / gamma_all0 / gamma_beta_all0），
# 用裸 [a-z0-9]+ 会截断成 gamma / beta，所以按已知模式表匹配（长的优先）。
ABLATION_MODES = ["gamma_beta_all0", "gamma0_beta0", "gamma_all0", "beta_all0"]


def ablate_of(label):
    for m in ABLATION_MODES:
        if f"ablate_{m}_" in label:
            return m
    return ""


def parse(path):
    meta = {}
    accs, eval_pair = [], None
    seen_test = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            for rgx, key in ((RUN_ID, "run_id"), (COMMIT, "repo_commit"),
                             (COMMAND, "command"), (EXIT, "exit_code"),
                             (RUNTIME, "runtime_seconds")):
                m = rgx.match(line)
                if m:
                    meta[key] = m.group(1).strip()
            m = BEST_ACCS.search(line)
            if m:
                accs = [float(v) for v in m.group(1).split(",") if v.strip()]
            m = EVAL_ACC.search(line)
            if m:
                eval_pair = (float(m.group(1)), float(m.group(2)))
            m = TEST_ACC.search(line)
            if m:
                seen_test.append(float(m.group(1)))
    if not accs and not eval_pair:
        return None
    cmd = meta.get("command", "")
    m = DS_ARG.search(cmd)
    dataset = m.group(1) if m else ""
    if accs:
        mean = statistics.mean(accs)
        std0 = statistics.pstdev(accs) if len(accs) > 1 else 0.0
        std1 = statistics.stdev(accs) if len(accs) > 1 else 0.0
    else:
        mean, std0, std1 = (eval_pair or ("", ""))[0], (eval_pair or ("", ""))[1], ""
    # label 里的数据集名（用于 CSV 排序）
    label = meta.get("run_id", Path(path).name)
    return {
        "label": label,
        "dataset": dataset,
        "ablate": ablate_of(label),
        "n_iters": len(accs),
        "acc_mean": f"{mean:.2f}" if mean != "" else "",
        "std_ddof0": f"{std0:.2f}" if std0 != "" else "",
        "std_ddof1": f"{std1:.2f}" if std1 != "" else "",
        "official_eval_acc": f"{eval_pair[0]:.2f}" if eval_pair else "",
        "official_eval_std": f"{eval_pair[1]:.2f}" if eval_pair else "",
        "per_iter": ";".join(f"{a:.2f}" for a in accs),
        "exit_code": meta.get("exit_code", ""),
        "runtime_seconds": meta.get("runtime_seconds", ""),
        "repo_commit": meta.get("repo_commit", "")[:12],
        "log": path,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--csv", default="")
    args = ap.parse_args()
    rows = [r for r in (parse(p) for p in args.logs) if r]
    if not rows:
        print("no parsable log", file=sys.stderr)
        sys.exit(1)
    rows.sort(key=lambda r: (r.get("ablate", ""), r["dataset"]))
    show = ["ablate", "dataset", "n_iters", "acc_mean", "std_ddof0", "std_ddof1",
            "exit_code", "runtime_seconds"]
    print("\t".join(show))
    for r in rows:
        print("\t".join(str(r[k]) for k in show))
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {args.csv}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
