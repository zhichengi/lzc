#!/usr/bin/env bash
# 10 stable_chebnet：Peptides-func 数据获取（不依赖 Dropbox）。
#
# 背景：PyG 的 LRGBDataset 默认从 Dropbox 拉 peptidesfunc.zip，并期望
# raw/{train,val,test}.pt 为 (x, edge_attr, edge_index, y) 元组列表。
# 本机 Dropbox 不可达（Network is unreachable）。
#
# 替代路径（均可达，走 hf-mirror）：
#  1. LRGB/peptides-functional -> geometric_data_processed.pt
#     原始 LRGB 加载器的 processed 产物（collated Data + slices），保持 CSV 行序。
#  2. scikit-fingerprints/LRGB_Peptides-func -> lrgb_splits_peptides_func.json
#     分层随机划分索引（10,873 / 2,331 / 2,331），索引同一份 CSV。
#
# 由 repro/build_stable_chebnet_peptides.py 还原成 PyG 需要的 raw 分片。
# 来源与校验细节见 STABLE_CHEBNET_REPRO_LOG.md 步骤 3。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/repro/stable_chebnet/Peptides/Stable"
CACHE="${ROOT}/repro/stable_chebnet/data_cache"
HF_MIRROR="${HF_ENDPOINT:-https://hf-mirror.com}"
PROCESSED_URL="${HF_MIRROR}/datasets/LRGB/peptides-functional/resolve/main/geometric_data_processed.pt"
SPLITS_URL="${HF_MIRROR}/datasets/scikit-fingerprints/LRGB_Peptides-func/resolve/main/lrgb_splits_peptides_func.json"
mkdir -p "${CACHE}" "${DEST}"
if [[ -f "${DEST}/peptides-func/processed/train.pt" ]]; then
  echo "[chebnet-data] processed train.pt 已在 ${DEST}/peptides-func/processed"
  exit 0
fi
fetch() {
  local url="$1" out="$2"
  if [[ -f "${out}" ]]; then
    echo "[chebnet-data] 已缓存 $(basename "${out}")"
    return 0
  fi
  echo "[chebnet-data] 下载 ${url}"
  curl --fail --location --retry 3 --output "${out}" "${url}"
  sha256sum "${out}" | tee "${out}.sha256"
}
fetch "${PROCESSED_URL}" "${CACHE}/geometric_data_processed.pt"
fetch "${SPLITS_URL}" "${CACHE}/lrgb_splits_peptides_func.json"
CONDA_HOME="${CONDA_HOME:-/home/lab_user/tools/miniconda3}"
# shellcheck disable=SC1091
source "${CONDA_HOME}/etc/profile.d/conda.sh"
conda activate "${CHEBNET_CONDA_ENV:-dtgb}"
python "${ROOT}/repro/build_stable_chebnet_peptides.py" \
  --processed "${CACHE}/geometric_data_processed.pt" \
  --splits "${CACHE}/lrgb_splits_peptides_func.json" \
  --out-root "${DEST}"
export CUDA_VISIBLE_DEVICES=""
python - <<PY
from torch_geometric.datasets import LRGBDataset
root = "${DEST}"
for split in ("train", "val", "test"):
    ds = LRGBDataset(root=root, name="Peptides-func", split=split)
    print(f"[chebnet-data] split={split} n={len(ds)} feats={ds.num_node_features} classes={ds.num_classes}")
PY
echo "[chebnet-data] done"
