#!/usr/bin/env bash
# 08 fair_eval_gfm 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
echo "[full] paper=fair_eval_gfm id=08 FULL=${FULL:-0}"
echo "[full] 对照：GraphLand 上的 GNN 基线；GFM 数字来自各官方仓。本仓库只用 uv 复现 GNN 部分。"
if [[ "${FULL:-0}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_fair_eval_gfm_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
uv run bin/go.py exp/cgasb/gcn/tolokers-2/evaluation.toml --n_seeds 5
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_fair_eval_gfm.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${ROOT}/repro/fair_eval_gfm"
cat <<'EOF'
uv run bin/go.py exp/cgasb/gcn/tolokers-2/evaluation.toml --n_seeds 5
EOF
echo "[full] 请按 README 逐条调用 run_fair_eval_gfm.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
