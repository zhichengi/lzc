#!/usr/bin/env python3
"""Summarize ScaDyG run logs and compare AP/MRR checkpoint epochs."""

from __future__ import annotations

import argparse
import math
import re
import statistics
from pathlib import Path


OLD_VAL_SUMMARY_RE = re.compile(
    r"validation summary epoch:(?P<epoch>\d+), avg_mrr:(?P<mrr>[0-9.]+), "
    r"avg_ap:(?P<ap>[0-9.]+),"
)
DUAL_VAL_SUMMARY_RE = re.compile(
    r"validation summary epoch:(?P<epoch>\d+), "
    r"avg_official_mrr:(?P<mrr>[0-9.]+), "
    r"global_filtered_mrr:(?P<filtered_mrr>[0-9.]+|nan), "
    r"avg_ap:(?P<ap>[0-9.]+),"
)


def first_match(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else default


def parse_log(path: Path) -> dict[str, object]:
    text = path.read_text(errors="replace")
    epoch_summary: dict[int, dict[str, float]] = {}
    for match in OLD_VAL_SUMMARY_RE.finditer(text):
        epoch_summary[int(match["epoch"])] = {
            "mrr": float(match["mrr"]),
            "filtered_mrr": math.nan,
            "ap": float(match["ap"]),
        }
    for match in DUAL_VAL_SUMMARY_RE.finditer(text):
        epoch_summary[int(match["epoch"])] = {
            "mrr": float(match["mrr"]),
            "filtered_mrr": float(match["filtered_mrr"]),
            "ap": float(match["ap"]),
        }
    if not epoch_summary:
        raise ValueError(f"no validation summaries found in {path}")

    ap_epoch = max(epoch_summary, key=lambda epoch: epoch_summary[epoch]["ap"])
    mrr_epoch = max(epoch_summary, key=lambda epoch: epoch_summary[epoch]["mrr"])
    filtered_epochs = [
        epoch
        for epoch, metrics in epoch_summary.items()
        if math.isfinite(metrics["filtered_mrr"])
    ]
    filtered_mrr_epoch = (
        max(
            filtered_epochs,
            key=lambda epoch: epoch_summary[epoch]["filtered_mrr"],
        )
        if filtered_epochs
        else -1
    )

    return {
        "path": str(path),
        "seed": int(first_match(r"--seed (\d+)", text, "-1")),
        "patch": first_match(r"tracked_patch_sha256=([0-9a-f]+)", text, "none"),
        "last_epoch": max(epoch_summary),
        "test_mrr": float(first_match(r"\{'avg_mrr': ([0-9.eE+-]+)\}", text, "nan")),
        "test_filtered_mrr": float(
            first_match(r"\{'avg_filtered_mrr': ([0-9.eE+-]+)\}", text, "nan")
        ),
        "test_ap": float(first_match(r"\{'avg_ap': ([0-9.eE+-]+)\}", text, "nan")),
        "test_auc": float(first_match(r"\{'avg_auc': ([0-9.eE+-]+)\}", text, "nan")),
        "runtime": float(first_match(r"All time: ([0-9.eE+-]+)", text, "nan")),
        "ap_epoch": ap_epoch,
        "ap_epoch_val_ap": epoch_summary[ap_epoch]["ap"],
        "ap_epoch_val_mrr": epoch_summary[ap_epoch]["mrr"],
        "mrr_epoch": mrr_epoch,
        "mrr_epoch_val_mrr": epoch_summary[mrr_epoch]["mrr"],
        "mrr_epoch_val_ap": epoch_summary[mrr_epoch]["ap"],
        "filtered_mrr_epoch": filtered_mrr_epoch,
        "filtered_mrr_epoch_val": (
            epoch_summary[filtered_mrr_epoch]["filtered_mrr"]
            if filtered_mrr_epoch >= 0
            else math.nan
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("logs", nargs="+", type=Path)
    args = parser.parse_args()

    runs = [parse_log(path) for path in args.logs]
    for run in runs:
        print(
            "seed={seed} official_mrr={test_mrr:.6f} "
            "filtered_mrr={test_filtered_mrr:.6f} last_epoch={last_epoch} "
            "AP-selected={ap_epoch} (val_ap={ap_epoch_val_ap:.6f}, "
            "val_mrr={ap_epoch_val_mrr:.6f}) MRR-selected={mrr_epoch} "
            "(val_mrr={mrr_epoch_val_mrr:.6f}, val_ap={mrr_epoch_val_ap:.6f}) "
            "filtered-selected={filtered_mrr_epoch} "
            "(val_filtered_mrr={filtered_mrr_epoch_val:.6f}) "
            "log={path}".format(**run)
        )

    test_mrr = [float(run["test_mrr"]) for run in runs]
    test_filtered_mrr = [
        float(run["test_filtered_mrr"])
        for run in runs
        if math.isfinite(float(run["test_filtered_mrr"]))
    ]
    if len(test_mrr) > 1:
        print(
            f"official n={len(test_mrr)} mean={statistics.mean(test_mrr):.6f} "
            f"sample_std={statistics.stdev(test_mrr):.6f}"
        )
    if len(test_filtered_mrr) > 1:
        print(
            f"filtered n={len(test_filtered_mrr)} "
            f"mean={statistics.mean(test_filtered_mrr):.6f} "
            f"sample_std={statistics.stdev(test_filtered_mrr):.6f}"
        )


if __name__ == "__main__":
    main()
