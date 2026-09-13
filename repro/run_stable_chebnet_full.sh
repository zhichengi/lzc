#!/usr/bin/env bash
# 10 stable_chebnet 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=stable_chebnet id=10 FULL=${FULL:-0}"
echo "[full] 对照：Peptides-func / Peptides-struct（LRGB）；Barbell 与 GraphProp 为合成/属性任务"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_stable_chebnet_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
cd repro/stable_chebnet/Peptides/Stable
python ChebStable_peptide.py
python ChebStable_Struc.py
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_stable_chebnet.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/stable_chebnet"
cat <<'EOF'
cd repro/stable_chebnet/Peptides/Stable
python ChebStable_peptide.py
python ChebStable_Struc.py
EOF
echo "[full] 请按 README 逐条调用 run_stable_chebnet.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
