# 31 PUMA 预处理 / 复现入口

论文：*PUMA: Efficient Continual Graph Learning with Graph Condensation*（TKDE 2025）。论文库编号 31。学习模块：`LEARNING_PLAN.md` M2。

- 官方仓库：`repro/puma/`（https://github.com/superallen13/PUMA）
- 固定提交：`9e4e87f53db0da6aacad4a0a9d08f1c2970413d0`（分支 `master`，与 `git ls-remote HEAD` 一致）
- 过程日志：[PUMA_REPRO_LOG.md](PUMA_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/08-ccf-journals/31_PUMA_TKDE2025.pdf`
- 读书笔记：`paper/notes/31_puma.md`
- 运行产物：`results/puma/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `puma`；bash scripts/setup_puma_conda.sh |
| 数据 | CoraFull 由 PyG 下载；OGB 需镜像。数据根 `--data-dir ./data`。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_puma_full.sh`（默认 dry-run） |

对照目标：Table 2 class-IL：CoraFull / arxiv / reddit / products，指标 AP / mAP / AF

## 烟雾（短）

```bash
bash repro/run_puma.sh smoke_bare_corafull -- --dataset-name corafull --cgl-method bare --cls-epoch 1 --repeat 1 --evaluate
```

新建 conda `puma` 之前，可先在 dtgb 试 bare 1 epoch。失败则按 setup_puma_conda.sh 建环境，不要往 dtgb 装 torch 1.13。

## 全量（默认不跑）

```bash
bash repro/run_puma_full.sh          # 只打印命令
FULL=1 bash repro/run_puma_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
