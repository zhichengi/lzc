#!/usr/bin/env bash
# R-GCTD-3：用 GCTD 评测链路跑 GCond 官方压缩图（外部对照）。
#
# 依赖 GCond 官方克隆自带的 saved_ours/*.pt（论文 Table 2 的原始产物）：
#   repro/gcond/saved_ours/{adj,feat}_<dataset>_<r>_<seed>.pt
# 压缩比换算（GCond 的 r 相对训练标签数，不是全图）：
#   cora      r=0.25  -> 论文 1.3%
#   citeseer  r=0.25  -> 论文 1.8%
#
# 用法:
#   bash repro/run_gcond_eval.sh                 # cora + citeseer，5 seed，两种选模
#   bash repro/run_gcond_eval.sh cora            # 只跑 cora
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

DATASETS=("$@")
if [[ ${#DATASETS[@]} -eq 0 ]]; then
  DATASETS=(cora citeseer)
fi

OUT_DIR="${ROOT}/results/gctd"
mkdir -p "${OUT_DIR}"
STAMP="$(date +%Y%m%d_%H%M%S)"
BATCH="${OUT_DIR}/runs/${STAMP}_gcond_official_eval.batch.log"
mkdir -p "${OUT_DIR}/runs"
: > "${BATCH}"

if command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
  conda activate gctd
fi

echo "[gcond] datasets=${DATASETS[*]} $(date --iso-8601=seconds)" | tee -a "${BATCH}"

for ds in "${DATASETS[@]}"; do
  case "${ds}" in
    cora)     RATE=0.25; PAPER="79.8 ± 1.3" ;;   # 论文 Table 2 的 GCond 列
    citeseer) RATE=0.25; PAPER="70.5 ± 1.2" ;;   # 注意：76.5 是 GCTD 列，不是 GCond
    pubmed)   RATE=0.5;  PAPER="78.3 ± 0.2" ;;   # saved_ours 无 pubmed，仅占位
    *) echo "[gcond] unknown dataset ${ds}" | tee -a "${BATCH}"; continue ;;
  esac
  for sel in val_loss val_acc; do
    CSV="${OUT_DIR}/gcond_official_${ds}_${RATE}_${sel}.csv"
    echo "=== ${ds} r=${RATE} select=${sel} paper=${PAPER} $(date +%H:%M:%S) ===" | tee -a "${BATCH}"
    python scripts/gcond_eval_official.py \
      --dataset "${ds}" --rate "${RATE}" --paper-value "${PAPER}" \
      --seeds "0 1 2 3 4" --select "${sel}" --epochs 600 \
      --csv "${CSV}" 2>&1 | tee -a "${BATCH}"
    echo "exit=$?" | tee -a "${BATCH}"
  done
done

echo "[gcond] done $(date --iso-8601=seconds)" | tee -a "${BATCH}"
echo "[gcond] batch log: ${BATCH}"
