# CORE_GRAPHRAG 复现日志

论文：*Core-based Hierarchies for Efficient GraphRAG*，KDD 2026。论文库编号 22。
官方代码：https://github.com/erdemUB/KDD26
本地论文：`papers/gnn-frontier-2025-2026/04-graphrag-llm/22_CoreGraphRAG_KDD2026.pdf`
读书笔记：`paper/notes/22_core_graphrag.md`
学习模块：`LEARNING_PLAN.md` M8

约定：日志只追加。官方仓库 `repro/core_graphrag/`。产物 `results/core_graphrag/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：只做 k-core 层次 / RkH·M2hC·MRC vs Leiden 的算法可复现性；LLM 查询不做

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`37a81bc38b0c5b5836c51d73d1f795a5b438407e`
- 克隆：`bash scripts/clone_official_repo.sh core_graphrag erdemUB/KDD26`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`dtgb`
- 安装：`echo optional pip install pytest in dtgb`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- Kevin Scott podcast 等来自 GraphRAG benchmarking datasets；算法烟雾不需要语料。
- 下载脚本：见 `repro/download_core_graphrag.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 基于 Microsoft GraphRAG v2.7.0 评测框架；index/query 需要 API key。
2. 本计划只复现社区构造算法侧。单元测试在 tests/unit 与 tests/smoke。
3. 安装 `pip install -e ./graphrag` 可能与 dtgb 冲突，全量前再决定是否新建 env。
4. community 算法名：RkH / M2hC / MRC。

## 2026-09-12 步骤 5：烟雾测试

- 官方 pytest：`dtgb` 无 pytest，且 `kcore_cluster_graph.py` 顶层 `import graspologic` / `plotly`。未往 dtgb 装 GraphRAG+OpenAI。
- 算法烟雾（CPU）：`python results/core_graphrag/smoke_kcore.py`，对 `graspologic.partition.leiden` 与缺失的 plotly 做了桩，调用官方 `kcore_cluster_graph(..., cluster_type="RkH")`。
- 图：networkx `karate_club_graph()`（34 点 / 78 边）。RkH 返回 8 个 community tuple。
- 退出码 0。日志 `results/core_graphrag/runs/20260912_183825_smoke_kcore_pid105786.log`。不是 LLM 检索，不能对论文查询指标。
- `use_lcc=False`，避免桩掉的 `graspologic.utils.largest_connected_component`。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_core_graphrag_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
