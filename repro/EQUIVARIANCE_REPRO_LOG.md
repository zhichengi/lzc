# EQUIVARIANCE 复现日志

论文：*Equivariance Everywhere All At Once: A Recipe for Graph Foundation Models*，NeurIPS 2025。论文库编号 01。
官方代码：https://github.com/benfinkelshtein/EquivarianceEverywhere
本地论文：`papers/gnn-frontier-2025-2026/01-graph-foundation-models/01_EquivarianceEverywhere_NeurIPS2025.pdf`
读书笔记：`paper/notes/01_equivariance.md`
学习模块：`LEARNING_PLAN.md` M6

约定：日志只追加。官方仓库 `repro/equivariance/`。产物 `results/equivariance/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：trainset1：Cora 训练、其余图测试。与 04 二选一做全量。

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`1dfe3870fd8a0de7e15db6958289661b2cabdc37`
- 克隆：`bash scripts/clone_official_repo.sh equivariance benfinkelshtein/EquivarianceEverywhere`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`gfm`
- 安装：`bash scripts/setup_gfm_uv.sh  # 或独立 conda equivariance`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- 脚本内下载多图节点分类基准；全量前应预下载并离线。
- 下载脚本：见 `repro/download_equivariance.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 官方 Python 3.10 + torch 2.3.0+cu118 + pyg 2.5.3；另要 neptune、triton。
2. 必须在仓库根目录启动 main.py。
3. README 让装 neptune；代码里需确认是否硬依赖（全量前审计 experiment.py）。
4. best config 的 max_epochs 达 2000。烟雾必须显式 --max_epochs 2。

## 2026-09-12 步骤 5：烟雾测试

- dtgb 已能 `import neptune`（1.14.0.post2）。`API_TOKEN` 仍是占位 `"..."`；烟雾用 `NEPTUNE_MODE=offline`，并必须给 `--project`（官方 argparse required）。
- Triton 在 dtgb 为 2.2.0；`GNNType.uses_triton()` 对 GAT 与 MEAN_GNN 均为 True。
- Planetoid Cora 已放到 `repro/equivariance/datasets/cora/cora/raw/`。
- `run_equivariance.sh` 写死 `--env gfm`；烟雾走 dtgb wrap。
- 第一次 follow-up waiter 未激活 conda，wrap 探活 `import torch` 失败，退出 1。日志 `results/equivariance/runs/20260912_194608_smoke_gat_cora_2ep_pid134203.log`。
- 第二次（conda activate dtgb 后）：neptune offline 初始化成功，随后 `RemoveSelfLoops` 在 PyG 2.8 不能实例化（缺 `forward`）。日志 `..._194701_...`。
- 兼容补丁 `repro/patches/equivariance-pyg28-transform.patch`（SHA-256 `45b89aaa260139eb51e1fc4dae6769fd9dd64539fc4cc4228b1fd7730f574788`）：`BaseTransform.__call__`→`forward`（4 个 transform），以及 `triton_nn` 解析 `2.8.0.post1`。数据加载与 GAT.propagate 已过。
- 第三次训练在 Triton JIT：`Failed to find C compiler`（本机无 `gcc`/`cc`）。退出码 **1**。日志 `results/equivariance/runs/20260912_195250_smoke_gat_cora_2ep_pyg28_pid136448.log`。未装系统编译器。数字未出。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_equivariance_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
