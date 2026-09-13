#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -eq 0 ]]; then
  SEEDS=(0 1 2 3 4)
else
  SEEDS=("$@")
fi

for seed in "${SEEDS[@]}"; do
  echo "[bipartite-multiseed] seed=${seed}"
  bash "${SCRIPT_DIR}/run_scadyg.sh" mooc \
    --seed "${seed}" \
    --eval_protocol both \
    --selection_metric filtered_mrr \
    --train_negative_protocol mooc_bipartite
done
