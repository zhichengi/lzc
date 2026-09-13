#!/usr/bin/env bash
# 在已激活的 conda 环境中安装 GCTD 复现所需的「官方缺的」包。
# 默认不降级 dtgb 里已有的 torch / pyg。
set -euo pipefail
cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python}"

"$PYTHON" -m pip install --upgrade-strategy only-if-needed \
  -i https://pypi.tuna.tsinghua.edu.cn/simple \
  --trusted-host pypi.tuna.tsinghua.edu.cn \
  -r repro/requirements-gctd.txt

"$PYTHON" - <<'PY'
import faiss, tensorly, wandb, dotmap, torch, torch_geometric
print("faiss", getattr(faiss, "__version__", "ok"))
print("tensorly", tensorly.__version__)
print("wandb", wandb.__version__)
print("torch", torch.__version__, "cuda", torch.cuda.is_available())
print("torch_geometric", torch_geometric.__version__)
print("gctd extra deps ok")
PY
