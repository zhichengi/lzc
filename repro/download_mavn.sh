#!/usr/bin/env bash
# MAVN 异配 npz（minesweeper / tolokers）。走 ghfast，不直连 GitHub。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE="${ROOT}/repro/mavn/datasets"
MIRROR="${GITHUB_MIRROR:-https://ghfast.top}"
UPSTREAM="https://github.com/yandex-research/heterophilous-graphs/raw/refs/heads/main/data"
mkdir -p "${BASE}"
fetch() {
  local name="$1"
  mkdir -p "${BASE}/${name}"
  local out="${BASE}/${name}/${name}.npz"
  if [[ -f "${out}" ]]; then
    echo "[mavn] exists ${out}"
    return
  fi
  local url="${MIRROR}/${UPSTREAM}/${name}.npz"
  echo "[mavn] wget ${url}"
  wget -q --timeout=60 -O "${out}.part" "${url}"
  mv "${out}.part" "${out}"
  sha256sum "${out}"
}
case "${1:-all}" in
  minesweeper) fetch minesweeper ;;
  tolokers) fetch tolokers ;;
  all) fetch minesweeper; fetch tolokers ;;
  *) echo "用法: $0 [minesweeper|tolokers|all]" >&2; exit 2 ;;
esac
echo "[mavn] Peptides-func / PascalVOC-SP 见 README Dropbox；预处理不自动拉大文件"
