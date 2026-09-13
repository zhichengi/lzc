#!/usr/bin/env bash
# 41 unlearning_inv 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=unlearning_inv id=41 FULL=${FULL:-0}"
echo "[full] 对照：Cora 上 Inversion + GIF；README 示例 num_runs=5。与 23 二选一全量。"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_unlearning_inv_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
python main.py --dataset_name cora --target_model=GCN --exp Inversion --method GIF --unlearn_ratio 0.05 --attack_method=trend_steal --num_runs=5 --cuda 0 --is_gen_unlearn_request=True --is_gen_unlearned_probs=True
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_unlearning_inv.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/unlearning_inv"
cat <<'EOF'
python main.py --dataset_name cora --target_model=GCN --exp Inversion --method GIF --unlearn_ratio 0.05 --attack_method=trend_steal --num_runs=5 --cuda 0 --is_gen_unlearn_request=True --is_gen_unlearned_probs=True
EOF
echo "[full] 请按 README 逐条调用 run_unlearning_inv.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
