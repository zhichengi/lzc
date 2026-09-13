# MF_GIA 复现日志

论文：*Modality-Free Graph In-context Alignment*，ICLR 2026。论文库编号 04。
官方代码：https://github.com/JhuoW/MF-GIA
本地论文：`papers/gnn-frontier-2025-2026/01-graph-foundation-models/04_MF-GIA_ICLR2026.pdf`
读书笔记：`paper/notes/04_mf_gia.md`
学习模块：`LEARNING_PLAN.md` M6

约定：日志只追加。官方仓库 `repro/mf_gia/`。产物 `results/mf_gia/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：ICL 节点分类：Cora k-shot。预训练 8000 epoch，优先用仓库 checkpoint。

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`9b2946d13af0372323b5e3f3105d822757a87cd9`
- 克隆：`bash scripts/clone_official_repo.sh mf_gia JhuoW/MF-GIA`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`gfm`
- 安装：`conda create -n mf_gia python=3.12 -y  # 见 README，暂不执行`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- 按 README 组织 datasets/；OFA 原始文件来自 https://github.com/LechengKong/OneForAll
- 下载脚本：见 `repro/download_mf_gia.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 官方 conda python 3.12.2；torch 2.6.0+cu124，与 dtgb 不兼容。
2. 数据目录结构严格（OFA / pyg SingleTextGraph）。缺文件会在预训练才爆。
3. configs 里 gpu 默认可能是 1；本机只有 0。
4. wandb 监控；num_workers 可能触发 too many open files。
5. generated_files/checkpoints 若在克隆中，全量应先评测 checkpoint 而非重训。

## 2026-09-12 步骤 5：烟雾测试

- 仓库自带 lightning ckpt 与 `generated_files/output/G-Align/Aug13-0:14-97cc0c8c/final_gfm_model.pt`。
- **没有** README 要求的 `datasets/` 目录（ofa / pyg 文本图布局）。ICL 烟雾无法启动。
- 不跑 `pretrain.py`（8000 epoch）。
- 退出码：未开训。阻塞：数据目录未按官方树组织。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_mf_gia_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
