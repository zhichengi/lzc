# <论文题目缩写>(填你的方法名)

> 一句话介绍:研究什么问题、提出什么方法、主要结论。

## 环境

```bash
conda create -n <env_name> python=3.10
pip install -r requirements.txt
```

## 数据准备

下载后放到 `data/raw/`,预处理脚本产出写入 `data/processed/`。

## 复现实验

```bash
bash scripts/run_example.sh          # 一键跑一组实验(多 seed)
python main.py --config configs/example.yaml   # 单次运行
```

## 目录结构

```
├── main.py              # 训练入口
├── configs/             # 实验配置(每条实验结果对应一个 yaml)
│   └── experiments/     # 正式实验配置(区别于调试用的 example)
├── data/
│   ├── raw/             # 原始数据(不入 git)
│   └── processed/       # 预处理产物(不入 git)
├── src/
│   ├── models/          # 模型定义
│   ├── layers/          # 网络层/算子
│   ├── dataloaders/     # 数据集加载
│   ├── trainers/        # 训练/评估循环
│   └── utils/           # 工具函数(指标、随机种子、日志)
├── scripts/             # 一键复现脚本
├── notebooks/           # 探索分析、画图草稿
├── results/
│   ├── logs/            # 训练日志、指标曲线
│   └── checkpoints/     # 模型权重
├── figures/             # 论文最终用图
├── paper/               # 论文草稿、相关工作笔记
└── tests/               # 单元测试
```

## 实验记录

| 日期 | 实验 | 配置 | 主要结果 | 备注 |
|------|------|------|----------|------|
|      |      |      |          |      |
