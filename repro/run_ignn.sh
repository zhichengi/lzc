#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/home/lab_user/project/lzc"
REPO="${ROOT}/repro/ignn"
ENV_DIR="/home/lab_user/tools/miniconda3/envs/ignn"
PYTHON="${ENV_DIR}/bin/python"
RUN_ROOT="${ROOT}/results/ignn/runs"

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 LABEL MAIN_ARGUMENTS..." >&2
    exit 2
fi

LABEL="${1//[^A-Za-z0-9._-]/_}"
shift

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="${RUN_ROOT}/${STAMP}_${LABEL}"
if [[ -e "${RUN_DIR}" ]]; then
    RUN_DIR="${RUN_DIR}_$$"
fi
mkdir -p "${RUN_DIR}"

LOG_FILE="${RUN_DIR}/run.log"
META_FILE="${RUN_DIR}/metadata.txt"
COMMAND_FILE="${RUN_DIR}/command.txt"

export LD_LIBRARY_PATH="${ENV_DIR}/lib:${ENV_DIR}/lib/python3.8/site-packages/torch/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
export PYTHONUNBUFFERED=1

printf '%q ' "${PYTHON}" -u -m main "$@" >"${COMMAND_FILE}"
printf '\n' >>"${COMMAND_FILE}"

{
    echo "run_id=$(basename "${RUN_DIR}")"
    echo "started_utc=$(date -u --iso-8601=seconds)"
    echo "host=$(hostname)"
    echo "repo=${REPO}"
    echo "commit=$(git -C "${REPO}" rev-parse HEAD)"
    echo "branch=$(git -C "${REPO}" branch --show-current)"
    echo "python=${PYTHON}"
    echo "ld_library_path=${LD_LIBRARY_PATH}"
    uname -a
    nvidia-smi --query-gpu=index,name,driver_version,memory.total --format=csv,noheader
    "${PYTHON}" - <<'PY'
import importlib.metadata as metadata
import platform
import torch

packages = (
    "torch",
    "torchvision",
    "torchaudio",
    "torch-geometric",
    "torch-scatter",
    "torch-sparse",
    "dgl",
    "graph-datasets",
    "the-utils",
    "ogb",
)
print(f"python_version={platform.python_version()}")
print(f"torch_cuda={torch.version.cuda}")
print(f"cuda_available={torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"gpu_name={torch.cuda.get_device_name(0)}")
for package in packages:
    print(f"{package}={metadata.version(package)}")
PY
    echo "source_status_begin"
    git -C "${REPO}" status --short
    echo "source_status_end"
    echo -n "command="
    cat "${COMMAND_FILE}"
} >"${META_FILE}"

on_exit() {
    status=$?
    {
        echo
        echo "finished_utc=$(date -u --iso-8601=seconds)"
        echo "exit_code=${status}"
    } | tee -a "${META_FILE}" "${LOG_FILE}"
}
trap on_exit EXIT

{
    echo "run_dir=${RUN_DIR}"
    echo "started_utc=$(date -u --iso-8601=seconds)"
    echo -n "command="
    cat "${COMMAND_FILE}"
} | tee -a "${LOG_FILE}"

cd "${REPO}"
"${PYTHON}" -u -m main "$@" 2>&1 | tee -a "${LOG_FILE}"
