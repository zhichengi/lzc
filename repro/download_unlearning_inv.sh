#!/usr/bin/env bash
# 41 unlearning_inv：Planetoid Cora 到官方 RAW_DATA_PATH。GitHub 走 ghfast。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW="${ROOT}/repro/unlearning_inv/temp_data/raw_data/cora/raw"
MIRROR="${GITHUB_MIRROR:-https://ghfast.top}"
UPSTREAM="https://github.com/kimiyoung/planetoid/raw/master/data"
mkdir -p "${RAW}"
NAMES="x tx allx y ty ally graph test.index"
ok=0
for n in ${NAMES}; do
  f="ind.cora.${n}"
  out="${RAW}/${f}"
  if [[ -f "${out}" && $(wc -c < "${out}") -gt 50 ]]; then
    echo "[unlearn] exists ${f}"
    ok=$((ok+1))
    continue
  fi
  url="${MIRROR}/${UPSTREAM}/${f}"
  echo "[unlearn] wget ${url}"
  wget -q --timeout=60 -O "${out}.part" "${url}"
  mv "${out}.part" "${out}"
  ok=$((ok+1))
done
echo "[unlearn] ${ok}/8 files in ${RAW}"
ls -l "${RAW}"
