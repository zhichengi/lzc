#!/usr/bin/env bash
# 在 CPU 85%、内存 85% 的 systemd 用户 scope 里执行命令。
# 例: bash scripts/run_capped.sh bash repro/run_ignn.sh LABEL ...
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
source "${ROOT}/scripts/capped_env.sh"

if [[ $# -lt 1 ]]; then
    echo "用法: $0 COMMAND [ARGS...]" >&2
    exit 2
fi

echo "[cap] cores=${REPRO_CAP_THREADS}/$(nproc --all) CPUQuota=${REPRO_CAP_CPU_QUOTA} MemoryMax=${REPRO_CAP_MEMORY_MAX} cuda_fraction=${REPRO_CAP_CUDA_FRACTION} mps=${CUDA_MPS_ACTIVE_THREAD_PERCENTAGE} gpu_gov=${GPU_GOV:-1}" >&2

systemd-run --user --scope --collect \
    -p "CPUQuota=${REPRO_CAP_CPU_QUOTA}" \
    -p "MemoryMax=${REPRO_CAP_MEMORY_MAX}" \
    -p "MemoryHigh=${REPRO_CAP_MEMORY_MAX}" \
    "$@" &
sr_pid=$!
gov_pid=""
if [[ "${GPU_GOV:-1}" != "0" ]]; then
    (
        target=""
        for _ in $(seq 1 50); do
            target="$(pgrep -P "${sr_pid}" | head -n 1 || true)"
            if [[ -n "${target}" ]]; then
                break
            fi
            if [[ -d "/proc/${sr_pid}" ]] && grep -q python "/proc/${sr_pid}/comm" 2>/dev/null; then
                target="${sr_pid}"
                break
            fi
            sleep 0.1
        done
        if [[ -n "${target}" ]]; then
            exec bash "${ROOT}/scripts/gpu_util_governor.sh" "${target}" "${REPRO_CAP_RATIO}"
        fi
    ) &
    gov_pid=$!
fi
wait "${sr_pid}"
status=$?
if [[ -n "${gov_pid}" ]]; then
    kill "${gov_pid}" 2>/dev/null || true
    wait "${gov_pid}" 2>/dev/null || true
fi
exit "${status}"
