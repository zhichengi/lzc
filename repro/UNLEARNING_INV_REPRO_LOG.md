# UNLEARNING_INV 复现日志

论文：*Unlearning Inversion Attacks for Graph Neural Networks*，WSDM 2026。论文库编号 41。
官方代码：https://github.com/QwQ2000/WSDM26-Graph-Unlearning-Inversion
本地论文：`papers/gnn-frontier-2025-2026/10-wsdm/41_UnlearningInversion_WSDM2026.pdf`
读书笔记：`paper/notes/41_unlearning_inv.md`
学习模块：`LEARNING_PLAN.md` M7

约定：日志只追加。官方仓库 `repro/unlearning_inv/`。产物 `results/unlearning_inv/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：Cora 上 Inversion + GIF；README 示例 num_runs=5。与 23 二选一全量。

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`3bfc1f17e82a3a9fad9b1cc3ef28281a1323ea16`
- 克隆：`bash scripts/clone_official_repo.sh unlearning_inv QwQ2000/WSDM26-Graph-Unlearning-Inversion`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`dtgb`
- 安装：`echo reuse dtgb`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- Planetoid Cora，PyG 默认路径。可复用已有下载。
- 下载脚本：见 `repro/download_unlearning_inv.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 官方声明 python 3.6 + torch 1.9；先试 dtgb。
2. `--cuda` 默认 **2**，本机必须传 `--cuda 0`。
3. 改编自 GIF-torch。可能需要 METIS。
4. 烟雾：`--num_epochs 2 --num_runs 1`。

## 2026-09-12 步骤 5：烟雾测试

- Cora 原始文件已放入 `repro/unlearning_inv/temp_data/raw_data/cora/raw/`（Planetoid / ghfast）。
- GPU 命令：`python main.py --dataset_name cora --target_model GCN --exp Inversion --method GIF --unlearn_ratio 0.05 --attack_method trend_steal --num_runs 1 --num_epochs 2 --cuda 0 --is_gen_unlearn_request True --is_gen_unlearned_probs True`
- 退出码 **1**。dtgb Python 3.10 无法解析官方 `exp/exp_GIF.py:145` 与 `lib_gnn_model/node_classifier.py:229` 的嵌套引号 f-string（`f'...{self.args['unlearn_ratio']}...'`，需 Python 3.12）。日志 `results/unlearning_inv/runs/20260912_194555_smoke_cora_pid134054.log`。
- 兼容补丁 `repro/patches/unlearning_inv-py310-fstring.patch`（SHA-256 `64b8f56d324f150e6169cb60cf76efbd7e05330ac7a2c3b4de9bf97916eb62d7`）：仅把外层单引号改成双引号，语义不变。
- 打补丁后同一命令退出码 **0**，8 秒。Attack Combined AUC 0.7369（2 epoch，**不对论文**）。日志 `results/unlearning_inv/runs/20260912_195316_smoke_cora_py310_pid136742.log`。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_unlearning_inv_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
