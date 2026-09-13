#!/usr/bin/env bash
# 用 SIGSTOP/SIGCONT 把目标进程的 GPU 忙时压到上限以下。
# MPS 的 active_thread_percentage 对 nvidia-smi GPU-Util/SM% 几乎无影响
#（卡在忙就接近 100%），功耗上限又需要 root，因此用占空比限制。
# 用法: bash scripts/gpu_util_governor.sh PID [MAX_UTIL]
set -euo pipefail
PID="${1:?pid}"
MAX_UTIL="${2:-85}"
RUN_S="${GPU_GOV_RUN_S:-0.82}"
STOP_S="${GPU_GOV_STOP_S:-0.15}"

while kill -0 "${PID}" 2>/dev/null; do
    kill -STOP "${PID}" 2>/dev/null || exit 0
    sleep "${STOP_S}"
    kill -CONT "${PID}" 2>/dev/null || exit 0
    sleep "${RUN_S}"
done
