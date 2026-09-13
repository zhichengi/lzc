#!/usr/bin/env bash
# ScaDyG 收尾全量：消融 + BitcoinAlpha。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=scadyg FULL=${FULL:-0}"
cat <<'EOF'
# 具体消融开关与 BitcoinAlpha 数据路径见 SCADYG_README.md / CLOSEOUT_PLAN.md R-SCADYG-*
# 入口沿用：
bash repro/run_scadyg.sh LABEL ...
bash repro/run_scadyg_multiseed.sh ...
# 不要与 SGPC / GBN 同时占 GPU。
EOF
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。全量命令需对照 SCADYG_README 填 LABEL；本脚本不静默开训。"
  exit 0
fi
echo "[full] 请按 SCADYG_README 逐条调用 run_scadyg.sh" >&2
exit 2
