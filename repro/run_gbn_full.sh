#!/usr/bin/env bash
# 09 gbn 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=gbn id=09 FULL=${FULL:-0}"
echo "[full] 对照：节点分类（WikiCS / Texas 等）与深层 GCN 对照；仓库预置 configs/NC/CS.json"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_gbn_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
bash repro/run_gbn.sh official_cs -- --task NC --dataset CS
bash repro/run_gbn.sh official_texas -- --task NC --dataset Texas
# Transfer 任务：python main.py --task Transfer --dataset line
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_gbn.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/gbn"
cat <<'EOF'
bash repro/run_gbn.sh official_cs -- --task NC --dataset CS
bash repro/run_gbn.sh official_texas -- --task NC --dataset Texas
# Transfer 任务：python main.py --task Transfer --dataset line
EOF
echo "[full] 请按 README 逐条调用 run_gbn.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
