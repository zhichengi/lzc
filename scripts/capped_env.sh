# 服务器资源上限：CPU / 内存 / GPU 显存均不超过 85%。
# 用法: source scripts/capped_env.sh
# 随后用 scripts/run_capped.sh COMMAND... 启动任务。
#
# 无法改 nvidia-smi 功耗/频率（需要 root），因此 GPU 侧用：
#   1) 显存 fraction=0.85
#   2) 同一时刻只跑一个训练进程
#   3) CPUQuota=85%×核数，避免 CPU 打满拖高整机利用率

_REPRO_NCORES="$(nproc --all)"
_REPRO_MEM_KB="$(awk '/MemTotal/ {print $2}' /proc/meminfo)"

export REPRO_CAP_RATIO=85
export REPRO_CAP_THREADS="$(( _REPRO_NCORES * REPRO_CAP_RATIO / 100 ))"
export REPRO_CAP_CPU_QUOTA="$(( _REPRO_NCORES * REPRO_CAP_RATIO ))%"
export REPRO_CAP_MEMORY_MAX="$(( _REPRO_MEM_KB * REPRO_CAP_RATIO / 100 * 1024 ))"
export REPRO_CAP_CUDA_FRACTION=0.85

export OMP_NUM_THREADS="${REPRO_CAP_THREADS}"
export MKL_NUM_THREADS="${REPRO_CAP_THREADS}"
export OPENBLAS_NUM_THREADS="${REPRO_CAP_THREADS}"
export NUMEXPR_NUM_THREADS="${REPRO_CAP_THREADS}"
export TORCH_NUM_THREADS="${REPRO_CAP_THREADS}"
export GOMP_CPU_AFFINITY="0-$(( REPRO_CAP_THREADS - 1 ))"

# GPU 计算占用：用户态 CUDA MPS，限制活动线程百分比为 85%。
# nvidia-smi -pl / -lgc 需要 root，本机无权限，不能用功耗/频率硬封顶。
export CUDA_MPS_PIPE_DIRECTORY="${CUDA_MPS_PIPE_DIRECTORY:-/tmp/nvidia-mps}"
export CUDA_MPS_LOG_DIRECTORY="${CUDA_MPS_LOG_DIRECTORY:-/tmp/nvidia-log}"
export CUDA_MPS_ACTIVE_THREAD_PERCENTAGE="${REPRO_CAP_RATIO}"
mkdir -p "${CUDA_MPS_PIPE_DIRECTORY}" "${CUDA_MPS_LOG_DIRECTORY}"
if ! echo get_default_active_thread_percentage | nvidia-cuda-mps-control >/dev/null 2>&1; then
    nvidia-cuda-mps-control -d >/dev/null 2>&1 || true
fi
echo set_default_active_thread_percentage "${REPRO_CAP_RATIO}" | nvidia-cuda-mps-control >/dev/null 2>&1 || true

_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${_HERE}${PYTHONPATH:+:${PYTHONPATH}}"
export PYTHONUNBUFFERED=1
