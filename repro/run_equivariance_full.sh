#!/usr/bin/env bash
# 01 equivariance 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=equivariance id=01 FULL=${FULL:-0}"
echo "[full] 对照：trainset1：Cora 训练、其余图测试。与 04 二选一做全量。"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_equivariance_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
python -u main.py --is_train --train_test_setup trainset1 --gnn_type MEAN_GNN --hidden_dim 16 --num_layers 2 --lp_ratio 0.4 --max_epochs 2000 --lr 0.01
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_equivariance.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/equivariance"
cat <<'EOF'
python -u main.py --is_train --train_test_setup trainset1 --gnn_type MEAN_GNN --hidden_dim 16 --num_layers 2 --lp_ratio 0.4 --max_epochs 2000 --lr 0.01
EOF
echo "[full] 请按 README 逐条调用 run_equivariance.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
