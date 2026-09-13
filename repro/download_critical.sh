#!/usr/bin/env bash
# 从镜像拉取 Platonov et al. "critical look" 异配数据集到 repro/ignn/data/
# graph_datasets.datasets.critical 直连 GitHub 常超时；文件存在时它会跳过下载。
# 文件名规则与 critical.py 一致：
#   roman-empire   -> roman_empire.npz
#   amazon-ratings -> amazon_ratings.npz
#   chameleon      -> chameleon_filtered_directed.npz
#   squirrel       -> squirrel_filtered_directed.npz
# 用法: bash repro/download_critical.sh roman-empire chameleon
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/ignn/data"
mkdir -p "$DATA_DIR"

# 与 graph_datasets/data_info.py 的 CRITICAL_URL 同一提交
COMMIT="a431395"
UPSTREAM="https://github.com/yandex-research/heterophilous-graphs/raw/${COMMIT}/data"

if [ $# -lt 1 ]; then
  echo "用法: $0 <dataset> [dataset ...]" >&2
  exit 2
fi

try_get() {
  wget -q --timeout=60 --tries=2 -O "$2" "$1" && test "$(wc -c < "$2")" -gt 1000
}

status=0
for name in "$@"; do
  case "$name" in
    chameleon|squirrel) file="${name}_filtered_directed.npz" ;;
    *) file="$(echo "$name" | tr '-' '_').npz" ;;
  esac
  dest="${DATA_DIR}/${file}"
  if [ -s "$dest" ]; then
    echo "exists ${file} $(wc -c < "$dest") sha256=$(sha256sum "$dest" | awk '{print $1}')"
    continue
  fi
  ok=0
  for mirror in "https://ghfast.top/${UPSTREAM}" "${UPSTREAM}"; do
    if try_get "${mirror}/${file}" "$dest"; then
      ok=1
      break
    fi
    rm -f "$dest"
  done
  if [ "$ok" -eq 1 ]; then
    echo "ok ${file} $(wc -c < "$dest") sha256=$(sha256sum "$dest" | awk '{print $1}')"
  else
    echo "fail ${file}" >&2
    status=1
  fi
done
exit "$status"
