#!/usr/bin/env bash
# 22 core_graphrag 数据准备（独立目录）。GitHub 走 ghfast.top。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "[data] paper=core_graphrag"
echo "Kevin Scott podcast 等来自 GraphRAG benchmarking datasets；算法烟雾不需要语料。"
echo "实现按 README 补齐；不要写到其它论文的 data/ 目录。"
