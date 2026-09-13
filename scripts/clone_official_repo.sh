#!/usr/bin/env bash
# 用 ghfast.top 镜像浅克隆官方仓库到 repro/<name>/，并与 GitHub ls-remote SHA 比对。
# 用法: bash scripts/clone_official_repo.sh NAME GITHUB_SLUG [BRANCH]
#   例: bash scripts/clone_official_repo.sh gbn ZhenhHuang/GBN
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="${1:?name}"
SLUG="${2:?owner/repo}"
BRANCH="${3:-}"
DEST="${ROOT}/repro/${NAME}"
MIRROR_PREFIX="${GITHUB_MIRROR:-https://ghfast.top}"
UPSTREAM="https://github.com/${SLUG}.git"
MIRROR="${MIRROR_PREFIX}/${UPSTREAM}"

if [[ -d "${DEST}/.git" ]]; then
  echo "[clone] already exists: ${DEST} HEAD=$(git -C "${DEST}" rev-parse HEAD)"
  exit 0
fi
if [[ -e "${DEST}" ]]; then
  echo "[clone] ${DEST} exists but is not a git repo" >&2
  exit 1
fi

clone_url="${MIRROR}"
echo "[clone] ${NAME} <- ${clone_url}"
if [[ -n "${BRANCH}" ]]; then
  git clone --depth 1 --branch "${BRANCH}" "${clone_url}" "${DEST}"
else
  git clone --depth 1 "${clone_url}" "${DEST}"
fi
HEAD="$(git -C "${DEST}" rev-parse HEAD)"
REMOTE_HEAD="$(git ls-remote "${clone_url}" HEAD | awk '{print $1}')"
echo "[clone] ${NAME} local=${HEAD}"
echo "[clone] ${NAME} remote_HEAD=${REMOTE_HEAD:-unknown}"
if [[ -n "${REMOTE_HEAD}" && "${HEAD}" != "${REMOTE_HEAD}" ]]; then
  echo "[clone] WARN SHA mismatch (shallow clone may follow default branch tip)" >&2
fi
git -C "${DEST}" rev-parse --abbrev-ref HEAD
git -C "${DEST}" log -1 --oneline
