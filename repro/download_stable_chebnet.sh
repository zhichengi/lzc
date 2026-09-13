#!/usr/bin/env bash
# 10 stable_chebnet：Peptides-func（PyG LRGB / Dropbox）。不直连 GitHub。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/repro/stable_chebnet/Peptides/Stable"
URL="https://www.dropbox.com/s/ycsq37q8sxs1ou8/peptidesfunc.zip?dl=1"
mkdir -p "${DEST}"
if [[ -f "${DEST}/peptides-func/processed/train.pt" ]]; then
  echo "[chebnet-data] processed train.pt 已在 ${DEST}/peptides-func/processed"
  exit 0
fi
echo "[chebnet-data] PyG LRGBDataset 默认从 Dropbox 拉 peptidesfunc.zip"
echo "[chebnet-data] ${URL}"
echo "[chebnet-data] HuggingFace LRGB/peptides-functional 只有 geometric_data_processed.pt，对不上官方 LRGBDataset 的 train/val/test 分片。"
CONDA_HOME="${CONDA_HOME:-/home/lab_user/tools/miniconda3}"
# shellcheck disable=SC1091
source "${CONDA_HOME}/etc/profile.d/conda.sh"
conda activate dtgb
export CUDA_VISIBLE_DEVICES=""
python - <<PY
from torch_geometric.datasets import LRGBDataset
root = "${DEST}"
for split in ("train", "val", "test"):
    ds = LRGBDataset(root=root, name="Peptides-func", split=split)
    print(f"[chebnet-data] split={split} n={len(ds)} feats={ds.num_node_features} classes={ds.num_classes}")
PY
echo "[chebnet-data] done"
