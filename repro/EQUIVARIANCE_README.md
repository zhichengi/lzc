# 01 EQUIVARIANCE 预处理 / 复现入口

论文：*Equivariance Everywhere All At Once: A Recipe for Graph Foundation Models*（NeurIPS 2025）。论文库编号 01。学习模块：`LEARNING_PLAN.md` M6。

- 官方仓库：`repro/equivariance/`（https://github.com/benfinkelshtein/EquivarianceEverywhere）
- 固定提交：`1dfe3870fd8a0de7e15db6958289661b2cabdc37`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[EQUIVARIANCE_REPRO_LOG.md](EQUIVARIANCE_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/01-graph-foundation-models/01_EquivarianceEverywhere_NeurIPS2025.pdf`
- 读书笔记：`paper/notes/01_equivariance.md`
- 运行产物：`results/equivariance/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `gfm`；bash scripts/setup_gfm_uv.sh  # 或独立 conda equivariance |
| 数据 | 脚本内下载多图节点分类基准；全量前应预下载并离线。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_equivariance_full.sh`（默认 dry-run） |

对照目标：trainset1：Cora 训练、其余图测试。与 04 二选一做全量。

## 烟雾（短）

```bash
bash repro/run_equivariance.sh smoke_gat -- python -u main.py --is_train --gnn_type GAT --lr 0.001 --lp_ratio 0.3 --max_epochs 2
```

与 04 都预处理；全量只开一篇。neptune 若强制登录，先定位再跑。

## 全量（默认不跑）

```bash
bash repro/run_equivariance_full.sh          # 只打印命令
FULL=1 bash repro/run_equivariance_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
