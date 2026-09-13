#!/usr/bin/env bash
# 在已激活的 conda 环境中安装本仓库依赖（Python 3.10 + torch 2.2.1+cu121）。
set -euo pipefail
cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python}"

"$PYTHON" -m pip install --upgrade-strategy only-if-needed \
  torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 \
  --index-url https://download.pytorch.org/whl/cu121

"$PYTHON" -m pip install --upgrade-strategy only-if-needed \
  pyg_lib==0.4.0+pt22cu121 \
  torch_scatter==2.1.2+pt22cu121 \
  torch_sparse==0.6.18+pt22cu121 \
  torch_cluster==1.6.3+pt22cu121 \
  torch_spline_conv==1.2.2+pt22cu121 \
  -f https://data.pyg.org/whl/torch-2.2.0+cu121.html

"$PYTHON" -m pip install --upgrade-strategy only-if-needed \
  dgl==2.2.1+cu121 \
  -f https://data.dgl.ai/wheels/torch-2.2/cu121/repo.html

"$PYTHON" -m pip install --upgrade-strategy only-if-needed \
  numpy==1.26.4 \
  scikit-learn==1.4.1.post1 \
  PyYAML==6.0.1 \
  tensorboard==2.21.0 \
  torchdata==0.7.1 \
  pydantic==2.13.5 \
  torch_geometric==2.8.0.post1

"$PYTHON" - <<'PY'
import torch, torch_geometric, dgl
assert torch.cuda.is_available(), "CUDA 不可用"
print("torch", torch.__version__, torch.cuda.get_device_name(0))
print("torch_geometric", torch_geometric.__version__)
print("dgl", dgl.__version__)
print("setup ok")
PY
