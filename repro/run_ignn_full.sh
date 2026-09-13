#!/usr/bin/env bash
# IGNN custom split 全量入口（包装已有 dry-run 脚本）。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=ignn custom FULL=${FULL:-0}"
echo "预检: bash repro/run_ignn_custom_cignn.sh"
echo "烟雾: IGNN_EXECUTE=1 IGNN_SMOKE_ONLY=1 bash repro/run_ignn_custom_cignn.sh"
echo "全量: IGNN_EXECUTE=1 bash repro/run_ignn_custom_cignn.sh"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。不改已冻结的 public 表。"
  exit 0
fi
IGNN_EXECUTE=1 bash repro/run_ignn_custom_cignn.sh
