# STABLE_CHEBNET 复现日志

论文：*Return of ChebNet: Understanding and Improving an Overlooked GNN on Long-Range Tasks*，NeurIPS 2025 Spotlight。论文库编号 10。
官方代码：https://github.com/ahariri13/Stable-ChebNet
本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/10_Stable-ChebNet_NeurIPS2025.pdf`
读书笔记：`paper/notes/10_stable_chebnet.md`
学习模块：`LEARNING_PLAN.md` M1,M5

约定：日志只追加。官方仓库 `repro/stable_chebnet/`。产物 `results/stable_chebnet/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：Peptides-func / Peptides-struct（LRGB）；Barbell 与 GraphProp 为合成/属性任务

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`7d7a7e2696119891d277fd3fa2b32fdda454b814`
- 克隆：`bash scripts/clone_official_repo.sh stable_chebnet ahariri13/Stable-ChebNet`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`dtgb`
- 安装：`echo 'reuse dtgb; pip install ogb if missing'`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- Peptides 走 PyG LRGB；不要直连 GitHub，先镜像或本地下好再离线加载。
- 下载脚本：见 `repro/download_stable_chebnet.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 无统一 requirements.txt；依赖 PyG + OGB。GraphProp 入口强制 `import ray`。
2. Barbell 默认 wandb，且 README 用 sbatch。
3. Peptides 脚本把超参写在 py 文件里，无 CLI epoch。
4. 主表应对 LRGB，不要用 Barbell 数字对论文主表。

## 2026-09-12 步骤 5：烟雾测试

- 计划命令（实际）：`WANDB_MODE=offline python ChebStable_peptide.py --epochs 2`（官方脚本已有 `--epochs`，不必改 py）。
- 环境：`dtgb`，wandb 0.19.6 已在 dtgb；`WANDB_MODE=offline`。
- 数据：Dropbox `peptidesfunc.zip` IPv4/IPv6 均 `Network is unreachable`。HuggingFace `LRGB/peptides-functional` 只有 `geometric_data_processed.pt`（361MB），对不上 `LRGBDataset` 的 train/val/test 分片。为跑通官方脚本，写入 **8–16 张占位图**（`peptides-func/README_DUMMY.txt`），**不是** LRGB，不能对论文。
- EulerModel import：11054 params（hidden=32 探测）成功。
- Barbell `layer_type=Cheb`：PyG 2.8 `ChebConv`/`MessagePassing` 拒收 `normalize=`，退出 1。日志 `results/stable_chebnet/runs/20260912_183316_smoke_barbell2ep_pid101912.log`。主表本就不是 Barbell。
- 官方 Peptides 脚本 2 epoch（CPU，隐藏 GPU 以免抢 SGPC）：训练打印 Epoch 000/001，Train AP 0.62→0.80。随后脚本把 `device="cuda"` 写死再 `model.to(device)`，CPU 烟雾退出 1。日志 `results/stable_chebnet/runs/20260912_183549_smoke_peptides_dummy_2ep_pid103999.log`。
- GPU 空闲后同一命令再跑：`WANDB_MODE=offline python ChebStable_peptide.py --epochs 2`。退出码 **0**，8 秒。Epoch 000/001 Train Acc 0.607→0.777，Val Acc 0.536→0.505（占位图，**不对论文**）。日志 `results/stable_chebnet/runs/20260912_194521_smoke_peptides_dummy_2ep_gpu_pid133488.log`。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_stable_chebnet_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
