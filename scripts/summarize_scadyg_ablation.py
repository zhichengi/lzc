#!/usr/bin/env python
"""汇总 ScaDyG 组件消融（R-SCADYG-2）的多种子结果。

复用 `scripts/analyze_scadyg_logs.py:parse_log` 的解析逻辑，额外从日志里读
`--ablate` 与 `--seed`，按组件分组给出 official / filtered MRR 的均值±样本标准差。

用法（在仓库根）:
    python scripts/summarize_scadyg_ablation.py results/scadyg/runs/2026*_mooc_pid*.log
    python scripts/summarize_scadyg_ablation.py <logs> --csv results/scadyg/ablation_summary.csv
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze_scadyg_logs import parse_log  # noqa: E402

ABLATE_RE = re.compile(r"--ablate (\w+)")
PAPER_OFFICIAL = 0.931
PAPER_STD = 0.009


def extract(path: Path) -> dict | None:
    try:
        run = parse_log(path)
    except ValueError:
        return None
    text = path.read_text(errors="replace")
    m = ABLATE_RE.search(text)
    ablate = m.group(1) if m else "unknown"
    return {
        "log": str(path),
        "ablate": ablate,
        "seed": run["seed"],
        "official_mrr": float(run["test_mrr"]),
        "filtered_mrr": float(run["test_filtered_mrr"]),
        "ap": float(run["test_ap"]),
    }


def agg(rows: list[dict], key: str) -> tuple[float, float, int]:
    vals = [r[key] for r in rows if math.isfinite(r[key])]
    if not vals:
        return math.nan, math.nan, 0
    std = statistics.stdev(vals) if len(vals) > 1 else 0.0
    return statistics.mean(vals), std, len(vals)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+", type=Path)
    ap.add_argument("--csv", default="")
    args = ap.parse_args()

    rows = [r for r in (extract(p) for p in args.logs) if r]
    if not rows:
        print("no parsable logs", file=sys.stderr)
        return 1

    order = {"none": 0, "time": 1, "topo": 2, "hyper": 3, "unknown": 9}
    rows.sort(key=lambda r: (order.get(r["ablate"], 9), r["seed"]))

    print(f"{'ablate':<9} {'seed':>4} {'official_mrr':>13} {'filtered_mrr':>13} {'ap':>10}")
    for r in rows:
        print(
            f"{r['ablate']:<9} {r['seed']:>4} {r['official_mrr']:>13.6f} "
            f"{r['filtered_mrr']:>13.6f} {r['ap']:>10.6f}"
        )

    summary = []
    print()
    print(f"{'ablate':<9} {'n':>3} {'official mean±std':>24} {'filtered mean±std':>24} {'Δofficial':>10}")
    for ab in sorted({r["ablate"] for r in rows}, key=lambda a: order.get(a, 9)):
        group = [r for r in rows if r["ablate"] == ab]
        om, os_, on = agg(group, "official_mrr")
        fm, fs, fn = agg(group, "filtered_mrr")
        delta = om - PAPER_OFFICIAL if math.isfinite(om) else math.nan
        print(
            f"{ab:<9} {on:>3} {om:>14.6f} ± {os_:<6.6f} "
            f"{fm:>14.6f} ± {fs:<6.6f} {delta:>+10.4f}"
        )
        summary.append(
            {
                "ablate": ab,
                "n": on,
                "official_mean": f"{om:.6f}" if math.isfinite(om) else "",
                "official_std": f"{os_:.6f}" if math.isfinite(os_) else "",
                "filtered_mean": f"{fm:.6f}" if math.isfinite(fm) else "",
                "filtered_std": f"{fs:.6f}" if math.isfinite(fs) else "",
                "delta_official_to_paper": f"{delta:+.4f}" if math.isfinite(delta) else "",
                "seeds": ";".join(str(r["seed"]) for r in group),
            }
        )

    print()
    print(f"paper (ScaDyG MOOC, MRR-selection): {PAPER_OFFICIAL} ± {PAPER_STD}")

    if args.csv:
        Path(args.csv).parent.mkdir(parents=True, exist_ok=True)
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(summary[0].keys()))
            w.writeheader()
            w.writerows(summary)
        print(f"wrote {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
