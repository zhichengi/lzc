#!/usr/bin/env bash
# 通用外层：固定 conda、cwd、85% 限额、提交哈希与文本日志。
# 不包含任何论文算法逻辑。
# 用法:
#   bash scripts/repro_wrap.sh --paper NAME --env ENV --repo RELPATH --cwd RELPATH --label LABEL -- python ...
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONDA_HOME="${CONDA_HOME:-/home/lab_user/tools/miniconda3}"

PAPER="" ENV_NAME="dtgb" REPO_REL="" CWD_REL="" LABEL=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --paper) PAPER="$2"; shift 2 ;;
    --env) ENV_NAME="$2"; shift 2 ;;
    --repo) REPO_REL="$2"; shift 2 ;;
    --cwd) CWD_REL="$2"; shift 2 ;;
    --label) LABEL="$2"; shift 2 ;;
    --) shift; break ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done
if [[ -z "${PAPER}" || -z "${LABEL}" || $# -lt 1 ]]; then
  echo "用法: $0 --paper NAME --env ENV --repo repro/name --cwd repro/name --label LABEL -- CMD..." >&2
  exit 2
fi
LABEL="${LABEL//[^A-Za-z0-9._-]/_}"
REPO="${ROOT}/${REPO_REL}"
CWD="${ROOT}/${CWD_REL}"
RESULT_DIR="${ROOT}/results/${PAPER}/runs"
mkdir -p "${RESULT_DIR}"

# shellcheck disable=SC1091
source "${ROOT}/scripts/capped_env.sh"
# shellcheck disable=SC1091
source "${CONDA_HOME}/etc/profile.d/conda.sh"
if conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}"; then
  conda activate "${ENV_NAME}"
else
  echo "[wrap] conda 环境 ${ENV_NAME} 不存在。先运行对应 scripts/setup_* 或改 --env" >&2
  exit 1
fi

STAMP="$(date +%Y%m%d_%H%M%S)"
RUN_ID="${STAMP}_${LABEL}_pid$$"
LOG_FILE="${RESULT_DIR}/${RUN_ID}.log"
COMMIT="nogit"
if [[ -d "${REPO}/.git" ]]; then
  COMMIT="$(git -C "${REPO}" rev-parse HEAD)"
fi

{
  echo "[repro] paper=${PAPER}"
  echo "[repro] started_at=$(date --iso-8601=seconds)"
  echo "[repro] run_id=${RUN_ID}"
  echo "[repro] repo_commit=${COMMIT}"
  echo "[repro] env=${ENV_NAME} cwd=${CWD}"
  echo "[repro] command=$*"
  echo "[repro] resource_cap_ratio=${REPRO_CAP_RATIO:-} threads=${REPRO_CAP_THREADS:-}"
  python - <<'PY'
import platform, torch
gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"
print(f"[repro] python={platform.python_version()} torch={torch.__version__} cuda={torch.cuda.is_available()} gpu={gpu}")
PY
  START=$(date +%s)
  cd "${CWD}"
  bash "${ROOT}/scripts/run_capped.sh" "$@"
  echo "[repro] exit_code=$?"
  echo "[repro] runtime_seconds=$(( $(date +%s) - START ))"
  echo "[repro] finished_at=$(date --iso-8601=seconds)"
} 2>&1 | tee -a "${LOG_FILE}"
echo "[repro] log_file=${LOG_FILE}"
