#!/usr/bin/env bash
# 12 stem_gnn 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=stem_gnn id=12 FULL=${FULL:-0}"
echo "[full] 对照：先 finetune Cora 节点任务；预训练 `pretrain.py --pretrain_dataset all` 很重，有 ckpt 则跳过"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_stem_gnn_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
python STEM-GNN/finetune.py --use_params --finetune_dataset cora --gpu 0
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_stem_gnn.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/stem_gnn"
cat <<'EOF'
python STEM-GNN/finetune.py --use_params --finetune_dataset cora --gpu 0
EOF
echo "[full] 请按 README 逐条调用 run_stem_gnn.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
