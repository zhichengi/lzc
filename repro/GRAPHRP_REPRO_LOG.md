# GRAPHRP 复现日志

论文：*Defending against Model Extraction for GNNs with Model Reprogramming*，KDD 2026。论文库编号 23。
官方代码：https://github.com/overwenyan/GraphRP-KDD2026
本地论文：`papers/gnn-frontier-2025-2026/05-data-mining-security/23_GraphRP_KDD2026.pdf`
读书笔记：`paper/notes/23_graphrp.md`
学习模块：`LEARNING_PLAN.md` M7

约定：日志只追加。官方仓库 `repro/graphrp/`。产物 `results/graphrp/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：MUTAG / ENZYMES 等图分类上的 clone acc ↓ 与 benign acc ↑。与 41 二选一全量。

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`38b00ecd2cc404461cec176051fd62efd01acd9c`
- 克隆：`bash scripts/clone_official_repo.sh graphrp overwenyan/GraphRP-KDD2026`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`dtgb`
- 安装：`echo blocked`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- TU 数据集（MUTAG 等），代码到位后由 PyG TUDataset 加载。
- 下载脚本：见 `repro/download_graphrp.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 克隆后**只有 README.md**。README 描述的 train_defense.py / models / configs 均不存在。
2. 无法烟雾、无法全量，直到作者推送源码。
3. 记录 blocker，不要手写一份“按论文实现”冒充官方。

## 2026-09-12 步骤 5：烟雾测试

- 计划命令：

```
echo 'BLOCKED: 仓库无源码'
```

- 预处理结论：源码未发布。全量脚本会拒绝执行。
- `bash repro/run_graphrp.sh smoke -- python train_defense.py` 退出码 3：仓库无源码，入口拒绝启动。全量同样拒绝。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_graphrp_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
