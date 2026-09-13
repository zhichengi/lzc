#!/usr/bin/env bash
# SGPC 剩余全量（步骤 7 未跑完的部分）。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=sgpc FULL=${FULL:-0}"
cat <<'EOF'
# 已完成：WebKB×10；Chameleon×10；Squirrel×10；Pubmed lobpcg seed 0；Cora/Citeseer seeds 0–4。
# 待跑（串行、85% 限额）：
bash repro/run_sgpc_splits.sh webkb_s0 5          # Actor 10 划分（约 3 小时）
EOF
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。FULL=1 才会开训。"
  exit 0
fi
bash repro/run_sgpc_splits.sh webkb_s0 5
