# 08 FAIR_EVAL_GFM 预处理 / 复现入口

论文：*A Fair Evaluation of Graph Foundation Models for Node Property Prediction*（ICML 2026 Workshop）。论文库编号 08。学习模块：`LEARNING_PLAN.md` M6。

- 官方仓库：`repro/fair_eval_gfm/`（https://github.com/yandex-research/gnn-fair-evaluation）
- 固定提交：`0a388f087773258e8f2559d801129dfe87adb3bc`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[FAIR_EVAL_GFM_REPRO_LOG.md](FAIR_EVAL_GFM_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/01-graph-foundation-models/08_FairEval_GFM_ICML2026Workshop.pdf`
- 读书笔记：`paper/notes/08_fair_eval_gfm.md`
- 运行产物：`results/fair_eval_gfm/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `gfm`；bash scripts/setup_gfm_uv.sh |
| 数据 | https://zenodo.org/records/16895532 下载解压后 `ln -s <path> repro/fair_eval_gfm/data` |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_fair_eval_gfm_full.sh`（默认 dry-run） |

对照目标：GraphLand 上的 GNN 基线；GFM 数字来自各官方仓。本仓库只用 uv 复现 GNN 部分。

## 烟雾（短）

```bash
export CUDA_VISIBLE_DEVICES=""
export PATH="/home/lab_user/tools/miniconda3/bin:$PATH"
cd repro/fair_eval_gfm
uv run --offline bin/go.py /home/lab_user/project/lzc/results/fair_eval_gfm/smoke/evaluation.toml --n_seeds 1 --ensemble_size 0 --force
```

不要改官方 `exp/` 下 toml。conda `gfm` 不存在，用 uv。

## 全量（默认不跑）

```bash
bash repro/run_fair_eval_gfm_full.sh          # 只打印命令
FULL=1 bash repro/run_fair_eval_gfm_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
