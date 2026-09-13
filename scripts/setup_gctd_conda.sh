#!/usr/bin/env bash
# 新建与官方钉扎对齐的 conda 环境 gctd，不改动 dtgb。
# Python 3.11 + torch 2.1.2+cu121 + torch-geometric 2.6.1
set -euo pipefail
cd "$(dirname "$0")/.."

PYPI_TUNA="https://pypi.tuna.tsinghua.edu.cn/simple"
TORCH_CU121="https://download.pytorch.org/whl/cu121"
PYG_WHL="https://data.pyg.org/whl/torch-2.1.0+cu121.html"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found" >&2
  exit 1
fi

eval "$(conda shell.bash hook)"

if conda env list | awk '{print $1}' | grep -qx gctd; then
  echo "[setup] conda env gctd already exists"
else
  echo "[setup] creating conda env gctd (python 3.11)"
  conda create -n gctd python=3.11 -y
fi

conda activate gctd
python -m pip install -U pip \
  -i "${PYPI_TUNA}" --trusted-host pypi.tuna.tsinghua.edu.cn

echo "[setup] torch 2.1.2+cu121"
python -m pip install \
  torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 \
  --index-url "${TORCH_CU121}"

echo "[setup] torch-geometric 2.6.1 + CUDA ops"
python -m pip install torch_geometric==2.6.1 \
  -i "${PYPI_TUNA}" --trusted-host pypi.tuna.tsinghua.edu.cn
python -m pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv \
  -f "${PYG_WHL}" \
  -i "${PYPI_TUNA}" --trusted-host pypi.tuna.tsinghua.edu.cn

echo "[setup] remaining GCTD pins"
python -m pip install \
  -i "${PYPI_TUNA}" --trusted-host pypi.tuna.tsinghua.edu.cn \
  "numpy<2" \
  scipy==1.13.1 \
  scikit-learn==1.6.1 \
  dotmap==1.3.30 \
  gdown==5.2.0 \
  ogb==1.3.6 \
  tensorly==0.9.0 \
  wandb==0.19.6 \
  faiss-cpu==1.9.0

python - <<'PY'
import torch, torch_geometric, sklearn, scipy, faiss, tensorly
print("python ok")
print("torch", torch.__version__, "cuda", torch.version.cuda, "avail", torch.cuda.is_available())
if torch.cuda.is_available():
    print("gpu", torch.cuda.get_device_name(0))
print("pyg", torch_geometric.__version__)
print("sklearn", sklearn.__version__)
print("scipy", scipy.__version__)
print("faiss", getattr(faiss, "__version__", "ok"))
print("tensorly", tensorly.__version__)
x = torch.zeros(1, device="cuda" if torch.cuda.is_available() else "cpu")
print("tensor", x.device)
PY
