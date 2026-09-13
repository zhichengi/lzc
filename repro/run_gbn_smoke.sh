#!/usr/bin/env bash
# GBN 烟雾：放入含 layer_wise 的短 epoch json，跑完删除，不改 CS.json。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG_DIR="${ROOT}/repro/gbn/configs/NC"
CFG="${CFG_DIR}/Texas.json"
SMOKE_JSON="${ROOT}/results/gbn/smoke_texas.json"
bash "${ROOT}/repro/download_gbn.sh"
mkdir -p "${CFG_DIR}"
cp "${SMOKE_JSON}" "${CFG}"
cleanup() { rm -f "${CFG}"; echo "[gbn-smoke] removed ${CFG}"; }
trap cleanup EXIT
bash "${ROOT}/repro/run_gbn.sh" smoke_texas -- python main.py --task NC --dataset Texas
