#!/usr/bin/env bash
# SGPC（AAAI 2026）官方 main.py 的外层入口。
# 官方代码把数据根目录写死为 /tmp/<Name>，且无 seed / 无 CLI 超参；本脚本只负责：
#   1) 用符号链接把 /tmp/<Name> 指到 repro/sgpc/data/<Name>（由 download_sgpc_data.py 预下载）
#   2) 固定 conda 环境与 GPU
#   3) 把提交哈希、补丁哈希、环境版本、完整命令和 stdout 写到 results/sgpc/runs/<时间戳>_<label>.log
# 用法: bash repro/run_sgpc.sh LABEL DATA_ID [main.py 的其他参数...]
#   例: bash repro/run_sgpc.sh official_cornell 6
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_DIR="${ROOT_DIR}/repro/sgpc"
DATA_DIR="${REPO_DIR}/data"
RESULT_DIR="${ROOT_DIR}/results/sgpc/runs"
CONDA_HOME="${CONDA_HOME:-/home/lab_user/tools/miniconda3}"
ENV_NAME="${SGPC_CONDA_ENV:-dtgb}"
export CUDA_VISIBLE_DEVICES="${SGPC_GPU:-0}"

if [[ $# -lt 2 ]]; then
  echo "用法: $0 LABEL DATA_ID [extra args]" >&2
  exit 2
fi
LABEL="${1//[^A-Za-z0-9._-]/_}"
DATA_ID="$2"
shift 2

NAMES=(Cora Citeseer Pubmed Chameleon Squirrel Actor Cornell Texas Wisconsin)
if ! [[ "${DATA_ID}" =~ ^[0-8]$ ]]; then
  echo "DATA_ID 必须是 0-8" >&2
  exit 2
fi
NAME="${NAMES[${DATA_ID}]}"

# shellcheck disable=SC1091
source "${ROOT_DIR}/scripts/capped_env.sh"
source "${CONDA_HOME}/etc/profile.d/conda.sh"
conda activate "${ENV_NAME}"

# 官方 root='/tmp/<Name>'；预下载目录必须存在
if [[ ! -d "${DATA_DIR}/${NAME}" ]]; then
  echo "缺少 ${DATA_DIR}/${NAME}，先运行: python repro/download_sgpc_data.py ${DATA_ID}" >&2
  exit 1
fi
if [[ -e "/tmp/${NAME}" && ! -L "/tmp/${NAME}" ]]; then
  echo "/tmp/${NAME} 已存在且不是符号链接，拒绝覆盖" >&2
  exit 1
fi
ln -sfn "${DATA_DIR}/${NAME}" "/tmp/${NAME}"

mkdir -p "${RESULT_DIR}"
STAMP="$(date +%Y%m%d_%H%M%S)"
RUN_ID="${STAMP}_${LABEL}_${NAME}_pid$$"
LOG_FILE="${RESULT_DIR}/${RUN_ID}.log"

cd "${REPO_DIR}"
REPO_COMMIT="$(git rev-parse HEAD)"
{
  echo "[repro] started_at=$(date --iso-8601=seconds)"
  echo "[repro] run_id=${RUN_ID}"
  echo "[repro] repo_commit=${REPO_COMMIT}"
  if git diff --quiet -- main.py; then
    echo "[repro] tracked_patch=none"
  else
    echo "[repro] tracked_patch_sha256=$(git diff --no-ext-diff -- main.py | sha256sum | awk '{print $1}')"
  fi
  echo "[repro] main_py_sha256=$(sha256sum main.py | awk '{print $1}')"
  echo "[repro] dataset=${NAME} data_id=${DATA_ID} env=${ENV_NAME} cuda_visible_devices=${CUDA_VISIBLE_DEVICES}"
  echo "[repro] data_link=/tmp/${NAME} -> $(readlink -f "/tmp/${NAME}")"
  echo "[repro] command=python main.py ${DATA_ID} $*"
  echo "[repro] resource_cap_ratio=${REPRO_CAP_RATIO} threads=${REPRO_CAP_THREADS} CPUQuota=${REPRO_CAP_CPU_QUOTA} MemoryMax=${REPRO_CAP_MEMORY_MAX} cuda_fraction=${REPRO_CAP_CUDA_FRACTION}"
  python - <<'PY'
import torch, torch_geometric, torch_sparse
print(f"[repro] python={__import__('platform').python_version()} torch={torch.__version__} pyg={torch_geometric.__version__} torch_sparse={torch_sparse.__version__}")
print(f"[repro] cuda={torch.cuda.is_available()} gpu={torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu'}")
PY
  START=$(date +%s)
  set +e
  bash "${ROOT_DIR}/scripts/run_capped.sh" python main.py "${DATA_ID}" "$@"
  EC=$?
  set -e
  echo "[repro] exit_code=${EC}"
  echo "[repro] runtime_seconds=$(( $(date +%s) - START ))"
  echo "[repro] finished_at=$(date --iso-8601=seconds)"
} 2>&1 | tee -a "${LOG_FILE}"

echo "[repro] log_file=${LOG_FILE}"
