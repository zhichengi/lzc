# 10 STABLE_CHEBNET 预处理 / 复现入口

论文：*Return of ChebNet: Understanding and Improving an Overlooked GNN on Long-Range Tasks*（NeurIPS 2025 Spotlight）。论文库编号 10。学习模块：`LEARNING_PLAN.md` M1,M5。

- 官方仓库：`repro/stable_chebnet/`（https://github.com/ahariri13/Stable-ChebNet）
- 固定提交：`7d7a7e2696119891d277fd3fa2b32fdda454b814`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[STABLE_CHEBNET_REPRO_LOG.md](STABLE_CHEBNET_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/10_Stable-ChebNet_NeurIPS2025.pdf`
- 读书笔记：`paper/notes/10_stable_chebnet.md`
- 运行产物：`results/stable_chebnet/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `dtgb`；echo 'reuse dtgb; pip install ogb if missing' |
| 数据 | Peptides 走 PyG LRGB；不要直连 GitHub，先镜像或本地下好再离线加载。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 已跑官方脚本 2ep（占位图；测试段写死 cuda，CPU 退出 1） |
| 全量 | `FULL=1 bash repro/run_stable_chebnet_full.sh`（默认 dry-run） |

对照目标：Peptides-func / Peptides-struct（LRGB）；Barbell 与 GraphProp 为合成/属性任务

## 烟雾（短）

```bash
export WANDB_MODE=offline
bash repro/run_stable_chebnet.sh smoke_peptides_2ep -- bash -c 'cd Peptides/Stable && python ChebStable_peptide.py --epochs 2'
```

官方脚本已有 `--epochs`。当前 `peptides-func/` 是占位图（Dropbox 不通）；换成真正 LRGB 后再对论文。Barbell 在 dtgb/PyG 2.8 下会因 `normalize=` 失败，不要当主表烟雾。

## 全量（默认不跑）

```bash
bash repro/run_stable_chebnet_full.sh          # 只打印命令
FULL=1 bash repro/run_stable_chebnet_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
