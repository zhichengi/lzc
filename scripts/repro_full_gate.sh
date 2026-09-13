#!/usr/bin/env bash
# 全量启动的 dry-run 外壳。FULL=1 时才真正训练。
# 用法: bash scripts/repro_full_gate.sh PAPER <<'EOF'
# 将要执行的命令（每行一条）
# EOF
set -euo pipefail
PAPER="${1:?paper name}"
shift || true
echo "[full] paper=${PAPER} FULL=${FULL:-0} $(date --iso-8601=seconds)"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认命令后执行: FULL=1 bash $0 ${PAPER}"
  echo "[full] 将要运行:"
  cat
  exit 0
fi
bash -s
