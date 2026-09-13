#!/usr/bin/env bash
# 08 fair_eval_gfm：只拉烟雾用的 GraphLand tolokers-2（约 3.2MB），不解压其它 Zenodo 大包。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/repro/fair_eval_gfm/data"
ZIP="${ROOT}/results/fair_eval_gfm/tolokers-2.zip"
URL="https://zenodo.org/records/16895532/files/tolokers-2.zip?download=1"
mkdir -p "${DEST}" "${ROOT}/results/fair_eval_gfm"
if [[ -f "${DEST}/tolokers-2/edgelist.csv" ]]; then
  echo "[gfm-data] exists ${DEST}/tolokers-2"
  exit 0
fi
echo "[gfm-data] wget ${URL}"
wget -4 --timeout=60 --tries=3 -O "${ZIP}" "${URL}"
sha256sum "${ZIP}"
unzip -o "${ZIP}" -d "${DEST}"
echo "[gfm-data] 其余 GraphLand zip 全量再拉。目录应对 ln -s <graphland_root> repro/fair_eval_gfm/data"
