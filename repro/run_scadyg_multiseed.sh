#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SELECTION_METRIC="${1:-mrr}"
if [[ $# -gt 0 ]]; then
  shift
fi

if [[ "${SELECTION_METRIC}" != "ap" && "${SELECTION_METRIC}" != "mrr" && "${SELECTION_METRIC}" != "filtered_mrr" ]]; then
  echo "selection metric 必须是 ap、mrr 或 filtered_mrr" >&2
  exit 1
fi

EVAL_ARGS=()
if [[ "${SELECTION_METRIC}" == "filtered_mrr" ]]; then
  EVAL_ARGS=(--eval_protocol both)
fi

if [[ $# -eq 0 ]]; then
  SEEDS=(0 1 2 3 4)
else
  SEEDS=("$@")
fi

for seed in "${SEEDS[@]}"; do
  echo "[multiseed] selection_metric=${SELECTION_METRIC} seed=${seed}"
  bash "${SCRIPT_DIR}/run_scadyg.sh" mooc \
    --seed "${seed}" \
    --selection_metric "${SELECTION_METRIC}" \
    "${EVAL_ARGS[@]}"
done
