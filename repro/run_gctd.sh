#!/usr/bin/env bash
# 从仓库内相对路径启动 GCTD，不依赖绝对路径与当前工作目录。
# 用法:
#   bash repro/run_gctd.sh cora 0.013
#   bash repro/run_gctd.sh cora 0.013 --rec_epochs 2 --gnn_epochs 2   # 烟雾测试
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GCTD_DIR="${SCRIPT_DIR}/gctd"
# 工作区根 = repro/..
WS_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

DATASET="${1:-cora}"
RATE="${2:-0.013}"
shift 2 || true

STAMP="$(date +%Y%m%d_%H%M%S)"
LOG_REL="../../results/gctd/runs/${STAMP}_${DATASET}.log"

mkdir -p "${WS_ROOT}/results/gctd/runs"
mkdir -p "${GCTD_DIR}/data"

export WANDB_MODE="${WANDB_MODE:-disabled}"
export WANDB_DIR="${WS_ROOT}/results/gctd/wandb"
export PYTHONUNBUFFERED=1

# 优先使用专用环境 gctd（官方钉扎），否则回退 dtgb。
# 已激活 dtgb 时仍切到 gctd，避免版本混用。可用 GCTD_CONDA_ENV 覆盖。
if command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
  WANT="${GCTD_CONDA_ENV:-}"
  if [[ -z "${WANT}" ]]; then
    if conda env list 2>/dev/null | awk '{print $1}' | grep -qx gctd; then
      WANT=gctd
    elif conda env list 2>/dev/null | awk '{print $1}' | grep -qx dtgb; then
      WANT=dtgb
    fi
  fi
  if [[ -n "${WANT}" && "${CONDA_DEFAULT_ENV:-}" != "${WANT}" ]]; then
    conda activate "${WANT}"
  fi
fi

cd "${GCTD_DIR}"
python src/train.py \
  --dataset "${DATASET}" \
  --reduction_rate "${RATE}" \
  --data_dir data \
  --save_dir saved_ours \
  --log_file "${LOG_REL}" \
  --no_wandb \
  --cuda \
  "$@"
