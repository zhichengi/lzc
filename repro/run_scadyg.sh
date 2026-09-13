#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_DIR="${ROOT_DIR}/repro/scadyg"
RESULT_DIR="${ROOT_DIR}/results/scadyg/runs"
CHECKPOINT_ROOT="${ROOT_DIR}/results/scadyg/checkpoints"
PROTOCOL_DIR="${ROOT_DIR}/results/scadyg/protocols"
EVAL_MANIFEST="${PROTOCOL_DIR}/mooc_full_item_v1.npz"
CONDA_HOME="${CONDA_HOME:-/home/lab_user/tools/miniconda3}"
ENV_NAME="${SCADYG_CONDA_ENV:-scadyg}"
GPU_ID="${SCADYG_GPU:-0}"
DATASET="${1:-mooc}"
if [[ $# -gt 0 ]]; then
  shift
fi

if [[ ! -d "${REPO_DIR}" ]]; then
  echo "找不到官方仓库: ${REPO_DIR}" >&2
  exit 1
fi
if [[ ! -f "${CONDA_HOME}/etc/profile.d/conda.sh" ]]; then
  echo "找不到 conda: ${CONDA_HOME}" >&2
  exit 1
fi

source "${CONDA_HOME}/etc/profile.d/conda.sh"
if ! conda env list | awk -v name="${ENV_NAME}" '$1 == name {found=1} END {exit !found}'; then
  echo "找不到 conda 环境 ${ENV_NAME}，请先运行 scripts/setup_scadyg_conda.sh" >&2
  exit 1
fi
conda activate "${ENV_NAME}"

mkdir -p "${RESULT_DIR}" "${CHECKPOINT_ROOT}" "${PROTOCOL_DIR}" "${REPO_DIR}/weights"
if [[ "${DATASET}" == "mooc" && ! -f "${EVAL_MANIFEST}" ]]; then
  python "${ROOT_DIR}/scripts/build_scadyg_mooc_protocol.py" \
    --edge-index-dir "${REPO_DIR}/dataset/mooc/edge_index" \
    --output "${EVAL_MANIFEST}"
fi
STAMP="$(date +%Y%m%d_%H%M%S)"
RUN_ID="${STAMP}_${DATASET}_pid$$"
LOG_FILE="${RESULT_DIR}/${RUN_ID}.log"
CHECKPOINT_DIR="${CHECKPOINT_ROOT}/${RUN_ID}"

cd "${REPO_DIR}"
REPO_COMMIT="$(git rev-parse HEAD)"
{
  echo "[repro] started_at=$(date --iso-8601=seconds)"
  echo "[repro] run_id=${RUN_ID}"
  echo "[repro] repo_commit=${REPO_COMMIT}"
  if git diff --quiet; then
    echo "[repro] tracked_patch=none"
  else
    echo "[repro] tracked_patch_sha256=$(git diff --no-ext-diff | sha256sum | awk '{print $1}')"
    git diff --stat --no-ext-diff | awk '{print "[repro] patch_stat=" $0}'
  fi
  for source_file in \
    "${REPO_DIR}/scalable_tgn_link_prediction.py" \
    "${REPO_DIR}/scalable_tgn_main_link_prediction.py" \
    "${REPO_DIR}/model/eval_protocols.py" \
    "${ROOT_DIR}/scripts/build_scadyg_mooc_protocol.py" \
    "${ROOT_DIR}/repro/run_scadyg.sh"; do
    if [[ -f "${source_file}" ]]; then
      echo "[repro] source_sha256=$(sha256sum "${source_file}" | awk '{print $1}') path=${source_file#${ROOT_DIR}/}"
    fi
  done
  echo "[repro] dataset=${DATASET} gpu=${GPU_ID} env=${ENV_NAME}"
  echo "[repro] eval_manifest=${EVAL_MANIFEST}"
  echo "[repro] eval_manifest_sha256=$(sha256sum "${EVAL_MANIFEST}" | awk '{print $1}')"
  echo "[repro] checkpoint_dir=${CHECKPOINT_DIR}"
  echo "[repro] command=python scalable_tgn_main_link_prediction.py --dataset ${DATASET} --cuda_device ${GPU_ID} --eval_manifest ${EVAL_MANIFEST} --checkpoint_dir ${CHECKPOINT_DIR} --repo_commit ${REPO_COMMIT} $*"
  python - <<'PY'
import dgl
import torch
import torch_geometric

print(f"[repro] torch={torch.__version__} pyg={torch_geometric.__version__} dgl={dgl.__version__}")
print(f"[repro] cuda={torch.cuda.is_available()} gpu_count={torch.cuda.device_count()}")
if torch.cuda.is_available():
    print(f"[repro] gpu_name={torch.cuda.get_device_name(0)}")
PY
  python scalable_tgn_main_link_prediction.py \
    --dataset "${DATASET}" \
    --cuda_device "${GPU_ID}" \
    --eval_manifest "${EVAL_MANIFEST}" \
    --checkpoint_dir "${CHECKPOINT_DIR}" \
    --repo_commit "${REPO_COMMIT}" \
    "$@"
  echo "[repro] finished_at=$(date --iso-8601=seconds)"
} 2>&1 | tee -a "${LOG_FILE}"

echo "[repro] log_file=${LOG_FILE}"
