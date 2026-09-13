#!/usr/bin/env bash
# R-SCADYG-2：三个组件消融 × seeds 0–4，同时输出 official 与 filtered MRR。
#
# 每个 (ablation, seed) 起独立进程，走 repro/run_scadyg.sh（独立日志 + checkpoint）。
# 选模口径固定 --selection_metric mrr（与论文主指标一致），
# 并加 --eval_protocol both，让每次运行同时产出 official 与 filtered MRR。
#
# 用法:
#   bash repro/run_scadyg_ablation.sh                  # none/time/topo/hyper × 0–4
#   bash repro/run_scadyg_ablation.sh topo             # 只跑某一个消融
#   bash repro/run_scadyg_ablation.sh time 0 1         # 指定 seed
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ABLATIONS=("none" "time" "topo" "hyper")

if [[ $# -gt 0 && "$1" =~ ^(none|time|topo|hyper)$ ]]; then
  ABLATIONS=("$1")
  shift
fi

if [[ $# -gt 0 ]]; then
  SEEDS=("$@")
else
  SEEDS=(0 1 2 3 4)
fi

for ab in "${ABLATIONS[@]}"; do
  for seed in "${SEEDS[@]}"; do
    echo "[ablation] component=${ab} seed=${seed} $(date --iso-8601=seconds)"
    bash "${SCRIPT_DIR}/run_scadyg.sh" mooc \
      --seed "${seed}" \
      --selection_metric mrr \
      --eval_protocol both \
      --ablate "${ab}"
  done
done

echo "[ablation] done $(date --iso-8601=seconds)"
