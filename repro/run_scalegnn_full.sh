#!/usr/bin/env bash
# 15 scalegnn 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=scalegnn id=15 FULL=${FULL:-0}"
echo "[full] 对照：Cora/Citeseer/Pubmed 小图；主表 ogbn-arxiv（约 1 小时 / 10 seed）。papers100M 仅 memmap 路径。"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_scalegnn_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
python main.py --config config_cora.yaml
python ogb_precompute_train.py --config config_arxiv.yaml
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_scalegnn.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/scalegnn"
cat <<'EOF'
python main.py --config config_cora.yaml
python ogb_precompute_train.py --config config_arxiv.yaml
EOF
echo "[full] 请按 README 逐条调用 run_scalegnn.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
