# PUMA 复现日志

论文：*PUMA: Efficient Continual Graph Learning with Graph Condensation*，TKDE 2025。论文库编号 31。
官方代码：https://github.com/superallen13/PUMA
本地论文：`papers/gnn-frontier-2025-2026/08-ccf-journals/31_PUMA_TKDE2025.pdf`
读书笔记：`paper/notes/31_puma.md`
学习模块：`LEARNING_PLAN.md` M2

约定：日志只追加。官方仓库 `repro/puma/`。产物 `results/puma/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：Table 2 class-IL：CoraFull / arxiv / reddit / products，指标 AP / mAP / AF

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`9e4e87f53db0da6aacad4a0a9d08f1c2970413d0`
- 克隆：`bash scripts/clone_official_repo.sh puma superallen13/PUMA`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`puma`
- 安装：`bash scripts/setup_puma_conda.sh`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- CoraFull：PyG 实际拉取 graph2gauss `cora.npz`（不是 cora_full.npz）。`bash repro/download_puma.sh` 经 ghfast。
- SHA-256：`62e054f93be00a3dedb15b7ac15a2a07168ceab68b40bf95f54d2289d024c6bc`
- 处理后：19793 点 / 126842 边 / 8710 维 / 70 类，根目录 `repro/puma/data/cora/`。
- arxiv/reddit/products 预处理不拉。

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 官方环境 Python 3.8 + torch 1.13.0 + pyg 2.2.0 + ogb 1.3.6。
2. table2.sh 对四个数据集循环，budget 写死；`--repeat 5`。
3. wandb 默认关。`--device cuda:0`。
4. CoraFull / Reddit 走 PyG；arxiv/products 走 OGB。
5. 全量 table2 小时级；烟雾用 `--cgl-method bare --cls-epoch 1 --repeat 1 --dataset-name corafull`。

## 2026-09-12 步骤 5：烟雾测试

- 数据已就绪（CoraFull 19793/70）。`progressbar2`、`quadprog` 已装进 dtgb（utilities 无条件 import GEM）。
- 烟雾命令（注意必须有 `python train.py`；`run_puma.sh` 写死 `--env puma`，puma conda 未建，改走 dtgb wrap）：

```
bash scripts/repro_wrap.sh --paper puma --env dtgb --repo repro/puma --cwd repro/puma --label smoke_bare_corafull -- python train.py --dataset-name corafull --cgl-method bare --cls-epoch 1 --repeat 1 --evaluate --device cuda:0
```

- 已排进 `repro/run_remaining_gpu_smokes.sh`。GPU 上跑完：退出码 **0**，13 秒。CoraFull `--cgl-method bare --cls-epoch 1 --repeat 1`。末任务 AP 1.62，汇总 `AP: 1.6±nan` / `mAP: 15.2±nan` / `AF: -5.7±nan`（`ddof=1` + 单 repeat 为 nan）。**不对论文**。日志 `results/puma/runs/20260912_194532_smoke_bare_corafull_pid133724.log`。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_puma_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
