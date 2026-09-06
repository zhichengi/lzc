#!/bin/bash
# 复现一组实验:论文表格中每一行对应脚本里一条命令
set -e
cd "$(dirname "$0")/.."

for seed in 0 1 2; do
    CUDA_VISIBLE_DEVICES=0 python main.py \
        --config configs/example.yaml \
        --seed "$seed"
done
