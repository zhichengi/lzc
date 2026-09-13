# 23 GRAPHRP 预处理 / 复现入口

论文：*Defending against Model Extraction for GNNs with Model Reprogramming*（KDD 2026）。论文库编号 23。学习模块：`LEARNING_PLAN.md` M7。

- 官方仓库：`repro/graphrp/`（https://github.com/overwenyan/GraphRP-KDD2026）
- 固定提交：`38b00ecd2cc404461cec176051fd62efd01acd9c`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[GRAPHRP_REPRO_LOG.md](GRAPHRP_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/05-data-mining-security/23_GraphRP_KDD2026.pdf`
- 读书笔记：`paper/notes/23_graphrp.md`
- 运行产物：`results/graphrp/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `dtgb`；echo blocked |
| 数据 | TU 数据集（MUTAG 等），代码到位后由 PyG TUDataset 加载。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_graphrp_full.sh`（默认 dry-run） |

对照目标：MUTAG / ENZYMES 等图分类上的 clone acc ↓ 与 benign acc ↑。与 41 二选一全量。

## 烟雾（短）

```bash
echo 'BLOCKED: 仓库无源码'
```

预处理结论：源码未发布。全量脚本会拒绝执行。

## 全量（默认不跑）

```bash
bash repro/run_graphrp_full.sh          # 只打印命令
FULL=1 bash repro/run_graphrp_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
