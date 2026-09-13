# 09 GBN 预处理 / 复现入口

论文：*Deeper with Riemannian Geometry: Overcoming Oversmoothing and Oversquashing for Graph Foundation Models*（NeurIPS 2025）。论文库编号 09。学习模块：`LEARNING_PLAN.md` M1。

- 官方仓库：`repro/gbn/`（https://github.com/ZhenhHuang/GBN）
- 固定提交：`72ad3692916ecc60f2c78d5bd01a55d7c6297a4f`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[GBN_REPRO_LOG.md](GBN_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/09_Riemannian_GBN_NeurIPS2025.pdf`
- 读书笔记：`paper/notes/09_gbn.md`
- 运行产物：`results/gbn/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `dtgb`；# 复用 dtgb。若 BoundaryGCN / torch-scatter 报错再新建 gbn。 |
| 数据 | PyG：WebKB / Planetoid / Coauthor / WikiCS / Heterophilous。优先符号链接已有 `repro/sgpc/data/`。Coauthor CS 需另下。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_gbn_full.sh`（默认 dry-run） |

对照目标：节点分类（WikiCS / Texas 等）与深层 GCN 对照；仓库预置 configs/NC/CS.json

## 烟雾（短）

```bash
bash repro/run_gbn.sh smoke_texas -- --task NC --dataset Texas --epochs_nc 2 --exp_iters 1 --patience_nc 1 --hid_dim 64 --embed_dim 64
```

烟雾用 Texas 并在运行后删除 configs/NC/Texas.json（若原本不存在）。不要改 CS.json。

## 全量（默认不跑）

```bash
bash repro/run_gbn_full.sh          # 只打印命令
FULL=1 bash repro/run_gbn_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
