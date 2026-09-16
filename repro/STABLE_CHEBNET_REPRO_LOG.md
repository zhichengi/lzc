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

---

## 2026-09-16 步骤 3 补：Peptides-func 真实数据获取（解除 Dropbox 阻塞）

步骤 5 的烟雾用的是占位图，原因是 Dropbox 不可达。本次重新排查并解除该阻塞。

### 网络实测

| 主机 | 结果 |
|------|------|
| `www.dropbox.com` | **超时**（IPv4/IPv6 均不可达） |
| `hf-mirror.com` | 200 |
| `raw.githubusercontent.com` / `api.github.com` | 200 |
| `ghfast.top` / 清华 PyPI | 200 |

结论：Dropbox 依旧不通，但 **HuggingFace 镜像可用**，可绕过官方下载。

### 两个数据来源

1. `LRGB/peptides-functional` → `geometric_data_processed.pt`
   - 大小 360,910,393 字节；SHA-256 `0a5fe87d60098750b5c1cd87d9ff381ae32b254d7fd3628391075cee792db1fd`
   - 识别为 **原始 LRGB 加载器的 processed 产物**：`torch.load` 得到 `(Data, slices)` 元组，
     `data.keys() = ['edge_index','x','edge_attr','y']`，`n_graphs = 15,535`。
     `x:[2344859,9]`、`edge_index:[2,4773974]`、`edge_attr:[4773974,3]`、`y:[15535,10]`，
     与论文 Table 1 的 Peptides-func 统计完全一致。
2. `scikit-fingerprints/LRGB_Peptides-func` → `lrgb_splits_peptides_func.json`
   - 大小 97,675 字节；SHA-256 `39ca1b1400761460c381fa407a234881bb617c8df06f7bd39fe11c70fcf85b14`
   - 划分索引：`train=10,873`、`valid=2,331`、`test=2,331`（合计 15,535）。
     README 标注 "Recommended split: stratified random"，引用 LRGB 原论文。

**为什么这两份能拼起来**：官方 LRGB 的 `PeptidesFunctionalDataset.process()` 就是
对同一份 CSV（`peptide_multi_class_dataset.csv.gz`）逐行调用 `smiles2graph` 后 `collate`，
所以 `geometric_data_processed.pt` 的图顺序就是 CSV 行序；而 split json 索引的正是那份 CSV。

### 校验（两项，都可独立复算）

1. **图顺序校验（决定性）**：把 CSV 每行的 10 个标签与 processed 的 `y[i]` 逐一对比较，
   **15,535 行全部一致，0 处不匹配** → 图顺序 == CSV 行序，split 索引可直接套用。
2. **划分完整性**：train/valid/test 三个索引集**两两不相交**，并集恰好等于 `0..15534`。
3. **分层性校验**：10 个标签的正例率在三个 split 间的最大绝对差为 **0.003**
   （如 antimicrobial 0.6272/0.6281/0.6268），符合" stratified random"的预期。

### 还原为 PyG 需要的 raw 分片

新增 `repro/build_stable_chebnet_peptides.py`：按 `__cat_dim__` 从 collated 张量切片还原每张图
（`x`/`y`/`edge_attr` 沿 dim 0，`edge_index` 沿 dim 1），写成
`raw/{train,val,test}.pt`，每项为 `(x, edge_attr, edge_index, y)`，`y` 形状 `[1,10]`
（与 PyG `LRGBDataset` 文档一致）。

| split | 图数 | 节点数 | 边数 |
|-------|------|--------|------|
| train | 10,873 | 1,647,684 | 3,354,790 |
| val | 2,331 | 348,441 | 709,242 |
| test | 2,331 | 348,734 | 709,942 |
| **合计** | **15,535** | **2,344,859** | **4,773,974** |

合计与 LRGB 论文 Table 1 的 `15,535 / 2,344,859 / 4,773,974` **逐项吻合**。
旧的占位 `processed/` 已删除，由 PyG 从 raw 重新处理。

`LRGBDataset` 加载核对：`train n=10873`、`val n=2331`、`test n=2331`，
`num_node_features=9`、`num_classes=10`；三个 split 的首个样本节点数与划分索引一致
（test[0]=0→119 节点、train[0]=1→338 节点、val[0]=6→228 节点）。

### 可重跑入口

`repro/download_stable_chebnet.sh` 已改写：走 `hf-mirror`，缓存到
`repro/stable_chebnet/data_cache/` 并记录 SHA-256，再调用上述构建脚本。
整个流程不需要 Dropbox。数据与缓存均在 `.gitignore`（`repro/stable_chebnet/`）内。

### 已知不确定项

split 来自 scikit-fingerprints 镜像，**不是**直接取自官方 Dropbox 的
`splits_random_stratified_peptide.pickle`（官方 MD5 `5a0114bdadc80b94fc7ae974f13ef061`）。
现有证据是"尺寸精确一致 + 分层性成立 + 索引完整分割"，**尚未逐位比对官方 pickle**。
若后续 Dropbox 可达，应下载该 pickle 并核 MD5，以完全排除划分差异。

## 2026-09-16 步骤 5 补：真实数据烟雾（Peptides-func，2 epoch）

```bash
export WANDB_MODE=offline
bash repro/run_stable_chebnet.sh smoke_peptides_real_2ep -- \
  bash -c 'cd Peptides/Stable && python ChebStable_peptide.py --epochs 2'
```

- 日志：`results/stable_chebnet/runs/20260916_205008_smoke_peptides_real_2ep_pid617657.log`
- 退出码 **0**，用时 39 秒；环境 `dtgb`，GPU RTX 3090
- 可训练参数：**659,069**（对比占位图那次 11,054，说明这次吃到了 `config_StableCheb.json` 的 `hidden=145`）
- Epoch 000：Train AP 0.2638，Val AP 0.3564
- Epoch 001：Train AP 0.3534，Val AP 0.4144；Test AP 0.40043

**这只是 2 epoch 的管线检查，不能与论文比较**（官方配置 `epochs=200`）。

顺带核实的两个实现细节（供步骤 4 审计补充）：

1. `config_StableCheb.json` 里 `pos_enc="None"`，因此 `model_euler.py` 走 `dim=9` 分支，
   不访问 `data.lap_pe`；脚本里 `AddLaplacianEigenvectorPE` 只是构造未使用。
2. 损失用 `nn.CrossEntropyLoss()` 作用在 `y`（形状 `[B,10]`）上，即把它当作软标签处理，
   与论文的 10 路多标签 AP 口径存在偏差；这一点留待步骤 6/7 再判定。

## 步骤 6–11

未开始。数据阻塞已解除，可以 `FULL=1 bash repro/run_stable_chebnet_full.sh` 启动官方原样
（`epochs=200`）；完成后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。

---

## 2026-09-16 步骤 6：官方原样全量（Peptides-func，200 epoch）

```bash
export WANDB_MODE=offline
bash repro/run_stable_chebnet.sh official_peptidesfunc_r1_200ep -- \
  bash -c 'cd Peptides/Stable && python ChebStable_peptide.py'
```

- 日志：`results/stable_chebnet/runs/20260916_205200_official_peptidesfunc_r1_200ep_pid618299.log`
- 提交 `7d7a7e2696119891d277fd3fa2b32fdda454b814`（未改官方代码）；环境 `dtgb`；RTX 3090
- 退出码 **0**，用时 **3329 秒（55.5 分钟）**，200/200 epoch 全部完成
- 可训练参数 659,069；配置取官方 `config_StableCheb.json`（`hidden=145, K=10,
  num_layers=3, lr=1e-3, step_size=0.45, seed=99`）

### 结果

| 指标 | 我们（1 run） | 论文 Table 5 |
|------|---------------|--------------|
| peptides-func **AP** | **67.869** | **70.32 ± 0.26** |
| 差值 | — | **−2.45** |
| Train AP（末 epoch） | 95.15 | — |
| Val AP（末 epoch） | 69.756 | — |
| Val AP（最佳，epoch 77） | **70.35** | — |

补充：Val AP 在前 30 epoch 快速升到 ~0.65，之后长期停在 0.69–0.70；Train AP 单调升到
95%。即**已过拟合，val 早已饱和**。

### 步骤 6 发现的两个实现细节（作为步骤 7 的线索）

1. **测试用的是最后一个 epoch 的模型，不是最佳 val 模型。**
   `ChebStable_peptide.py:195` 的 `torch.save(model.state_dict(), checkpoint_path)`
   与 `:206-207` 的 `torch.load` / `load_state_dict` **全部被注释掉**。
   脚本只维护 `temp`（最佳 val）与 `when`（对应 epoch）两个变量用于打印，不影响测试。
   因此 Test AP 与 Val AP 不是同一模型：末 epoch Val AP 69.756 vs 最佳 70.35。
2. **日志把 AP 印成 "Acc"。** `eval_ap()` 用 sklearn `average_precision_score`
   对 10 个任务取平均，确实是论文口径的 AP；打印标签 `Test Acc:` 是命名错误。

### 与论文的差距（−2.45 AP）的可能来源（未逐项验证）

1. **单 run vs 多 seed**：本次 1 次（`seed=99`，官方配置），论文报 ±0.26，说明是多 seed；
   我们的观测里 val AP 在 0.69–0.70 之间波动约 ±0.5，量级与差距相当。
2. **末 epoch 评测**：若改用最佳 val（epoch 77）的模型，预期会略好（Val AP 70.35）。
3. **损失函数**：脚本用 `nn.CrossEntropyLoss()` 作用于 `y`（形状 `[B,10]`），
   即把多标签当作互斥分类的软标签；LRGB 的 Peptides-func 标准做法是 **BCEWithLogitsLoss**
   （10 个独立二分类）。这会改变优化目标。
4. **划分来源**：见步骤 3 的待确认项（取自镜像，未逐位比对官方 pickle）。
5. **无 PE 的对照口径**：论文强调 Stable-ChebNet 不依赖位置编码；脚本 `pos_enc="None"`
   确实没用 PE，这一点与论文一致。

### 分层判定（步骤 6 阶段，先不定稿）

- **L1 管线闭环：是**。真实 LRGB 数据（规模与论文 Table 1 逐项吻合）、200 epoch 跑完、
  退出码 0、日志含 commit/环境/GPU、同命令可重跑。
- **L2 数值量级：部分**。单 run 67.87 对 70.32 ± 0.26，差 −2.45，超出论文 σ；但差距
  有两条已定位的候选原因（末 epoch 评测、损失函数口径），尚需步骤 7 的对照实验判定。
- **L3 统计一致：未评估**。本次只有 1 个 seed，未做多种子。

### 下一步（步骤 7）

优先级从高到低：

1. 做"最佳 val 模型 vs 末 epoch 模型"的对照（不改官方默认路径，用独立脚本/开关复现
   checkpoint 逻辑），量化第 1 点的影响。
2. 查官方是否有 BCE 版本的脚本或说明（第 2 条损失口径），确认论文实际用法。
3. 若需多种子，用 `--seed` 跑 3–5 次，报告均值±std 再对 70.32 ± 0.26。

**未做**：Peptides-struct（`ChebStable_Struc.py`）、Barbell、GraphProp；多种子。
