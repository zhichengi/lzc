#!/usr/bin/env bash
# 顺序运行多个 SGPC 数据集，每个都走 repro/run_sgpc.sh（独立日志）。
# 用法: bash repro/run_sgpc_batch.sh LABEL ID [ID ...] [-- main.py 其他参数]
#   例: bash repro/run_sgpc_batch.sh official 0 1 6 7 8
set -uo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -lt 2 ]]; then
  echo "用法: $0 LABEL ID [ID ...] [-- extra args]" >&2
  exit 2
fi
LABEL="$1"; shift
IDS=()
while [[ $# -gt 0 && "$1" != "--" ]]; do IDS+=("$1"); shift; done
[[ "${1:-}" == "--" ]] && shift
for id in "${IDS[@]}"; do
  echo "[batch] === data_id=${id} $(date --iso-8601=seconds)"
  bash "${ROOT_DIR}/repro/run_sgpc.sh" "${LABEL}" "${id}" "$@" | rg "^\[repro\]|Early stopping" || true
done
echo "[batch] done $(date --iso-8601=seconds)"
