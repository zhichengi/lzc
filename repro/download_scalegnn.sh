#!/usr/bin/env bash
# ScaleGNN：Planetoid(root=./data, name=Cora) 需要 ./data/Cora/{raw,processed}
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${ROOT}/repro/sgpc/data"
DST="${ROOT}/repro/scalegnn/data"
mkdir -p "${DST}"
for name in Cora Citeseer Pubmed; do
  inner="${SRC}/${name}/${name}"
  if [[ -d "${inner}/raw" || -d "${inner}/processed" ]]; then
    ln -sfn "${inner}" "${DST}/${name}"
    echo "[scalegnn] ${DST}/${name} -> ${inner}"
  else
    echo "[scalegnn] skip missing ${inner}"
  fi
done
echo "[scalegnn] ogbn-arxiv / products 全量时放到 ${DST}"
