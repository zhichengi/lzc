# MAVN 复现日志

论文：*Learn When and Where to Connect: Adaptive Virtual Nodes for Dynamic Message Passing on Graphs*，KDD 2026。论文库编号 13。
官方代码：https://github.com/bdi-lab/MAVN
本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/13_MAVN_KDD2026.pdf`
读书笔记：`paper/notes/13_mavn.md`
学习模块：`LEARNING_PLAN.md` M5

约定：日志只追加。官方仓库 `repro/mavn/`。产物 `results/mavn/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：Peptides-func AP（seed 0–3）；PascalVOC-SP；minesweeper / tolokers 10 split。附录 PDF：Setup_MAVN_KDD2026.pdf

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`3773c40a753a08528aa73c641c4f991ba4cfd4e5`
- 克隆：`bash scripts/clone_official_repo.sh mavn bdi-lab/MAVN`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`dtgb`
- 安装：`echo reuse dtgb first`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- minesweeper：`https://ghfast.top/https://github.com/yandex-research/heterophilous-graphs/raw/refs/heads/main/data/minesweeper.npz`
- 下载：`bash repro/download_mavn.sh minesweeper`
- SHA-256：`e664c8dacf1e8ac466c2c09ed4b237bd2c5541f47a6eae9c6092cb87f16412b3`
- 加载核验：10000 点，78804 边（含双向化），10 split 的 split 0。
- Peptides-func / PascalVOC-SP Dropbox 大文件预处理不拉。

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 官方 Python 3.9.19 + torch 2.0.1+cu117。requirements 很短，其余在 PDF。
2. 两个入口：train.py（TunedGNN 风格）与 train_v2.py（heterophily 风格）。
3. Peptides 要改 val.pt→valid.pt；数据放 ./datasets/。
4. 命令极长，必须原样复制 README，只改 --num_epoch 做烟雾。
5. 许可证 CC BY-NC-SA 4.0。

## 2026-09-12 步骤 5：烟雾测试

- minesweeper npz：`bash repro/download_mavn.sh minesweeper`，SHA-256 `e664c8dacf1e8ac466c2c09ed4b237bd2c5541f47a6eae9c6092cb87f16412b3`。
- 数据加载（CPU，`--pe None`）：10000 点 / 78804 边 / 2 类，split0 train 5000 / val 2500 / test 2500，特征 `(10000, 7)`。dtgb 可 import `Heterophily_Dataset`。
- 训练烟雾（官方 README 命令，只改 `--num_epoch 2`，加 `--no_write`）在 GPU 上跑完：退出码 **0**，5 秒。minesweeper 10000 点 / 78804 边，392463 params。Epoch 1/2 Task Loss 0.817→0.813。`Best Valid AUCROC:0`（2 epoch 未出有效 val）。**不对论文**。日志 `results/mavn/runs/20260912_194547_smoke_minesweeper_2ep_pid133905.log`。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_mavn_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
