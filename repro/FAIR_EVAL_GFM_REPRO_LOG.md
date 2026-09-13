# FAIR_EVAL_GFM 复现日志

论文：*A Fair Evaluation of Graph Foundation Models for Node Property Prediction*，ICML 2026 Workshop。论文库编号 08。
官方代码：https://github.com/yandex-research/gnn-fair-evaluation
本地论文：`papers/gnn-frontier-2025-2026/01-graph-foundation-models/08_FairEval_GFM_ICML2026Workshop.pdf`
读书笔记：`paper/notes/08_fair_eval_gfm.md`
学习模块：`LEARNING_PLAN.md` M6

约定：日志只追加。官方仓库 `repro/fair_eval_gfm/`。产物 `results/fair_eval_gfm/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：GraphLand 上的 GNN 基线；GFM 数字来自各官方仓。本仓库只用 uv 复现 GNN 部分。

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`0a388f087773258e8f2559d801129dfe87adb3bc`
- 克隆：`bash scripts/clone_official_repo.sh fair_eval_gfm yandex-research/gnn-fair-evaluation`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`gfm`
- 安装：`bash scripts/setup_gfm_uv.sh`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- https://zenodo.org/records/16895532 下载解压后 `ln -s <path> repro/fair_eval_gfm/data`
- 下载脚本：见 `repro/download_fair_eval_gfm.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 强制 Python 3.12.9 + uv；torch==2.4.0、dgl==2.4.0，不能塞进 dtgb。
2. 数据 GraphLand：Zenodo 16895532，需 symlink `data/`。
3. 仓库已含实验报告；重跑必须 `--force`。
4. GFM 方法不在本仓，链到 AnyGraph / GraphPFN / EquivarianceEverywhere 等。

## 2026-09-12 步骤 5：烟雾测试

- GraphLand 只拉 `tolokers-2.zip`（Zenodo 16895532，3.2MB）到 `repro/fair_eval_gfm/data/tolokers-2/`。
- `uv` 0.12.13；`uv sync --managed-python --no-dev` 退出 0。Python 3.12.9 + torch 2.4.0 + dgl 2.4.0+cu124。日志 `results/fair_eval_gfm/uv_sync.log`。
- 短配置 `results/fair_eval_gfm/smoke/evaluation.toml`（n_steps=2，n_seeds=1，无 amp_dtype；官方只认 bfloat16/float16 字符串）。
- 命令：`CUDA_VISIBLE_DEVICES="" uv run --offline bin/go.py results/fair_eval_gfm/smoke/evaluation.toml --n_seeds 1 --ensemble_size 0 --force`
- Device cpu。2 step val 0.306 / test 0.290。退出码 0。不对论文。
- 记录 `results/fair_eval_gfm/runs/20260912_185729_smoke_tolokers2.txt`。
- `run_fair_eval_gfm.sh` 仍写死 conda `gfm`，烟雾用 uv 未走该入口。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_fair_eval_gfm_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
