#!/usr/bin/env bash
# 15 scalegnn 单次运行入口（独立于其它论文）。
# 用法: bash repro/run_scalegnn.sh LABEL -- CMD...
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -lt 1 ]]; then
  echo "用法: $0 LABEL -- command..." >&2
  exit 2
fi
LABEL="$1"; shift
[[ "${1:-}" == "--" ]] && shift

if [[ $# -lt 1 ]]; then
  echo "缺少命令。示例见 repro/SCALEGNN_README.md" >&2
  exit 2
fi
exec bash "${ROOT}/scripts/repro_wrap.sh" \
  --paper scalegnn --env dtgb --repo repro/scalegnn --cwd repro/scalegnn --label "${LABEL}" -- "$@"
