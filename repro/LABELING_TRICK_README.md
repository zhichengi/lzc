# 44 LABELING_TRICK 预处理 / 复现入口

论文：*Improving Graph Neural Networks on Multi-node Tasks with the Labeling Trick*（JMLR 2025）。论文库编号 44。学习模块：`LEARNING_PLAN.md` M5。

- 官方仓库：`repro/labeling_trick/`（https://github.com/GraphPKU/LabelingTrick）
- 固定提交：`17b71959c854c5379e1b042100321661c7d1d55e`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[LABELING_TRICK_REPRO_LOG.md](LABELING_TRICK_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/11-journals-tnnls-jmlr/44_LabelingTrick_JMLR2025.pdf`
- 读书笔记：`paper/notes/44_labeling_trick.md`
- 运行产物：`results/labeling_trick/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `dtgb`；echo reuse dtgb; python -c 'import optuna, torch_scatter' |
| 数据 | `repro/labeling_trick/LinkPred/data/` 链到已有 Planetoid。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_labeling_trick_full.sh`（默认 dry-run） |

对照目标：LinkPred 子目录：Cora/CiteSeer/PubMed 无向链接预测 AUROC；`--test` 为 10 seed 正式协议

## 烟雾（短）

```bash
bash repro/run_labeling_trick.sh smoke_import -- python -c "from Dataset import load_dataset; d=load_dataset('Cora'); print('nodes', d.num_nodes, 'edges', d.edge_index.size(1))"
```

官方无短 epoch CLI。训练烟雾不要用 --test（那是 10 seed 全量）。全量：python main.py --dataset Cora --test

## 全量（默认不跑）

```bash
bash repro/run_labeling_trick_full.sh          # 只打印命令
FULL=1 bash repro/run_labeling_trick_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
