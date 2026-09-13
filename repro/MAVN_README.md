# 13 MAVN 预处理 / 复现入口

论文：*Learn When and Where to Connect: Adaptive Virtual Nodes for Dynamic Message Passing on Graphs*（KDD 2026）。论文库编号 13。学习模块：`LEARNING_PLAN.md` M5。

- 官方仓库：`repro/mavn/`（https://github.com/bdi-lab/MAVN）
- 固定提交：`3773c40a753a08528aa73c641c4f991ba4cfd4e5`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[MAVN_REPRO_LOG.md](MAVN_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/13_MAVN_KDD2026.pdf`
- 读书笔记：`paper/notes/13_mavn.md`
- 运行产物：`results/mavn/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `dtgb`；echo reuse dtgb first |
| 数据 | Peptides/Pascal 来自 Dropbox/PyG LRGB；minesweeper/tolokers 用 ghfast 拉 yandex npz。脚本 repro/download_mavn_data.sh |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_mavn_full.sh`（默认 dry-run） |

对照目标：Peptides-func AP（seed 0–3）；PascalVOC-SP；minesweeper / tolokers 10 split。附录 PDF：Setup_MAVN_KDD2026.pdf

## 烟雾（短）

```bash
echo '先 bash repro/download_mavn_data.sh minesweeper，再把 README 的 minesweeper 命令 --num_epoch 改为 2'
```

烟雾数据集优先 minesweeper（比 Peptides 小）。不要在没数据时启动 train.py。

## 全量（默认不跑）

```bash
bash repro/run_mavn_full.sh          # 只打印命令
FULL=1 bash repro/run_mavn_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
