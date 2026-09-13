#!/usr/bin/env bash
# 31 PUMA：CoraFull 的 npz。PyG CoraFull 实际下的是 graph2gauss 的 cora.npz。
# GitHub 走 ghfast.top，放到官方 --data-dir ./data 对应的 raw/。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW="${ROOT}/repro/puma/data/cora/raw"
MIRROR="${GITHUB_MIRROR:-https://ghfast.top}"
UPSTREAM="https://github.com/abojchevski/graph2gauss/raw/master/data/cora.npz"
mkdir -p "${RAW}"
out="${RAW}/cora.npz"
if [[ -f "${out}" ]]; then
  echo "[puma] exists ${out}"
else
  url="${MIRROR}/${UPSTREAM}"
  echo "[puma] wget ${url}"
  wget -q --timeout=90 -O "${out}.part" "${url}"
  mv "${out}.part" "${out}"
fi
sha256sum "${out}"
echo "[puma] CoraFull 就绪。arxiv/reddit/products 全量再拉，预处理不自动下。"
