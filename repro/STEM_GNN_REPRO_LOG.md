# STEM_GNN 复现日志

论文：*Generalizing GNNs with Tokenized Mixture of Experts*，KDD 2026。论文库编号 12。
官方代码：https://github.com/GXG-CS/STEM-GNN
本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/12_STEM-GNN_KDD2026.pdf`
读书笔记：`paper/notes/12_stem_gnn.md`
学习模块：`LEARNING_PLAN.md` M7

约定：日志只追加。官方仓库 `repro/stem_gnn/`。产物 `results/stem_gnn/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：先 finetune Cora 节点任务；预训练 `pretrain.py --pretrain_dataset all` 很重，有 ckpt 则跳过

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`8995878ca0df9f1fcaedca49d3a45a44ec8403c2`
- 克隆：`bash scripts/clone_official_repo.sh stem_gnn GXG-CS/STEM-GNN`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`stem_gnn`
- 安装：`bash scripts/setup_stem_gnn_conda.sh`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- Cora 等放 `repro/stem_gnn/STEM-GNN/data/`。
- 下载脚本：见 `repro/download_stem_gnn.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. environment.yml 是整机导出（CUDA 11.6、graph-tool、transformers、deepspeed），**禁止 conda env create -f 原文件**。
2. 入口在子目录 STEM-GNN/。`--use_params` 读 config/*.yaml。
3. 数据放 STEM-GNN/data，权重 STEM-GNN/ckpts。
4. setup 脚本只装最小依赖，不复现官方巨型 yml。

## 2026-09-12 步骤 5：烟雾测试

- 未创建 `stem_gnn` conda（禁止官方 `environment.yml`；也不往 dtgb 装 pytorch_lightning）。
- dtgb：`from model.encoder import Encoder` 成功。`from model.vq import VectorQuantize` 缺 `einops`。`from dataset.process_datasets import get_finetune_graph` 缺 `pytorch_lightning`（模块顶层就 import WandbLogger）。官方 `finetune.py` 因此无法启动。
- 数据：`STEM-GNN/dataset/data/single_graph/Cora/cora.pt` 6898749 bytes，SHA-256 `80bf9563cf56f1d9c0b2456331760ab52f3b45f113b2d7f62b20a3ac5b521b6d`。PyG Data：2708 点、特征 `(2708, 384)`、边 `(2, 10858)`、7 类。官方 `data_path` 指向 `STEM-GNN/../data`（即 `repro/stem_gnn/data`），该目录不存在；OFA 布局另要 `get_task_constructor`。
- Encoder.forward（CPU，隐藏 GPU）：`MySAGEConv.propagate(..., xe=edge_attr)` 被 PyG 2.8 拒绝（`unexpected keyword argument 'xe'`）。未改官方代码。
- 无 `ckpts/pretrain_model`；默认 `--pretrain_dataset all` 会 FileNotFoundError。即便补包，烟雾也必须 `--pretrain_dataset na --finetune_epochs 2 --repeat 1 --debug`。
- **未开训。阻塞：dtgb 缺 lightning/einops，且预处理不建 stem_gnn 环境。**

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_stem_gnn_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
