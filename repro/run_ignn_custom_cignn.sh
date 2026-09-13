#!/usr/bin/env bash
# IGNN c-IGNN custom split（10× 48/32/20）排队脚本。
# 默认只打印命令，不训练。GPU 空闲后显式执行：
#   IGNN_EXECUTE=1 bash repro/run_ignn_custom_cignn.sh
# 仅烟雾测试（三个数据集各 2 epoch / repeat 1）：
#   IGNN_EXECUTE=1 IGNN_SMOKE_ONLY=1 bash repro/run_ignn_custom_cignn.sh
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPLIT_DIR="${ROOT}/repro/ignn/data/random_splits/fixed_splits"
RUNNER="${ROOT}/repro/run_ignn.sh"

EXPECTED_ACTOR="9668e2f89750f49567b99671d250c1bc9300574298ce6efc910dd76dbb7e8478"
EXPECTED_CHAMELEON="2174cc40152f1c5d78b4022d80df652c914d5390f402d20ffd114705799c9b2b"
EXPECTED_SQUIRREL="e6220e175e748158ce3fd4816e80bbe5d8c75ea09b860ce577ce47e13ee1a222"

check_hash() {
    local file="$1"
    local expected="$2"
    local actual
    actual="$(sha256sum "${file}" | awk '{print $1}')"
    if [[ "${actual}" != "${expected}" ]]; then
        echo "划分指纹不符: ${file}" >&2
        echo "  expected ${expected}" >&2
        echo "  actual   ${actual}" >&2
        exit 3
    fi
}

echo "=== IGNN custom split 预检 ==="
check_hash "${SPLIT_DIR}/actor_pyg-48-32-splitsx10.npy" "${EXPECTED_ACTOR}"
check_hash "${SPLIT_DIR}/chameleon_critical-48-32-splitsx10.npy" "${EXPECTED_CHAMELEON}"
check_hash "${SPLIT_DIR}/squirrel_critical-48-32-splitsx10.npy" "${EXPECTED_SQUIRREL}"
if compgen -G "${SPLIT_DIR}/*-48-32-splitsx1.npy" > /dev/null; then
    echo "发现 splitsx1.npy，先删除再跑，避免 repeat=1 读到非官方划分：" >&2
    ls "${SPLIT_DIR}"/*-48-32-splitsx1.npy >&2
    exit 4
fi
echo "划分指纹通过；无 splitsx1 污染。"
echo

COMMON_PREFIX=(--gpu_id 0 --seed 42 --model ignn --agg_type gcn_incep --IN IN-SN --eval_interval 1 --eval_start 0 --public False)

cmd_actor() {
    local label="$1"
    local epochs="$2"
    local repeat="$3"
    echo bash "${RUNNER}" "${label}" "${COMMON_PREFIX[@]}" \
        --dataset actor --source pyg --n_epochs "${epochs}" --h_feats 512 --lr 0.001 \
        --l2_coef 0.0 --n_hops 1 --n_layers 1 --early_stop 100 --RN concat --norm_type ln \
        --act_type relu --preln False --fast False --pre_dropout 0.0 --hid_dropout 0.8 \
        --clf_dropout 0.9 --repeat "${repeat}"
}

cmd_chameleon() {
    local label="$1"
    local epochs="$2"
    local repeat="$3"
    echo bash "${RUNNER}" "${label}" "${COMMON_PREFIX[@]}" \
        --dataset chameleon --source critical --n_epochs "${epochs}" --h_feats 64 --lr 0.001 \
        --l2_coef 0.0 --n_hops 1 --n_layers 5 --early_stop 150 --RN concat --norm_type none \
        --act_type none --preln True --fast False --pre_dropout 0.8 --hid_dropout 0.3 \
        --clf_dropout 0.3 --repeat "${repeat}"
}

cmd_squirrel() {
    local label="$1"
    local epochs="$2"
    local repeat="$3"
    echo bash "${RUNNER}" "${label}" "${COMMON_PREFIX[@]}" \
        --dataset squirrel --source critical --n_epochs "${epochs}" --h_feats 128 --lr 0.005 \
        --l2_coef 0.0 --n_hops 1 --n_layers 3 --early_stop 200 --RN none --norm_type none \
        --act_type relu --preln False --fast False --pre_dropout 0.8 --hid_dropout 0.2 \
        --clf_dropout 0.8 --repeat "${repeat}"
}

echo "=== 待跑队列（c-IGNN，01-best-cIGNN.sh 第 2/4/6 行）==="
cmd_actor smoke_actor_c_custom_2ep_r1 2 1
cmd_actor official_actor_c_custom_r10 3000 10
cmd_chameleon smoke_chameleon_c_custom_2ep_r1 2 1
cmd_chameleon official_chameleon_c_custom_r10 3000 10
cmd_squirrel smoke_squirrel_c_custom_2ep_r1 2 1
cmd_squirrel official_squirrel_c_custom_r10 3000 10
echo

EXECUTE_FLAG="${IGNN_EXECUTE:-0}"
SMOKE_FLAG="${IGNN_SMOKE_ONLY:-0}"
if [[ "${EXECUTE_FLAG}" != "1" ]]; then
    echo "默认不训练。服务器空闲后执行："
    echo "  IGNN_EXECUTE=1 bash repro/run_ignn_custom_cignn.sh"
    echo "仅烟雾："
    echo "  IGNN_EXECUTE=1 IGNN_SMOKE_ONLY=1 bash repro/run_ignn_custom_cignn.sh"
    exit 0
fi

run_one() {
    local label="$1"
    shift
    echo
    echo ">>> ${label}"
    bash "${RUNNER}" "${label}" "$@"
    if [[ "${label}" == *smoke* ]]; then
        if compgen -G "${SPLIT_DIR}/*-48-32-splitsx1.npy" > /dev/null; then
            echo "烟雾测试生成了 splitsx1，正在删除以免污染后续 repeat=1。"
            rm -f "${SPLIT_DIR}"/*-48-32-splitsx1.npy
        fi
    fi
}

echo "EXECUTE_FLAG=1，开始训练。包装器仍走 85% 资源上限。"

run_one smoke_actor_c_custom_2ep_r1 "${COMMON_PREFIX[@]}" --dataset actor --source pyg --n_epochs 2 --h_feats 512 --lr 0.001 --l2_coef 0.0 --n_hops 1 --n_layers 1 --early_stop 100 --RN concat --norm_type ln --act_type relu --preln False --fast False --pre_dropout 0.0 --hid_dropout 0.8 --clf_dropout 0.9 --repeat 1
run_one smoke_chameleon_c_custom_2ep_r1 "${COMMON_PREFIX[@]}" --dataset chameleon --source critical --n_epochs 2 --h_feats 64 --lr 0.001 --l2_coef 0.0 --n_hops 1 --n_layers 5 --early_stop 150 --RN concat --norm_type none --act_type none --preln True --fast False --pre_dropout 0.8 --hid_dropout 0.3 --clf_dropout 0.3 --repeat 1
run_one smoke_squirrel_c_custom_2ep_r1 "${COMMON_PREFIX[@]}" --dataset squirrel --source critical --n_epochs 2 --h_feats 128 --lr 0.005 --l2_coef 0.0 --n_hops 1 --n_layers 3 --early_stop 200 --RN none --norm_type none --act_type relu --preln False --fast False --pre_dropout 0.8 --hid_dropout 0.2 --clf_dropout 0.8 --repeat 1

if [[ "${SMOKE_FLAG}" == "1" ]]; then
    echo "SMOKE_ONLY=1，三个烟雾测试完成，停止。"
    exit 0
fi

run_one official_actor_c_custom_r10 "${COMMON_PREFIX[@]}" --dataset actor --source pyg --n_epochs 3000 --h_feats 512 --lr 0.001 --l2_coef 0.0 --n_hops 1 --n_layers 1 --early_stop 100 --RN concat --norm_type ln --act_type relu --preln False --fast False --pre_dropout 0.0 --hid_dropout 0.8 --clf_dropout 0.9 --repeat 10
run_one official_chameleon_c_custom_r10 "${COMMON_PREFIX[@]}" --dataset chameleon --source critical --n_epochs 3000 --h_feats 64 --lr 0.001 --l2_coef 0.0 --n_hops 1 --n_layers 5 --early_stop 150 --RN concat --norm_type none --act_type none --preln True --fast False --pre_dropout 0.8 --hid_dropout 0.3 --clf_dropout 0.3 --repeat 10
run_one official_squirrel_c_custom_r10 "${COMMON_PREFIX[@]}" --dataset squirrel --source critical --n_epochs 3000 --h_feats 128 --lr 0.005 --l2_coef 0.0 --n_hops 1 --n_layers 3 --early_stop 200 --RN none --norm_type none --act_type relu --preln False --fast False --pre_dropout 0.8 --hid_dropout 0.2 --clf_dropout 0.8 --repeat 10
echo "custom c-IGNN 首轮三数据集完成。"
