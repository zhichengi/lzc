#!/usr/bin/env bash
# 异配图 geom-gcn 10 划分遍历。固定 --seed 0，使每个划分可复现。
# 用法: bash repro/run_sgpc_splits.sh LABEL_PREFIX [DATA_ID ...]
#   例: bash repro/run_sgpc_splits.sh webkb_s0 6 7 8
set -uo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -lt 1 ]]; then
  echo "用法: $0 LABEL_PREFIX [DATA_ID ...]" >&2
  exit 2
fi
PREFIX="${1//[^A-Za-z0-9._-]/_}"
shift
IDS=("$@")
if [[ ${#IDS[@]} -eq 0 ]]; then
  IDS=(6 7 8)
fi
for id in "${IDS[@]}"; do
  for s in $(seq 0 9); do
    echo "[splits] === data_id=${id} split=${s} $(date --iso-8601=seconds)"
    bash "${ROOT_DIR}/repro/run_sgpc.sh" "${PREFIX}_s${s}" "${id}" --split "${s}" --seed 0
  done
done
echo "[splits] done $(date --iso-8601=seconds)"
