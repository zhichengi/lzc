#!/usr/bin/env bash
# 01 equivariance 数据准备（独立目录）。GitHub 走 ghfast.top。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "[data] paper=equivariance"
echo "脚本内下载多图节点分类基准；全量前应预下载并离线。"
echo "实现按 README 补齐；不要写到其它论文的 data/ 目录。"
