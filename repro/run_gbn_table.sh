#!/usr/bin/env bash
# 09 GBN 节点分类主表运行器（论文 Table 3）。默认 dry-run，不训练。
#
#   bash repro/run_gbn_table.sh                      # 只打印计划
#   SMOKE=1 bash repro/run_gbn_table.sh              # 2 epoch / 1 iter 烟雾（验证+计时）
#   EXECUTE=1 bash repro/run_gbn_table.sh            # 全量（每数据集 10 iters）
#   EXECUTE=1 DATASETS="Texas Wisconsin" bash repro/run_gbn_table.sh
#   EXECUTE=1 SMOKE=1 bash repro/run_gbn_table.sh    # 显式烟雾
#
# 配置来源：`results/gbn/configs/<DS>.json`（论文 Table 8 超参，由
# `scripts/gen_gbn_configs.py` 生成）。烟雾用 `results/gbn/configs/smoke/<DS>.json`。
#
# 为什么要拷配置：`repro/gbn/main.py` 的 argparse 没有 `layer_wise`，但
# `node_classification.py:load_model` 会读它；没有 json 时会 AttributeError。
# 官方只预置了 `configs/NC/CS.json`，所以其余数据集必须由外层注入 json。
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG_SRC="${ROOT}/results/gbn/configs"
CFG_DST="${ROOT}/repro/gbn/configs/NC"

# 论文 Table 3 的 7 个数据集；Cora 为额外项（不在论文表内）
DEFAULT_DATASETS="CS WikiCS computers Roman-empire Amazon-ratings Texas Wisconsin Cora"
DATASETS="${DATASETS:-${DEFAULT_DATASETS}}"

MODE="full"
LABEL_SUFFIX="r10"
if [[ "${SMOKE:-0}" == "1" ]]; then
  MODE="smoke"
  LABEL_SUFFIX="2ep"
fi

echo "[gbn-table] mode=${MODE} datasets='${DATASETS}'"
if [[ "${MODE}" == "smoke" ]]; then
  echo "[gbn-table] 配置源 ${CFG_SRC}/smoke/<DS>.json  ->  ${CFG_DST}/<DS>.json"
else
  echo "[gbn-table] 配置源 ${CFG_SRC}/<DS>.json  ->  ${CFG_DST}/<DS>.json"
fi
echo

plan=()
for ds in ${DATASETS}; do
  if [[ "${MODE}" == "smoke" ]]; then
    SRC_JSON="${CFG_SRC}/smoke/${ds}.json"
    LABEL="smoke_${ds}_2ep"
  else
    SRC_JSON="${CFG_SRC}/${ds}.json"
    LABEL="official_${ds}_${LABEL_SUFFIX}"
  fi
  if [[ ! -f "${SRC_JSON}" ]]; then
    echo "[gbn-table] 缺少配置 ${SRC_JSON}；先跑 scripts/gen_gbn_configs.py" >&2
    exit 3
  fi
  plan+=("${ds}|${LABEL}|${SRC_JSON}")
  printf '  %-16s label=%-28s cfg=%s\n' "${ds}" "${LABEL}" "${SRC_JSON}"
done
echo

if [[ "${EXECUTE:-0}" != "1" ]]; then
  echo "[gbn-table] dry-run。确认 GPU 空闲且只跑这一篇后："
  echo "             SMOKE=1 bash repro/run_gbn_table.sh      # 先烟雾"
  echo "             EXECUTE=1 bash repro/run_gbn_table.sh    # 再全量"
  exit 0
fi

mkdir -p "${CFG_DST}"
STAMP="$(date +%Y%m%d_%H%M%S)"
BATCH_LOG="${ROOT}/results/gbn/runs/${STAMP}_gbn_table_${MODE}.batch.log"
echo "[gbn-table] 批次日志 ${BATCH_LOG}"
{
  echo "=== gbn table mode=${MODE} datasets='${DATASETS}' $(date --iso-8601=seconds) ==="
} | tee -a "${BATCH_LOG}"

for entry in "${plan[@]}"; do
  IFS='|' read -r ds label src <<< "${entry}"
  dst="${CFG_DST}/${ds}.json"
  cp "${src}" "${dst}"
  echo "" | tee -a "${BATCH_LOG}"
  echo ">>> ${label}  ($(date --iso-8601=seconds))  cfg=${src}" | tee -a "${BATCH_LOG}"
  set +e
  bash "${ROOT}/repro/run_gbn.sh" "${label}" -- python main.py --task NC --dataset "${ds}" \
    2>&1 | tee -a "${BATCH_LOG}"
  rc=${PIPESTATUS[0]}
  set -e
  echo "<<< ${label} exit=${rc}" | tee -a "${BATCH_LOG}"
done

echo "" | tee -a "${BATCH_LOG}"
echo "=== gbn table done $(date --iso-8601=seconds) ===" | tee -a "${BATCH_LOG}"
echo "[gbn-table] 官方结果文件在 repro/gbn/results/NC_<DS>.txt；外层日志在 results/gbn/runs/*${LABEL_SUFFIX}*.log"
