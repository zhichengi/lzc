#!/usr/bin/env bash
# Equivariance 训练烟雾：等第一批 GPU 队列结束后再占卡。
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
log() { echo "[eq-smoke] $(date --iso-8601=seconds) $*"; }

log "waiting for repro/run_remaining_gpu_smokes.sh"
while pgrep -f '[b]ash .*/repro/run_remaining_gpu_smokes.sh' >/dev/null; do
  sleep 30
done
# 队列脚本退出后，其子训练可能还在最后一条；再等 GPU 训练进程清空
log "queue script gone; wait until no leftover GPU trainers"
while pgrep -f 'ChebStable_peptide.py|train.py --dataset-name corafull|[p]ython train.py --exp|[p]ython main.py --dataset_name cora' >/dev/null; do
  sleep 15
done

log "GPU free. start equivariance GAT 2ep (dtgb, neptune offline)"
export NEPTUNE_MODE=offline
export NEPTUNE_API_TOKEN="${NEPTUNE_API_TOKEN:-anonymous}"
unset CUDA_VISIBLE_DEVICES

bash scripts/repro_wrap.sh --paper equivariance --env dtgb --repo repro/equivariance --cwd repro/equivariance \
  --label smoke_gat_cora_2ep -- \
  python -u main.py --project offline/smoke --is_train --gnn_type GAT --lr 0.001 --lp_ratio 0.3 --max_epochs 2
log "equivariance exit=$?"
log "done"
