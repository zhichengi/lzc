#!/usr/bin/env bash
# STEM-GNN：禁止 conda env create -f 官方 environment.yml（整机导出）。
# 需要时从 dtgb 克隆后按最小依赖补包。
set -euo pipefail
CONDA_HOME="${CONDA_HOME:-/home/lab_user/tools/miniconda3}"
# shellcheck disable=SC1091
source "${CONDA_HOME}/etc/profile.d/conda.sh"
if conda env list | awk '{print $1}' | grep -qx stem_gnn; then
  echo "[setup] stem_gnn 已存在"
  exit 0
fi
echo "[setup] 尚未创建。需要时："
echo "  conda create -n stem_gnn --clone dtgb"
echo "  conda activate stem_gnn"
echo "  # 再按 STEM-GNN 实际 import 补 transformers / dgl 等，不要喂完整 yml"
exit 0
