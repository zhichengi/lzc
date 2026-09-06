"""训练入口:python main.py --config configs/example.yaml"""
import argparse
from pathlib import Path

import yaml


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=str, required=True, help="实验配置文件")
    p.add_argument("--gpu", type=int, default=0)
    p.add_argument("--seed", type=int, default=None, help="覆盖配置中的 seed")
    return p.parse_args()


def main():
    args = parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    if args.seed is not None:
        cfg["seed"] = args.seed

    print(f"配置文件: {args.config}")
    print(f"使用 GPU: {args.gpu}")
    # TODO: 数据加载 -> 模型构建 -> 训练循环 -> 结果写 results/
    Path(cfg["output"]["log_dir"]).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()
