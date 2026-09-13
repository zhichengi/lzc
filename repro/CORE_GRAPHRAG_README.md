# 22 CORE_GRAPHRAG 预处理 / 复现入口

论文：*Core-based Hierarchies for Efficient GraphRAG*（KDD 2026）。论文库编号 22。学习模块：`LEARNING_PLAN.md` M8。

- 官方仓库：`repro/core_graphrag/`（https://github.com/erdemUB/KDD26）
- 固定提交：`37a81bc38b0c5b5836c51d73d1f795a5b438407e`（分支 `master`，与 `git ls-remote HEAD` 一致）
- 过程日志：[CORE_GRAPHRAG_REPRO_LOG.md](CORE_GRAPHRAG_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/04-graphrag-llm/22_CoreGraphRAG_KDD2026.pdf`
- 读书笔记：`paper/notes/22_core_graphrag.md`
- 运行产物：`results/core_graphrag/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `dtgb`；echo optional pip install pytest in dtgb |
| 数据 | Kevin Scott podcast 等来自 GraphRAG benchmarking datasets；算法烟雾不需要语料。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | **已跑** karate RkH，退出 0（graspologic/plotly 打桩） |
| 全量 | `FULL=1 bash repro/run_core_graphrag_full.sh`（默认 dry-run） |

对照目标：只做 k-core 层次 / RkH·M2hC·MRC vs Leiden 的算法可复现性；LLM 查询不做

## 烟雾（短）

```bash
export CUDA_VISIBLE_DEVICES=""
bash repro/run_core_graphrag.sh smoke_kcore -- python /home/lab_user/project/lzc/results/core_graphrag/smoke_kcore.py
```

pytest 全量单元测试需要 graspologic / 整包 GraphRAG，预处理不做。不要为测算法去装 OpenAI。

## 全量（默认不跑）

```bash
bash repro/run_core_graphrag_full.sh          # 只打印命令
FULL=1 bash repro/run_core_graphrag_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
