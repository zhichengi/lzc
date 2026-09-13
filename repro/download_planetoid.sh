#!/usr/bin/env bash
# 从镜像拉取 Planetoid 原始文件到 repro/gctd/data/<Name>/raw/
# PyG 直连 GitHub 常超时。相对路径，可移植。
# 用法: bash repro/download_planetoid.sh cora
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAME="${1:-cora}"
NAME_LOWER="$(echo "$NAME" | tr '[:upper:]' '[:lower:]')"
# 必须与 Planetoid(root, name.lower()) 一致：data/cora/raw，不是 data/Cora/raw
DIR_NAME="$NAME_LOWER"

RAW="${SCRIPT_DIR}/gctd/data/${DIR_NAME}/raw"
mkdir -p "$RAW"
UPSTREAM="https://github.com/kimiyoung/planetoid/raw/master/data"
NAMES="x tx allx y ty ally graph test.index"

try_get() {
  wget -q --timeout=30 --tries=2 -O "$2" "$1" && test "$(wc -c < "$2")" -gt 50
}

ok=0
for mirror in \
  "https://ghfast.top/${UPSTREAM}" \
  "${UPSTREAM}"
do
  fail=0
  for n in $NAMES; do
    f="ind.${NAME_LOWER}.${n}"
    if try_get "${mirror}/${f}" "${RAW}/${f}"; then
      echo "ok ${f} $(wc -c < "${RAW}/${f}")"
    else
      echo "fail ${f} via ${mirror}"
      fail=1
      break
    fi
  done
  if [ "$fail" -eq 0 ]; then ok=1; break; fi
done
if [ "$ok" -ne 1 ]; then
  echo "download failed"
  exit 1
fi
echo "saved under ${RAW}"
