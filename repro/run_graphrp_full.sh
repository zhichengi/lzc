#!/usr/bin/env bash
# 23 graphrp 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=graphrp id=23 FULL=${FULL:-0}"
echo "[full] 对照：MUTAG / ENZYMES 等图分类上的 clone acc ↓ 与 benign acc ↑。与 41 二选一全量。"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_graphrp_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
echo BLOCKED no source
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_graphrp.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/graphrp"
cat <<'EOF'
echo BLOCKED no source
EOF
echo "[full] 请按 README 逐条调用 run_graphrp.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
