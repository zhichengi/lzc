#!/usr/bin/env bash
# 23 graphrp 数据准备（独立目录）。GitHub 走 ghfast.top。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "[data] paper=graphrp"
echo "TU 数据集（MUTAG 等），代码到位后由 PyG TUDataset 加载。"
echo "实现按 README 补齐；不要写到其它论文的 data/ 目录。"
