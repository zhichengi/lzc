#!/usr/bin/env bash
# 13 mavn 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=mavn id=13 FULL=${FULL:-0}"
echo "[full] 对照：Peptides-func AP（seed 0–3）；PascalVOC-SP；minesweeper / tolokers 10 split。附录 PDF：Setup_MAVN_KDD2026.pdf"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_mavn_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
见 README Peptides-func 四 seed 命令；在 code/ 下执行。
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_mavn.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/mavn/code"
cat <<'EOF'
见 README Peptides-func 四 seed 命令；在 code/ 下执行。
EOF
echo "[full] 请按 README 逐条调用 run_mavn.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
