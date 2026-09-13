# 15 SCALEGNN 预处理 / 复现入口

论文：*ScaleGNN: Towards Scalable Graph Neural Networks via Adaptive High-order Neighboring Feature Fusion*（WWW 2026）。论文库编号 15。学习模块：`LEARNING_PLAN.md` M3。

- 官方仓库：`repro/scalegnn/`（https://github.com/lx970414/ScaleGNN）
- 固定提交：`4825c7ed2ccb8a7a4c47edce4afefb1e771389aa`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[SCALEGNN_REPRO_LOG.md](SCALEGNN_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/03-scalable-bigdata-gnn/15_ScaleGNN_WWW2026.pdf`
- 读书笔记：`paper/notes/15_scalegnn.md`
- 运行产物：`results/scalegnn/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `dtgb`；echo reuse dtgb; python -c 'import yaml,ogb' |
| 数据 | 小图 Planetoid 符号链接 `repro/sgpc/data/Cora` → `repro/scalegnn/data/Cora`。arxiv 用 OGB `./data`。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_scalegnn_full.sh`（默认 dry-run） |

对照目标：Cora/Citeseer/Pubmed 小图；主表 ogbn-arxiv（约 1 小时 / 10 seed）。papers100M 仅 memmap 路径。

## 烟雾（短）

```bash
bash repro/run_scalegnn.sh smoke_cora -- python main.py --config /home/lab_user/project/lzc/results/scalegnn/smoke_cora.yaml
```

smoke yaml 由预处理写入 results/scalegnn/smoke_cora.yaml（epochs=2, device=cuda）。

## 全量（默认不跑）

```bash
bash repro/run_scalegnn_full.sh          # 只打印命令
FULL=1 bash repro/run_scalegnn_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
