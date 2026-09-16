#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW_DIR="${ROOT_DIR}/repro/scadyg/dataset_raw/bitcoinalpha"
RAW_GZ="${RAW_DIR}/soc-sign-bitcoinalpha.csv.gz"
RAW_CSV="${RAW_DIR}/bitcoinalpha.csv"
URL="https://snap.stanford.edu/data/soc-sign-bitcoinalpha.csv.gz"

mkdir -p "${RAW_DIR}"
if [[ ! -f "${RAW_GZ}" ]]; then
  curl --fail --location --retry 3 --output "${RAW_GZ}" "${URL}"
fi

sha256sum "${RAW_GZ}" | tee "${RAW_GZ}.sha256"
gzip -cd "${RAW_GZ}" | sed '/^[[:space:]]*#/d' > "${RAW_CSV}"

conda run -n "${SCADYG_CONDA_ENV:-scadyg}" \
  python "${ROOT_DIR}/repro/scadyg-extra/process_bitcoin.py" \
  --input "${RAW_CSV}" \
  --output-root "${ROOT_DIR}/repro/scadyg/dataset" \
  --snapshot-seconds "${SCADYG_SNAPSHOT_SECONDS:-723000}"