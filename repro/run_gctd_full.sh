#!/usr/bin/env bash
# GCTD 收尾全量：Citeseer / Pubmed，不再扫 Cora。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=gctd FULL=${FULL:-0}"
cat <<'EOF'
bash repro/download_planetoid.sh citeseer
bash repro/download_planetoid.sh pubmed
bash repro/run_gctd.sh citeseer 0.013 --num_workers 0 --lr_rec 0.01 --edge_topk 12
bash repro/run_gctd.sh pubmed 0.013 --num_workers 0 --lr_rec 0.01 --edge_topk 12
# 可选 GCond 对照：同一命令加 --gcond_protocol 1 --weighted 0 --rec_proj 1
EOF
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。FULL=1 时按上面顺序执行。"
  exit 0
fi
bash repro/download_planetoid.sh citeseer
bash repro/download_planetoid.sh pubmed
bash repro/run_gctd.sh citeseer 0.013 --num_workers 0 --lr_rec 0.01 --edge_topk 12
bash repro/run_gctd.sh pubmed 0.013 --num_workers 0 --lr_rec 0.01 --edge_topk 12
