#!/usr/bin/env bash
# 22 core_graphrag 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=core_graphrag id=22 FULL=${FULL:-0}"
echo "[full] 对照：只做 k-core 层次 / RkH·M2hC·MRC vs Leiden 的算法可复现性；LLM 查询不做"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_core_graphrag_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
echo '算法全量：在无 API 条件下对比 Leiden vs RkH 的社区划分可复现性（见笔记）；query 等预算'
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_core_graphrag.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/core_graphrag"
cat <<'EOF'
echo '算法全量：在无 API 条件下对比 Leiden vs RkH 的社区划分可复现性（见笔记）；query 等预算'
EOF
echo "[full] 请按 README 逐条调用 run_core_graphrag.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
