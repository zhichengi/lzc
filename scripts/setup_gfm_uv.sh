#!/usr/bin/env bash
# FairEval GFM 使用 uv + Python 3.12.9，不能并进 dtgb。
# 本脚本只打印步骤，不自动 uv sync（会拉 torch 2.4 / dgl 2.4）。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cat <<EOF
[setup-gfm] 在准备跑 08 FairEval 时手动执行：
  curl -LsSf https://astral.sh/uv/install.sh | sh
  cd ${ROOT}/repro/fair_eval_gfm
  uv sync --managed-python
  # 数据：Zenodo GraphLand https://zenodo.org/records/16895532
  ln -s /path/to/graphland data
不要把 uv 的包装进 dtgb / ignn / gctd。
EOF
