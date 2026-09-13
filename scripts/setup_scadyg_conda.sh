#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONDA_HOME="${CONDA_HOME:-/home/lab_user/tools/miniconda3}"
ENV_NAME="${SCADYG_CONDA_ENV:-scadyg}"
BASE_ENV="${SCADYG_BASE_ENV:-dtgb}"

if [[ ! -f "${CONDA_HOME}/etc/profile.d/conda.sh" ]]; then
  echo "找不到 conda: ${CONDA_HOME}" >&2
  exit 1
fi

# 复用已经验证可用的 CUDA 12.1、torch、PyG 扩展和 DGL 组合，避免安装
# 官方完整 requirements.txt 中互相冲突的 torch 1.12 / PyG 2.5 / DGL 1.0。
source "${CONDA_HOME}/etc/profile.d/conda.sh"
if ! conda env list | awk -v name="${ENV_NAME}" '$1 == name {found=1} END {exit !found}'; then
  conda create --name "${ENV_NAME}" --clone "${BASE_ENV}" -y
fi

conda activate "${ENV_NAME}"
python -m pip install -r "${ROOT_DIR}/repro/requirements-scadyg.txt"

python - <<'PY'
import dgl
import deepsnap
import tgb
import torch
import torch_geometric
import torch_scatter
import torch_sparse
import yacs

print("torch", torch.__version__)
print("torch_geometric", torch_geometric.__version__)
print("dgl", dgl.__version__)
print("cuda", torch.cuda.is_available(), torch.cuda.device_count())
print("deepsnap", getattr(deepsnap, "__version__", "installed"))
print("tgb", getattr(tgb, "__version__", "installed"))
print("yacs", getattr(yacs, "__version__", "installed"))
PY
