#!/usr/bin/env bash
# 04 mf_gia 数据准备（独立目录）。GitHub 走 ghfast.top。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "[data] paper=mf_gia"
echo "按 README 组织 datasets/；OFA 原始文件来自 https://github.com/LechengKong/OneForAll"
echo "实现按 README 补齐；不要写到其它论文的 data/ 目录。"
