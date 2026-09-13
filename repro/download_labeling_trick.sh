#!/usr/bin/env bash
# Labeling Trick LinkPred：./data/Cora/{raw,processed}
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${ROOT}/repro/sgpc/data"
DST="${ROOT}/repro/labeling_trick/LinkPred/data"
mkdir -p "${DST}"
for name in Cora Citeseer Pubmed; do
  inner="${SRC}/${name}/${name}"
  if [[ -d "${inner}/raw" || -d "${inner}/processed" ]]; then
    ln -sfn "${inner}" "${DST}/${name}"
    echo "[labeling] ${DST}/${name} -> ${inner}"
  else
    echo "[labeling] skip missing ${inner}"
  fi
done
