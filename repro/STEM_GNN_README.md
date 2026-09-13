# 12 STEM_GNN 预处理 / 复现入口

论文：*Generalizing GNNs with Tokenized Mixture of Experts*（KDD 2026）。论文库编号 12。学习模块：`LEARNING_PLAN.md` M7。

- 官方仓库：`repro/stem_gnn/`（https://github.com/GXG-CS/STEM-GNN）
- 固定提交：`8995878ca0df9f1fcaedca49d3a45a44ec8403c2`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[STEM_GNN_REPRO_LOG.md](STEM_GNN_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/12_STEM-GNN_KDD2026.pdf`
- 读书笔记：`paper/notes/12_stem_gnn.md`
- 运行产物：`results/stem_gnn/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `stem_gnn`；bash scripts/setup_stem_gnn_conda.sh |
| 数据 | Cora 等放 `repro/stem_gnn/STEM-GNN/data/`。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_stem_gnn_full.sh`（默认 dry-run） |

对照目标：先 finetune Cora 节点任务；预训练 `pretrain.py --pretrain_dataset all` 很重，有 ckpt 则跳过

## 烟雾（短）

```bash
# 预处理未建 stem_gnn，也不往 dtgb 装 lightning。官方 finetune 目前无法启动。
# 环境独立建好后（不要 conda env create -f 官方 yml）：
CUDA_VISIBLE_DEVICES="" python STEM-GNN/finetune.py --debug --pretrain_dataset na \
  --finetune_dataset cora --finetune_epochs 2 --repeat 1 --finetune_seed 0 --gpu 0
```

预处理不创建 stem_gnn conda。数字不对论文。

## 全量（默认不跑）

```bash
bash repro/run_stem_gnn_full.sh          # 只打印命令
FULL=1 bash repro/run_stem_gnn_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
