#!/usr/bin/env bash
# 09 GBN 消融运行器（论文 Table 4）。默认 dry-run。
#
#   bash repro/run_gbn_ablation.sh                    # 只打印计划
#   EXECUTE=1 bash repro/run_gbn_ablation.sh          # 全量（5 变体 × 4 数据集）
#   EXECUTE=1 MODES="none gamma_all0" DATASETS="Texas" bash repro/run_gbn_ablation.sh
#
# 前置：`repro/gbn-ablation.patch` 必须已应用到 `repro/gbn/`：
#   cd repro/gbn && git apply ../gbn-ablation.patch
# 该补丁新增 `ablate`（默认 `none`，与官方路径逐位一致）。未打补丁时脚本会报错退出。
#
# 配置来源：`results/gbn/configs/ablate/<mode>/<DS>.json`
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG_SRC="${ROOT}/results/gbn/configs/ablate"
CFG_DST="${ROOT}/repro/gbn/configs/NC"
REPO="${ROOT}/repro/gbn"

MODES="${MODES:-none gamma0_beta0 gamma_all0 beta_all0 gamma_beta_all0}"
DATASETS="${DATASETS:-CS WikiCS Texas Amazon-ratings}"

# 前置检查：补丁是否已应用
if ! grep -q "ablate" "${REPO}/node_classification.py" 2>/dev/null; then
  echo "[gbn-abl] 未检测到 ablate 支持。先应用补丁：" >&2
  echo "          cd repro/gbn && git apply ../gbn-ablation.patch" >&2
  exit 3
fi

echo "[gbn-abl] modes='${MODES}' datasets='${DATASETS}'"
echo "[gbn-abl] 配置源 ${CFG_SRC}/<mode>/<DS>.json"
echo
plan=()
for m in ${MODES}; do
  for ds in ${DATASETS}; do
    src="${CFG_SRC}/${m}/${ds}.json"
    if [[ ! -f "${src}" ]]; then
      echo "[gbn-abl] 缺少配置 ${src}；先跑 scripts/gen_gbn_configs.py --ablation" >&2
      exit 3
    fi
    plan+=("${m}|${ds}|${src}")
    printf '  %-16s %-16s cfg=%s\n' "${m}" "${ds}" "${src}"
  done
done
echo

if [[ "${EXECUTE:-0}" != "1" ]]; then
  echo "[gbn-abl] dry-run。确认主表已跑完、GPU 空闲后："
  echo "          EXECUTE=1 bash repro/run_gbn_ablation.sh"
  exit 0
fi

mkdir -p "${CFG_DST}"
STAMP="$(date +%Y%m%d_%H%M%S)"
BATCH_LOG="${ROOT}/results/gbn/runs/${STAMP}_gbn_ablation.batch.log"
echo "[gbn-abl] 批次日志 ${BATCH_LOG}"
echo "=== gbn ablation $(date --iso-8601=seconds) modes='${MODES}' datasets='${DATASETS}' ===" | tee -a "${BATCH_LOG}"

for entry in "${plan[@]}"; do
  IFS='|' read -r m ds src <<< "${entry}"
  cp "${src}" "${CFG_DST}/${ds}.json"
  label="ablate_${m}_${ds}_r10"
  echo "" | tee -a "${BATCH_LOG}"
  echo ">>> ${label}  ($(date --iso-8601=seconds))" | tee -a "${BATCH_LOG}"
  set +e
  bash "${ROOT}/repro/run_gbn.sh" "${label}" -- python main.py --task NC --dataset "${ds}" \
    2>&1 | tee -a "${BATCH_LOG}"
  rc=${PIPESTATUS[0]}
  set -e
  echo "<<< ${label} exit=${rc}" | tee -a "${BATCH_LOG}"
done

echo "" | tee -a "${BATCH_LOG}"
echo "=== gbn ablation done $(date --iso-8601=seconds) ===" | tee -a "${BATCH_LOG}"
