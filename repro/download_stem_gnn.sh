#!/usr/bin/env bash
# 12 stem_gnn 数据准备（独立目录）。GitHub 走 ghfast.top。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "[data] paper=stem_gnn"
echo "Cora 等放 `repro/stem_gnn/STEM-GNN/data/`。"
echo "实现按 README 补齐；不要写到其它论文的 data/ 目录。"
