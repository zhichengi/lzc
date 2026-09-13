#!/usr/bin/env bash
# 04 mf_gia 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=mf_gia id=04 FULL=${FULL:-0}"
echo "[full] 对照：ICL 节点分类：Cora k-shot。预训练 8000 epoch，优先用仓库 checkpoint。"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_mf_gia_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
python run_ICL_node.py --dataset cora --k_shot 1
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_mf_gia.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/mf_gia"
cat <<'EOF'
python run_ICL_node.py --dataset cora --k_shot 1
EOF
echo "[full] 请按 README 逐条调用 run_mf_gia.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
