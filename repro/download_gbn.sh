#!/usr/bin/env bash
# GBN：链到 PyG 数据集的内层目录（root/<name>/raw），避免再去 GitHub。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${ROOT}/repro/sgpc/data"
DST="${ROOT}/repro/gbn/datasets"
mkdir -p "${DST}"

link_inner() {
  local src_parent="$1" inner="$2" dest_name="$3"
  local inner_path="${SRC}/${src_parent}/${inner}"
  if [[ -d "${inner_path}/raw" || -d "${inner_path}/processed" ]]; then
    ln -sfn "${inner_path}" "${DST}/${dest_name}"
    echo "[gbn] ${DST}/${dest_name} -> ${inner_path}"
  else
    echo "[gbn] skip missing ${inner_path}"
  fi
}

link_inner Cora Cora Cora
link_inner Citeseer Citeseer Citeseer
link_inner Pubmed Pubmed Pubmed
link_inner Cornell cornell cornell
link_inner Texas texas texas
link_inner Wisconsin wisconsin wisconsin
link_inner Chameleon chameleon chameleon
link_inner Squirrel squirrel squirrel
link_inner Actor actor actor

# 去掉错误的大写外壳链接，否则 WebKB 仍会认为 texas 不存在而去下载
rm -f "${DST}/Texas" "${DST}/Cornell" "${DST}/Wisconsin" "${DST}/Chameleon" "${DST}/Squirrel" "${DST}/Actor"

echo "[gbn] Coauthor CS / WikiCS / Amazon 全量前再镜像到 ${DST}"
