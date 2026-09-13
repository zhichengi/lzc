# GBN 复现日志

论文：*Deeper with Riemannian Geometry: Overcoming Oversmoothing and Oversquashing for Graph Foundation Models*，NeurIPS 2025。论文库编号 09。
官方代码：https://github.com/ZhenhHuang/GBN
本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/09_Riemannian_GBN_NeurIPS2025.pdf`
读书笔记：`paper/notes/09_gbn.md`
学习模块：`LEARNING_PLAN.md` M1

约定：日志只追加。官方仓库 `repro/gbn/`。产物 `results/gbn/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：节点分类（WikiCS / Texas 等）与深层 GCN 对照；仓库预置 configs/NC/CS.json

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`72ad3692916ecc60f2c78d5bd01a55d7c6297a4f`
- 克隆：`bash scripts/clone_official_repo.sh gbn ZhenhHuang/GBN`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`dtgb`
- 安装：`# 复用 dtgb。若 BoundaryGCN / torch-scatter 报错再新建 gbn。
echo 'reuse dtgb'`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- PyG：WebKB / Planetoid / Coauthor / WikiCS / Heterophilous。优先符号链接已有 `repro/sgpc/data/`。Coauthor CS 需另下。
- 下载脚本：见 `repro/download_gbn.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. cwd 依赖：`./datasets` `./configs/{task}/{dataset}.json`；JSON 存在时会覆盖 CLI。
2. seed 写死 `set_seed(3047)`，`exp_iters` 默认 10。
3. 官方 requirements 钉 torch 2.0.0+cu118；本机先试 `dtgb`。
4. 无 wandb。GPU `--gpu` 默认 0。
5. NC 预置配置只有 CS；Cora/Texas 首次运行会**写入**新 json，烟雾后必须删掉以免污染全量。

## 2026-09-12 步骤 5：烟雾测试

- 命令：`bash repro/run_gbn_smoke.sh`（`results/gbn/smoke_texas.json` 含 `layer_wise`，2 epoch；跑完删除 `configs/NC/Texas.json`）
- 日志：`results/gbn/runs/20260912_175331_smoke_texas_pid84650.log`
- 退出码 0；Texas test_acc 10.81%（2 epoch，不对论文）。数据必须链内层 `datasets/texas`，外壳目录会触发 GitHub 下载。
- CLI 不含 `layer_wise`，无 json 时会 AttributeError；全量用仓库预置 `CS.json`。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_gbn_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
