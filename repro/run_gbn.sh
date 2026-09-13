#!/usr/bin/env bash
# 09 gbn 单次运行入口（独立于其它论文）。
# 用法: bash repro/run_gbn.sh LABEL -- CMD...
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -lt 1 ]]; then
  echo "用法: $0 LABEL -- command..." >&2
  exit 2
fi
LABEL="$1"; shift
[[ "${1:-}" == "--" ]] && shift

if [[ $# -lt 1 ]]; then
  echo "缺少命令。示例见 repro/GBN_README.md" >&2
  exit 2
fi
exec bash "${ROOT}/scripts/repro_wrap.sh" \
  --paper gbn --env dtgb --repo repro/gbn --cwd repro/gbn --label "${LABEL}" -- "$@"
