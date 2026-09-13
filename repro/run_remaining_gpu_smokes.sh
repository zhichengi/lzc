#!/usr/bin/env bash
# GPU 空闲后按队列顺序补训练烟雾。同一时刻只占一张卡。
# SGPC Squirrel split 循环结束后才启动。
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
log() { echo "[gpu-smoke] $(date --iso-8601=seconds) $*"; }

log "waiting for SGPC Squirrel (python main.py 4 --split) to finish"
while pgrep -f '[p]ython main.py 4 --split' >/dev/null; do
  sleep 30
done
log "GPU free. start remaining training smokes"

export WANDB_MODE=offline
export WANDB_SILENT=true
export WANDB_DIR="${ROOT}/results/stable_chebnet"
unset CUDA_VISIBLE_DEVICES

log "=== 10 stable_chebnet dummy peptides 2ep (need real GPU for hardcoded test device) ==="
bash repro/run_stable_chebnet.sh smoke_peptides_dummy_2ep_gpu -- \
  bash -c 'cd Peptides/Stable && python ChebStable_peptide.py --epochs 2'
log "chebnet exit=$?"

log "=== 31 puma bare corafull 1ep (dtgb, not puma env) ==="
bash scripts/repro_wrap.sh --paper puma --env dtgb --repo repro/puma --cwd repro/puma \
  --label smoke_bare_corafull -- \
  python train.py --dataset-name corafull --cgl-method bare --cls-epoch 1 --repeat 1 --evaluate --device cuda:0 --data-dir ./data --result-dir ./results
log "puma exit=$?"

log "=== 13 mavn minesweeper 2ep ==="
bash repro/run_mavn.sh smoke_minesweeper_2ep -- python train.py \
  --exp 'KDD2026' --log_name 'MAVN_smoke' --seed 0 --dataset_name 'minesweeper' --split 0 \
  --task 'Node Classification' --eval_metric 'AUCROC' --model_name 'MAVN' \
  --base_model 'GraphSAGE-TunedGNN' --dim_pe '0' --dim 64 --dim_dot 64 --num_VN 80 --num_head 1 \
  --act 'ReLU' --normalize 'BatchNorm' --num_layer 15 --num_mlp_layer 1 --num_pred_mlp_layer 1 \
  --norm_N 'GraphNorm' --norm_VN 'None' --aggr_VN 'normalized_sigmoid' --log_w 0.2 \
  --pe 'None' --pe_norm 'None' --num_pe '0' --loss_function 'CE' --optimizer 'Adam' \
  --lr_max 5e-2 --grad_clip 0.0 --warmup_epoch 300 --restart_epoch 2700 --dropout 0.2 \
  --num_epoch 2 --batch_size -1 --tau_end 0.1 --tau_epoch 1500 --pred_mlp_layer_init 'default' --res --no_write
log "mavn exit=$?"

log "=== 41 unlearning_inv cora 2ep ==="
bash repro/run_unlearning_inv.sh smoke_cora -- python main.py \
  --dataset_name cora --target_model GCN --exp Inversion --method GIF \
  --unlearn_ratio 0.05 --attack_method trend_steal --num_runs 1 --num_epochs 2 \
  --cuda 0 --is_gen_unlearn_request True --is_gen_unlearned_probs True
log "unlearning exit=$?"

log "all queued GPU smokes finished"
