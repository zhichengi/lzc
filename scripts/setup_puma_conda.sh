#!/usr/bin/env bash
# 从 dtgb 克隆出 puma 环境，再装官方声明的较旧栈。不改 dtgb。
set -euo pipefail
CONDA_HOME="${CONDA_HOME:-/home/lab_user/tools/miniconda3}"
# shellcheck disable=SC1091
source "${CONDA_HOME}/etc/profile.d/conda.sh"
if conda env list | awk '{print $1}' | grep -qx puma; then
  echo "[setup] puma 已存在"
  exit 0
fi
if conda env list | awk '{print $1}' | grep -qx dtgb; then
  conda create -n puma --clone dtgb -y
else
  conda create -n puma python=3.10 -y
fi
echo "[setup] 官方钉 python3.8/torch1.13。当前策略：先 clone dtgb 试跑。"
echo "[setup] 若烟雾因 API 失败，再在 puma 里降级 torch，不要动 dtgb。"
conda activate puma
python - <<'PY'
import torch, torch_geometric
print("puma env torch", torch.__version__, "pyg", torch_geometric.__version__)
PY
