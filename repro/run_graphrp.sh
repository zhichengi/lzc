#!/usr/bin/env bash
# 23 graphrp 单次运行入口（独立于其它论文）。
# 用法: bash repro/run_graphrp.sh LABEL -- CMD...
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -lt 1 ]]; then
  echo "用法: $0 LABEL -- command..." >&2
  exit 2
fi
LABEL="$1"; shift
[[ "${1:-}" == "--" ]] && shift

echo "[run] 仓库无源码，拒绝启动。" >&2
exit 3

if [[ $# -lt 1 ]]; then
  echo "缺少命令。示例见 repro/GRAPHRP_README.md" >&2
  exit 2
fi
exec bash "${ROOT}/scripts/repro_wrap.sh" \
  --paper graphrp --env dtgb --repo repro/graphrp --cwd repro/graphrp --label "${LABEL}" -- "$@"
