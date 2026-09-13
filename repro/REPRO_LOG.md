# GCTD 复现日志

> 当前：Table 2 三个小图格已跑完（建议命令 `--lr_rec 0.01 --edge_topk 12` + 塌缩重试 + 超点配额，10 seed）——
> Cora 1.3% `66.0 ± 9.4`、Citeseer 0.9% `64.9 ± 7.7`、Pubmed 0.08% `77.9 ± 1.5`，
> 论文对应 `81.4 ± 1.6` / `76.8 ± 0.4` / `79.9 ± 0.2`。
> 汇总表：`results/gctd/table2_summary.csv`（Cora 明细见 `cora_summary.csv`）。
> L1 是，L2 部分（Pubmed 差 2.0，Cora/Citeseer 差 10–15），L3 否。**不再在 Cora 上扫参**。
> 入口：[GCTD_README.md](GCTD_README.md)。

记录复现过程中的问题、结论，以及相对官方仓库的重要改动。  
新条目按时间追加，不要改写旧条目。

约定：

- 路径一律写相对工作区根，例如 `repro/gctd/src/train.py`
- 「官方」指 `https://github.com/nicolasrsantos/gctd` 克隆当时的 HEAD

---

## 2026-09-10 搭建与代码审阅

### 环境

- 机器：NVIDIA GeForce RTX 3090，conda `dtgb`（Python 3.10.20，torch 2.2.1+cu121，torch_geometric 2.8.0.post1）
- 官方声明：Python 3.11.5，torch 2.1.2，torch-geometric 2.6.1
- 决定：先在 `dtgb` 上补齐缺失包做管道验证，不另装一套 CUDA 轮子；版本偏差记在本条。若数字对不上论文，再新建 `gctd` 环境对齐钉扎版本。

### 官方代码审阅结论

1. **`wandb.login()` 无条件调用**（`repro/gctd/src/train.py`）。无 W&B 账号时会卡住或失败，无法本地复现。
2. **路径依赖 cwd。** `--data_dir` 默认 `data/`，`save_graph` / `load_cached_data` 写死 `saved_ours/`。从工作区根启动会把数据下到错误位置。
3. **`DataLoader(num_workers=16)` 写死**（`src/utils/utils.py`）。小机器或容器里容易拖垮或报错。
4. **README 与实现不一致。** README 写 ogbn-arxiv 会自动下载；`prepare_data()` 把它归入 GraphSAINT 分支，读 `data/ogbn-arxiv/{adj_full.npz,role.json,feats.npy,class_map.json}`。`PygNodePropPredDataset` 已 import 但从未使用。
5. **`faiss` 包名。** README 写 `faiss==1.9.0`，pip 实际是 `faiss-cpu` / `faiss-gpu`。
6. **训练 loss 累加疑似有误**（`train()` / `eval()` 每个 batch 后执行 `total_loss = total_loss / total_examples`）。未改官方公式，只记录；对「能否跑通」无阻塞。
7. **`--cuda` / `--verbose` / `--use_cached` 的 argparse 写法是 `action="store_true", default="store_true"`**，语义上始终为真。保持原样。

### 重要改动（移植向）

| 文件 | 改动 |
|------|------|
| `repro/gctd/src/utils/paths.py` | **新增**。`resolve_rel_path()` 把相对路径锚定到 `repro/gctd/`。 |
| `repro/gctd/src/utils/args.py` | 增加 `--save_dir`、`--log_file`、`--num_workers`（默认 4）、`--no_wandb`。 |
| `repro/gctd/src/utils/data_handling.py` | `load_data` / `load_cached_data` 走 `resolve_rel_path`。 |
| `repro/gctd/src/utils/utils.py` | `save_graph` 走 `--save_dir`；`num_workers` 可配。 |
| `repro/gctd/src/train.py` | wandb 可关闭并失败回退；stdout/stderr 可 tee 到 `--log_file`。 |
| `repro/run_gctd.sh` | **新增**入口，只用相对路径。 |
| `repro/requirements-gctd.txt` | **新增**额外依赖清单。 |
| `scripts/setup_gctd_env.sh` | **新增**安装脚本。 |

未改模型公式、超参默认值（除 `num_workers` 16→4）和数据增强逻辑。

---

## 2026-09-10 依赖安装

- `conda run -n dtgb bash scripts/setup_gctd_env.sh` 卡住约 13 分钟。原因：`requirements-gctd.txt` 按官方钉扎了 `scikit-learn==1.6.1`，pip 正在拉取大 wheel 覆盖 `dtgb` 已有的 1.4.1。
- 处理：杀掉该进程；清单改为只装缺失包（dotmap / gdown / ogb / tensorly / wandb / faiss-cpu），不再动 sklearn / scipy / torch / pyg。
- 清华镜像安装成功。`dtgb` 现有：faiss-cpu 1.9.0、tensorly 0.9.0、wandb 0.19.6、ogb 1.3.6、dotmap 1.3.30。
- **副作用：** wandb 0.19.6 把 `protobuf` 从 7.36.1 降到 5.29.6，与 `tensorboard 2.21.0`（要求 protobuf>=6.31.1）冲突。GCTD 默认 `--no_wandb`，暂不升级 wandb。若要用根目录 tensorboard，需另处理 protobuf。
- PyPI 官方源下载 tensorly 约 15 kB/s 且超时；改清华源后 6+ MB/s。`scripts/setup_gctd_env.sh` 已改为清华源。

---

## 2026-09-10 Cora 烟雾测试

- PyG `Planetoid` 直连 `github.com/kimiyoung/planetoid` 超时（FSTimeoutError）。
- 用镜像 `https://ghfast.top/` 拉原始文件。注意目录名必须是 **`data/cora/raw`**（与 `Planetoid(root, "cora")` 的 `name.lower()` 一致），写成 `data/Cora/raw` 时 PyG 仍会去 GitHub 下载。
- 新增 `repro/download_planetoid.sh`（相对路径）。
- 烟雾命令：`bash repro/run_gctd.sh cora 0.013 --rec_epochs 2 --gnn_epochs 2 --num_workers 0`
- **结果：管道跑通。** 日志：`results/gctd/runs/20260910_101449_cora.log`
  - 压缩 2 epoch：rec error 30.87 → 12.57，condensation time 2.08 s
  - GNN 2 epoch：test acc **17.80%**（epoch 太少，不能对照论文表；仅验证可运行）
  - `--log_file` 解析为工作区内相对路径 `../../results/gctd/runs/...`（相对 `repro/gctd/`）
  - wandb 已 disabled，未要求登录
- 尚未跑论文设定（rec_epochs=200, gnn_epochs=600）。下一步用同一条命令去掉短 epoch 即可。

---

## 2026-09-10 完整 Cora 1.3%（论文默认 epoch）

对照：论文 Table 2，Cora 1.3%，GCTD **81.4 ± 1.6**（10 次平均）；Full dataset 81.4 ± 0.6。

### 运行 A：CLI 默认

- 命令：`bash repro/run_gctd.sh cora 0.013 --num_workers 0`
- 日志：`results/gctd/runs/20260910_102048_cora.log`
- 压缩：22 epoch 早停（atol=1e-7），rec error 30.4 → 1e-3，耗时 20.9 s
- 合成图 batch：train/val/test = **9 / 500 / 1000**（val/test 仍走原图）
- GNN 600 epoch：训练集 acc **一直卡在 33.33%**，val 约 25–30%
- **test acc 30.20%**（按 val loss 选的最佳 checkpoint）

### 运行 B：按 wandb 注释改 `weighted=0`、`atol=1e-6`

- 命令：`bash repro/run_gctd.sh cora 0.013 --num_workers 0 --weighted 0 --atol 1e-6`
- 日志：`results/gctd/runs/20260910_102156_cora.log`
- 压缩轨迹与 A 几乎相同（同一 seed、同一 cache）
- **test acc 30.40%**，train acc 仍全程 33.33%

### 结论（本轮）

- 管道、相对路径、缓存、无 wandb 均正常；**数字对不上论文**，且超出 10-run 标准差，不是「少跑几次」能解释的。
- 更像合成图/节点分配有问题：9 个训练合成节点都拟合不好（600 epoch 仍 33.33%），不像论文里「接近全图 81%」的小图。
- 可能原因（待查）：官方表格来自 wandb 搜索后的超参，不是 README 默认值；`dtgb` 的 torch 2.2 / pyg 2.8 与官方 2.1.2 / 2.6.1 不一致；K-Means 分配与划分比例（计划约 1/6/12，实际 train=9）不稳定。

---

## 2026-09-10 原因检查

脚本：`repro/diagnose_cora.py`（同 seed 42、同 cache、压缩同样 22 epoch 早停）。

### 直接原因：合成图是完全图，GCN 把特征抹平

| 量 | 数值 |
|----|------|
| 合成节点数 | 35（= ⌊2708×0.013⌋） |
| 边数 | **1225 = 35×35**（含自环） |
| 密度 | **1.0**，每个点度数 35 |
| 核张量平均后 `A^S` | min **0.057**，mean 0.358，max 0.672 |
| 官方二值化 | `new_adj >= 0.05`（写死在 `to_edge_index`，不是 CLI 参数） |

min 已经大于 0.05，所以**所有**条目都变成边。两层 GCN 在完全图上会把所有节点聚成几乎同一表示，分类退化成常数预测。

对照原图 Cora：全局多数类（类 3）占 **30.2%**，测试集多数类 **31.9%**。我们两次 GNN 的 test acc 是 **30.2% / 30.4%**，训练集 acc 卡在 **33.33%**，与「始终预测多数类」一致，而不是「压缩质量差一点点」。

旁证：把图结构拿掉、只用合成节点特征做 Logistic Regression：

- 拟合合成 train：**87.5%**
- 迁到原图 test：**48.7%**（仍高于 30%，说明特征里有信号，是卷积图把信号毁掉了）

阈值若改到 0.50，边数会降到 133（密度 0.11）。这只是诊断，尚未改官方代码重跑。

### 次要问题：合成特征不是「本簇节点平均」

`compute_supernode_info` 里特征取的是**全图中同一 class + 同一 split 的所有节点平均**，不是 K-Means 分到该簇的节点。因此相同 (class, split) 的合成节点特征完全一样：35 个点只有 **16** 种不同特征，8 个 train 点只有 **4** 种。论文文字写的是对 K-Means 分配到的节点取平均，实现与描述不一致。这一条会削弱可解释映射，但单独解释不了 30%——无图 logreg 已经能到 49%。

### 与论文设定的关系

- Table 2 的 81.4% 是 **10 次平均**，且官方 `wandb_example.yml` 会搜 `lr_rec / R / add_ratio` 等；不同 `lr_rec` 可能让核张量更稀疏，0.05 阈值才合理。
- README 默认 `lr_rec=0.001` 时，当前种子下核值下限是 0.057，阈值必然失效。

---

## 2026-09-10 提高阈值 / 扫描 lr_rec

对照仍是 Table 2 Cora 1.3%：**81.4 ± 1.6**。本轮把 `to_edge_index` 的写死 `>= 0.05` 改成 `--edge_thresh`，并加 `--seed`（官方写死 42）。

### 代码改动

| 文件 | 改动 |
|------|------|
| `repro/gctd/src/utils/args.py` | `--edge_thresh`（默认 0.05）、`--seed`（默认 42） |
| `repro/gctd/src/models/gctd.py` | `to_edge_index` 用 `args.edge_thresh`；空边抛错并打印 adj 统计；K-Means `seed` 跟 CLI |
| `repro/gctd/src/train.py` | 先解析 args 再 `set_seed(args.seed)` |

### 结果（Cora 0.013，seed 42 除非另写）

| 标记 | 设定 | 密度 / 边数 | test acc | 日志 |
|------|------|-------------|----------|------|
| C | `edge_thresh=0.5`，默认 `lr_rec=0.001` | 0.1804 / 221 | **41.60%** | `results/gctd/runs/20260910_103126_cora.log` |
| D | `thresh=0.5`，`lr_rec=0.01` | 0 边（max=0.456） | 失败 | `.../20260910_103155_cora.log` |
| **E** | **官方 thresh=0.05，`lr_rec=0.1`** | **0.0098 / 12** | **74.50%** | `.../20260910_103210_cora.log` |
| F | thresh=0.05，`lr_rec=0.01` | 0.9992 / 1224 | 18.20% | `.../20260910_103426_cora.log` |
| G | E + `weighted=0` `atol=1e-6` | 同 E，12 边 | 69.40% | `.../20260910_103446_cora.log` |
| H | E + `lr_gnn=0.01` | 同 E，12 边 | 70.70% | `.../20260910_103500_cora.log` |
| I | F + `weighted=0` `atol=1e-6` | 同 F，近完全图 | 18.50% | `.../20260910_103520_cora.log` |
| J | thresh=0.05，`lr_rec=0.05` | 0 边（max=0.040） | 失败 | `.../20260910_103714_cora.log` |
| K | `thresh=0.02`，`lr_rec=0.1` | 0.6727 / 824 | 72.50% | `.../20260910_103729_cora.log` |
| E0 | E 的设定，`--seed 0` | 0 边（max=0） | 失败 | `.../20260910_103749_cora.log` |
| E1 | E 的设定，`--seed 1` | 12 边，train 仅 4 点 | 31.70% | `.../20260910_103805_cora.log` |
| E7 | E 的设定，`--seed 7` | 0 边（max=0.017） | 失败 | `.../20260910_103818_cora.log` |

C 组 train acc 已能到 100%（不再卡在 33.33%），val 约 49%，说明阈值解开了过平滑，但合成特征种类仍少，GCN 过拟合。

### 结论

1. **根因确认：** README 默认 `lr_rec=0.001` 时核值下限 > 0.05，官方阈值必然得到完全图。把 `lr_rec` 提到 wandb 网格上沿 **0.1** 后，seed 42 下核值落到 0.05 附近，官方阈值才有效。
2. **当前最好：74.50%**（E），比完全图的 30% 高很多，仍低于论文 81.4%，大约差 7 个点（论文 10 次标准差 1.6，单次 74.5 仍偏矮）。
3. **绝对阈值 0.05 对种子极敏感。** 同一 `lr_rec=0.1`：seed 42 出 12 边到 74.5%；seed 0/7 核值上限 ≤ 0.017，0 边直接崩；seed 1 虽有 12 边但 train 合成点只剩 4 个，test 31.7%。无法直接做论文那种 10-run 平均。
4. `lr_rec=0.01` 仍几乎是完全图（1224/1225），阈值必须再抬，或学习率必须到 ~0.1。
5. wandb 注释里的 `weighted=0` / `atol=1e-6` / 更大 `lr_gnn` **没有**超过 E。

剩余差距更可能来自：K-Means 特征仍是「全图同一 class+split 平均」而非簇内平均；绝对阈值不稳定；以及 `dtgb` 的 torch/pyg 版本。

建议复现命令（当前单次最好）：

```bash
bash repro/run_gctd.sh cora 0.013 --num_workers 0 --lr_rec 0.1 --edge_thresh 0.05
```

---

## 2026-09-10 簇内特征平均（论文文字对齐）

官方 `compute_supernode_info` 在选定 (class, split) 后，对**全图**该 class+split 的节点取特征平均。相同 (y, mask) 的超点特征完全一样（先前诊断：35 点只有 16 种特征）。论文文字是对 K-Means 分到该簇的节点取平均。新增 `--feat_from_cluster`（默认 0=官方）。

GCTD 在合成图上训 GCN，但 val/test 走**原图节点**，所以超点特征必须能迁回原图特征空间。

| 标记 | 特征规则 | 设定 | unique_x | test acc | 对照 | 日志 |
|------|----------|------|----------|----------|------|------|
| E | 官方 class+split | `lr_rec=0.1` thresh=0.05 | 16/35 | **74.50%** | — | 上轮 |
| L | 簇内全部节点平均 | 同 E | **35/35** | 31.90% | 多数类 | `results/gctd/runs/20260910_104740_cora.log` |
| M | 簇内全部节点平均 | thresh=0.5 默认 lr | **35/35** | 31.00% | 官方同设定 41.60% | `.../20260910_104836_cora.log` |
| L2 | 簇内同类同 split 平均 | 同 E | **35/35** | 37.60% | E 的 74.50% | `.../20260910_104959_cora.log` |
| M2 | 簇内同类同 split 平均 | thresh=0.5 默认 lr | **35/35** | 35.90% | C 的 41.60% | `.../20260910_105018_cora.log` |

L 把别的类混进超点特征，GCN 在合成图上仍能 100% 拟合，迁回原图 val 掉到 ~30%。L2 只平均簇内同类节点，特征仍全部独特，好于 L，但仍远差于官方 class 原型。

**结论：** 这条「与论文文字对齐」的修改在 Cora 1.3% 上**不能**缩小与 81.4% 的差距；官方的 class+split 原型反而更利于迁回原图。默认改回 `--feat_from_cluster 0`。当前最好仍是 E 的 **74.50%**。

---

## 2026-09-10 相对 / 分位数 / top-k 阈值

绝对 0.05 对核值尺度过敏：`lr_rec=0.1` 时有的种子 max 小于 0.05 直接 0 边。新增三个尺度无关选项（同时给时优先级 topk > quantile > rel > 绝对阈值）：

| 参数 | 含义 |
|------|------|
| `--edge_quantile q` | 阈值 = 核值的 q 分位 |
| `--edge_rel r` | 阈值 = r × adj.max() |
| `--edge_topk k` | 保留最大的 k 条有向边，再补成无向 |

空图时：max 大于 0 则退回 top 1%；核全零则加自环。

### seed 42、`lr_rec=0.1`（对照 E=74.50%，12 边）

| 标记 | 规则 | 边数 / 密度 | test acc | 日志 |
|------|------|-------------|----------|------|
| N | quantile 0.99 | 26 / 0.021 | **74.80%** | `results/gctd/runs/20260910_105649_cora.log` |
| O | quantile 0.95 | 118 / 0.096 | 73.70% | `.../20260910_105708_cora.log` |
| P | rel 0.5 | 275 / 0.225 | 73.70% | `.../20260910_105728_cora.log` |
| **Qk** | **topk 12** | 24 / 0.020 | **75.00%** | `.../20260910_105748_cora.log` |
| R | 默认 `lr_rec=0.001` + q0.99 | 26 / 0.021 | 53.20% | `.../20260910_105807_cora.log` |

Qk 略高于 E。默认学习率即使只留最强 1% 也只有 53%，说明问题不只是边数，核张量本身在 `lr_rec=0.001` 时区分度不够。

### 10-run：`lr_rec=0.1 --edge_topk 12`，seed 0–9

全部跑通，不再 0 边崩溃。test acc：32.0, 28.0, 50.7, 63.4, 74.1, 64.8, 41.7, 42.4, 41.7, 31.9。

**平均 47.1 ± 15.7**（样本标准差），论文 Table 2 是 **81.4 ± 1.6**。单次最好仍是 seed 42 的 75.0%，seed 4 也有 74.1%。

方差主要来自两处，不是阈值本身：

1. **压缩塌缩：** seed 0/6/9 的 adj 全零，topk 只能在零矩阵上随便留 12 条边，acc 约 32–42%。
2. **训练超点太少：** seed 1/8 的 train batch 只有 4 个点（官方按划分比例取整），即使核值正常也只有 28–42%。seed 4 有 10 个训练点，74.1%。

### 结论

分位数/topk **解决了「能不能出边」**，单次最好从 74.5% 到 **75.0%**，但 10 次平均被塌缩种子和划分配额拖到 ~47%，对不上 81.4%。下一步更像是压住 `lr_rec=0.1` 的塌缩（或换不塌缩的学习率再配 topk），以及训练超点配额，而不是继续调阈值。

---

## 2026-09-10 塌缩重试 + 训练超点配额

针对上一轮 10-run 的两个来源：核全零、train 只有 4 个点。

### 代码

| 改动 | 说明 |
|------|------|
| 去掉 `Embedding(..., padding_idx=0)` | 官方把 Cora 的 0 号节点因子锁成 0 |
| `--rec_retries`（默认 2） | `core_max < min_core` 时 `lr_rec × 0.1` 重新分解 |
| `--rec_proj`（默认 0） | 每步投影到非负；与 `lr_rec=0.1` 合用会**立刻**塌缩，已关掉 |
| `class_split_distribution` | 按 `mask_list` 的 0/1/2 做最大余数法，Cora 配额约 **16/6/13** |
| `--train_all_synth` | 全部合成节点当训练集；含 val/test 原型，**有泄漏，不作正式对照** |

本轮实验开了 `rec_proj=1`（当时的默认），因此 `lr_rec=0.1` 第一次必塌缩，第二次用 0.01 成功（核 max≈0.66）。

### 结果（`--lr_rec 0.1 --edge_topk 12`，自动重试到 0.01）

| seed | train 超点 | test acc | 上一轮 topk 同种子 |
|------|------------|----------|-------------------|
| 0 | 14 | **65.30%** | 32.0%（核全零） |
| 1 | 15 | **69.30%** | 28.0%（train=4） |
| 2 | 16 | **75.20%** | 50.7% |
| 3 | 16 | 67.40% | 63.4% |
| 4 | 14 | 65.10% | 74.1% |
| 5 | 16 | 57.60% | 64.8% |
| 6 | 15 | **69.70%** | 41.7%（核全零） |
| 7 | 16 | 73.60% | 42.4% |
| 8 | 15 | 73.00% | 41.7%（train=4） |
| 9 | 15 | 43.40% | 31.9%（核全零） |
| 42 | 14 | 73.30% | 75.0% |

seed 0–9：**65.96 ± 9.43**（先前 47.1 ± 15.7）。论文 **81.4 ± 1.6**。单次最好 seed 2 的 **75.20%**。

直接 `--lr_rec 0.01 --edge_topk 12` seed 42：70.60%，与重试后同一量级。

`--train_all_synth 1` seed 42：test **88.00%**、val 81%。合成 val/test 超点特征是原图 val/test 同类平均，等于把测试原型拿去训练，**不算有效复现**。

### 结论

塌缩重试 + 配额把 10 次平均从 47% 拉到 **66%**，坏种子不再掉到 30%。与 81.4% 仍差约 15 个点，方差仍大于论文。剩余更可能是官方 wandb 扫到的 `R / add_ratio / lr_gnn` 组合，或 `dtgb` 的 torch 2.2 / pyg 2.8 与官方 2.1.2 / 2.6.1 不一致。

建议命令：

```bash
bash repro/run_gctd.sh cora 0.013 --num_workers 0 --lr_rec 0.1 --edge_topk 12
```

（`lr_rec=0.1` 若塌缩会自动改用 0.01。）

---

## 2026-09-10 小网格扫描 R / add_ratio / lr_gnn

固定：Cora 0.013，seed 42，`--lr_rec 0.01 --edge_topk 12`，`drop_ratio=0.1`。  
网格：`R ∈ {3,5}`，`add_ratio ∈ {0.05,0.1,0.2}`，`lr_gnn ∈ {0.01,0.001}`，共 12 组。  
选优指标与官方 wandb 一致：验证集 `best_val_acc`（按最小 val loss 存的 checkpoint）。  
表：`results/gctd/runs/sweep_R_add_lrgnn.csv`

| R | add_ratio | lr_gnn | val | test |
|---|-----------|--------|-----|------|
| 3 | 0.05 | 0.01 | 70.4 | 71.6 |
| 3 | 0.05 | 0.001 | 75.8 | 73.9 |
| 3 | 0.10 | 0.01 | 66.2 | 66.4 |
| 3 | 0.10 | 0.001 | 73.4 | 71.8 |
| 3 | 0.20 | 0.01 | 50.6 | 51.5 |
| 3 | 0.20 | 0.001 | 73.8 | 71.7 |
| 5 | 0.05 | 0.01 | 73.2 | 71.1 |
| 5 | 0.05 | 0.001 | 67.6 | 67.3 |
| 5 | 0.10 | 0.01 | 70.0 | 66.4 |
| 5 | 0.10 | 0.001 | 70.8 | 69.2 |
| **5** | **0.20** | **0.01** | **76.4** | **76.3** |
| 5 | 0.20 | 0.001 | 71.2 | 68.9 |

seed 42 上最好是 `R=5, add_ratio=0.2, lr_gnn=0.01`，test **76.3%**（此前单次最好 75.2%）。默认 `R=5, add=0.1, lr_gnn=0.001` 只有 69.2%。

同一组再跑 seed 0–9：26.5, 68.9, 54.5, 73.2, 71.8, 18.6, 38.7, 33.9, 70.7, 69.7。  
**平均 52.7 ± 21.3**，比上一轮配额修正后的 66.0 ± 9.4 **更差**。`lr_gnn=0.01` 在部分种子上把 GCN 训崩（18–27%）。

### 结论

单种子网格能把 seed 42 从 ~70% 抬到 76%，但对不上论文的 81.4%，也泛化不到 10-run。作者用的是贝叶斯搜索且看 val，我们只扫了 12 组、只看一个种子，搜到的是「这个种子上的峰」而不是稳定设定。默认复现命令不改成这组。

---

## 2026-09-10 独立环境 gctd（Python 3.11 + torch 2.1.2）

新建 conda 环境 `gctd`，不改 `dtgb`。脚本：`scripts/setup_gctd_conda.sh`。`repro/run_gctd.sh` 改为优先激活 `gctd`。

| 项 | 官方 README | `gctd` 环境 |
|----|-------------|-------------|
| Python | 3.11.5 | 3.11.15 |
| torch | 2.1.2 | 2.1.2+cu121 |
| pyg | 2.6.1 | 2.6.1 |
| sklearn / scipy / faiss / tensorly | 1.6.1 / 1.13.1 / 1.9.0 / 0.9.0 | 已对齐 |
| GPU | — | RTX 3090，CUDA 可用 |

烟雾测试通过（2+2 epoch）。随后同一套复现补丁（配额、topk、`--rec_proj 0`）。

### seed 42

| 设定 | 环境 | core_max | train | test |
|------|------|----------|-------|------|
| `--lr_rec 0.1 --edge_topk 12` | gctd | 0.089（未塌缩） | 16 | **44.90%** |
| `--lr_rec 0.01 --edge_topk 12` | gctd | 0.662 | 16 | **69.20%** |
| 同左（重试后的 0.01） | dtgb | ~0.66 | 14 | 73.30% |

官方版本下 `lr_rec=0.1` 反而更差：核没塌成全零，但合成图偏软（mean 0.019），GCN 只有 45%。`lr_rec=0.01` 与 `dtgb` 上同一设定的 69.2%（扫描表里 R=5, add=0.1）一致。

### 10-run：gctd，`--lr_rec 0.01 --edge_topk 12`，seed 0–9

test：67.3, 61.0, 64.4, 69.7, 69.4, 71.9, 39.2, 36.8, 73.6, 57.1。  
**61.0 ± 13.1**。表：`results/gctd/runs/env_gctd_lr01_seeds.csv`。

对照 `dtgb` 上配额+重试后的 10-run：**66.0 ± 9.4**。论文 **81.4 ± 1.6**。

### 结论

对齐官方 torch/pyg **不能**解释与 Table 2 的差距，钉扎环境甚至略差于 `dtgb`。剩余差异更像是：官方 wandb 搜到但未写入 README 的完整超参、或我们改过的阈值/配额与他们实际表格设定仍不一致。不要指望换环境就能到 81%。

建议命令改为直接 `--lr_rec 0.01`：

```bash
bash repro/run_gctd.sh cora 0.013 --num_workers 0 --lr_rec 0.01 --edge_topk 12
```

---

## 2026-09-10 GCond 协议（全合成点训练 + 只用原图 train 特征）

开关 `--gcond_protocol 1`：K-Means 簇内原图 **train** 节点取特征/多数类；无 train 的簇回退到该类全体 train 原型；合成点全部 `train_mask`。`--weighted 0`。环境 `gctd`，`--lr_rec 0.01 --rec_proj 1`。

### 论文边：ReLU 核平均再对称化（无 0.05）

seed 42：`edge_mode=relu_sym`，adj min=0.0045，**1225 边、密度 1.0**（ReLU 没有造出零）。35 个点特征全独特（34 簇含 train）。train acc 卡在 22.9%，**test 23.30%**。完全图 + 无权 GCN 再次过平滑。论文「ReLU 带来稀疏」在当前学习率下不成立。

### 同一训练协议 + `--edge_topk 12`

seed 42：test **53.10%**（val 50.0%），batch 35。  
seed 0–9：70.3, 46.0, 51.0, 59.2, 65.9, 60.8, 69.2, 60.6, 56.6, 41.1。  
**58.1 ± 9.6**。表：`results/gctd/runs/gcond_protocol_topk12_seeds.csv`。

对照同环境、官方 class+split 特征、约 16 个训练超点的 10-run：**61.0 ± 13.1**。论文 **81.4 ± 1.6**。

### 结论

这条「更像 GCond / 更像论文文字」的协议**没有**把数字拉到 81%。全 35 点监督反而略差于官方「类原型 + 少训练点」。主要瓶颈仍是：核在 ReLU 后并不稀疏，以及簇内 train 平均迁回原图不如全图 class 原型。默认复现命令仍用 `--lr_rec 0.01 --edge_topk 12`，不要默认打开 `gcond_protocol`。

---

## 待办

- [x] 按论文超参跑完整 Cora 0.013，对照表格精度（默认 30.2%；`lr_rec=0.1` 后单次 74.5%）
- [x] 检查合成图标签/划分与 K-Means 分配，确认 train acc 卡死原因
- [x] 提高边阈值或扫 `lr_rec`，使 `A^S` 非完全图后再训 GCN
- [x] 修 `compute_supernode_info`：特征改为 K-Means 簇内平均（已试；Cora 上变差，默认关闭）
- [x] 相对/分位数阈值，避免绝对 0.05 对种子过敏，才能做 10-run（已做；10-run 47.1±15.7）
- [x] 压住 `lr_rec=0.1` 塌缩 + 训练超点配额（10-run 66.0±9.4）
- [x] 小网格扫描 R / add_ratio / lr_gnn（seed 42 最好 76.3%；10-run 52.7±21.3，不稳）
- [x] 独立环境 `gctd`（Python 3.11 + torch 2.1.2）：10-run 61.0±13.1，未到 81.4%
- [x] GCond 协议（全合成点 + 原图 train 特征）：relu_sym 23%；+topk 10-run 58.1±9.6
- [x] Cora 实验总表 `results/gctd/cora_summary.csv`；issue 草稿 `repro/gctd_issue_draft.md`（未发出）
- [x] Citeseer / Pubmed 原始文件已下
- [x] Citeseer 0.9% 与 Pubmed 0.08% 各 10 seed（2026-09-13，见文末三节）：64.92±7.72 与 77.90±1.45
- [x] Citeseer `lr_rec=0.001` 对照 10 seed：66.45±5.09（否证"塌缩降 lr"假设）
- [x] Table 2 三格汇总 `results/gctd/table2_summary.csv`
- [ ] GCond 外部对照（R-GCTD-3）
- [ ] wandb 0.19.6 降级 protobuf 与 tensorboard 的冲突尚未修复（仅影响 `dtgb`）
- [ ] 向作者发 issue；冻结条目（R-GCTD-5）待 R-GCTD-3 完成或作者回复

---

## 2026-09-12 Cora 实验总表（不训练）

把此前散落在本日志各节的 Cora 1.3% 结果收成 `results/gctd/cora_summary.csv`。列：id / kind（single、10-run、fail、reference）/ setting / env / seeds / n / mean_test / std_test / best_test / notes / source。数字与上文各节一致，未重跑。

读表时先看 10-run 与 paper 行：

| id | 设定 | 环境 | n | 均值 ± σ | 单次最好 |
|----|------|------|---|---------|----------|
| A | 官方默认 `lr_rec=0.001` thresh 0.05 | dtgb | 1 | 30.2 | — |
| Qk10 | `lr_rec=0.1` topk 12 | dtgb | 10 | 47.1 ± 15.7 | 74.1 |
| Qretry | 上者 + 塌缩重试 + 训练超点配额 | dtgb | 10 | **66.0 ± 9.4** | 75.2 |
| grid10 | seed 42 网格峰 `R=5 add=0.2 lr_gnn=0.01` | dtgb | 10 | 52.7 ± 21.3 | 73.2 |
| env01_10 | `lr_rec=0.01` topk 12 | gctd 钉扎 | 10 | 61.0 ± 13.1 | 73.6 |
| gcond_topk10 | GCond 协议 + topk 12 | gctd | 10 | 58.1 ± 9.6 | 70.3 |
| grid42 | 同上网格、仅 seed 42 | dtgb | 1 | 76.3 | 76.3 |
| paper | Table 2 | — | 10 | 81.4 ± 1.6 | — |

`leak`（`train_all_synth` 88%）含 val/test 原型，不算有效复现。默认命令仍是 `--lr_rec 0.01 --edge_topk 12`，不要用网格峰。向作者的求证草稿：`repro/gctd_issue_draft.md`，**尚未发出**。Cora 上不再扫参。

---

## 2026-09-12 Citeseer / Pubmed 原始文件（未训练）

Actor 10 划分占用 GPU 时只拉数据。`bash repro/download_planetoid.sh citeseer` / `pubmed`（`ghfast.top`）。落点 `repro/gctd/data/<name>/raw/`。

Citeseer SHA-256：

- `ind.citeseer.allx` `2ac30345d95c9ec933a817ee0bdd6a5f077f8c184a20e696910192d534414668`
- `ind.citeseer.ally` `f704b2d986dde6c2669934de1f3ae5696a6cf9455c0f6b2646a2d135ea0a1c95`
- `ind.citeseer.graph` `d79a4ef9d3e7169aee8946145f6b7306e35bc79bffad26346cfb94e10e9912a7`
- `ind.citeseer.test.index` `2af990671580b6b2df5d158d1038f8292e30c9cd821b5453f399659b25b723d4`
- `ind.citeseer.tx` `539a8906a2da97628d212f2fdd668c109a8b3f0d36574b59e5d3fd5b5303da21`
- `ind.citeseer.ty` `55e5bd1ba1e733a04598753ad1a8d57957f4b8f89e74519f41f4f4938767e4ce`
- `ind.citeseer.x` `d20de19150741e555de0ed037195630fc194114ebc7fd72ced62810148aa22f6`
- `ind.citeseer.y` `8ba87e515d8e3ee3cf52f6d2c5b86aa73f11ecad825a808455209ec26cd54924`

Pubmed SHA-256：

- `ind.pubmed.allx` `508e538e2abdccdd54c4d3e9f49d638b4af7107d85845f66ddea5a5152658b7e`
- `ind.pubmed.ally` `0c37bbe3b5014ec365e9d393cf4791925e5ed94fb194305d74f064a8d7b50f0e`
- `ind.pubmed.graph` `5b89f0036ca22909471f1e6558eb42fa06e0c730a577bde5b058b40638f81dc9`
- `ind.pubmed.test.index` `b101d421688bbaecbd82e8a18f1e282378d6830f3a37666f28ebc47f844341b5`
- `ind.pubmed.tx` `4eb5f5d0f30f26497eb0ac6ac9719d09c67e284f1ed0385c93f3ef27a671da3d`
- `ind.pubmed.ty` `ee2e0d4819d9fbcc403689c3bf2e49face401b605932f093bc58ab6461130fdd`
- `ind.pubmed.x` `fbe9cb5c47200d1b7769a26e579be3b7130b556831f9d850e77c4c74f2599b33`
- `ind.pubmed.y` `e6c807633307a07ed659249006536a147c7999c797f11a2560752990181b41b3`

未跑 `run_gctd.sh citeseer/pubmed`（GPU 给 SGPC Actor）。

---

## 2026-09-13 固化复现改动为 `gctd-repro.patch`（不训练）

此前对官方代码的改动只散落在日志表格里，补上可 `git apply` 的完整补丁（CLOSEOUT_PLAN R-WS-1）。

- 官方提交：`785cfc9`（`grafted`，仅含一个提交）。
- 补丁：`repro/gctd-repro.patch`，834 行，6 个文件。
- SHA-256：`2e6cc76d9cf1208565b2949e7a22d1106b63c8ddb9966566c7cdc9736dec4500`。

涉及文件与内容：

| 文件 | 改动 |
|------|------|
| `src/utils/args.py` | 新增 CLI 开关：`--no_wandb`、`--data_dir` / `--save_dir` / `--log_file`、`--num_workers`、`--edge_topk` / `--edge_quantile` / `--edge_rel`、`--seed`、`--feat_from_cluster`、`--gcond_protocol`、`--train_all_synth`、`--rec_retries`、`--min_core`、`--rec_proj`；默认值与官方一致（`--lr_rec` 默认仍 0.001、`--seed` 默认仍 42） |
| `src/train.py` | stdout 落盘（`--log_file`，Tee）；wandb 改为可选（`--no_wandb` / `WANDB_MODE`），官方是无条件 `wandb.login()`；核塌缩时按 `--rec_retries` 把 `lr_rec × 0.1` 重分解；按重建误差选最佳 checkpoint |
| `src/models/gctd.py` | `to_edge_index` 支持 `--edge_topk` / `--edge_quantile` / `--edge_rel`，替代写死的 0.05 阈值；`--gcond_protocol` 的 ReLU+对称化路径；按原图类别/划分分布分配超点配额；`--feat_from_cluster` 簇内平均（默认关） |
| `src/utils/data_handling.py` | 特征归一化 / 邻接构建的小修 |
| `src/utils/utils.py` | 日志与随机种子相关小修 |
| `src/utils/paths.py` | **新增**：把相对路径解析到仓库根，去掉对 cwd 的隐式依赖 |

注：**没有** `--train_supernode_quota` / `--collapse_retry` 这两个开关；超点配额是 `gctd.py` 内置行为，塌缩重试的开关名是 `--rec_retries`（配合 `--min_core`）。

验证：在官方 `HEAD` 的干净 worktree 上 `git apply --check repro/gctd-repro.patch` 通过（临时 worktree 已清理）。

未包含：`data/`（数据，已在根 `.gitignore` 排除）。默认开关全部关闭时行为与官方原样一致（1 epoch 回归见表内 A 行）。

---

## 2026-09-13 Citeseer 0.9%（R-GCTD-1 第一格）

命令（当前建议设定，与 Cora 收口一致）：

```bash
bash repro/run_gctd.sh citeseer 0.009 --num_workers 0 --lr_rec 0.01 --edge_topk 12 --seed <S>
```

环境 `gctd`。烟雾 `20260913_174140_citeseer.log`（2+2 epoch，36.0%）通过后跑正式。
批量日志 `results/gctd/runs/20260913_citeseer_009_seeds0to9.batch.log`。
逐运行 CSV：`results/gctd/citeseer_0p009_runs.csv`（解析脚本 `scripts/parse_gctd_log.py`）。

| seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 42（单次） |
|------|---|---|---|---|---|---|---|---|---|---|-----------|
| test | 65.0 | 62.6 | 72.9 | 60.3 | 59.5 | 72.5 | 74.7 | 49.8 | 61.9 | 70.0 | 59.8 |

- 10 seed：**64.92 ± 7.72**（最好 74.70，seed 6）。
- 论文 Table 2（Citeseer 0.9%）：**76.8 ± 0.4**。差值 **−11.88**。
- 方差 7.72 是论文 0.4 的 **约 19 倍**。
- 全部 10 次 `lr_rec=0.01` **未塌缩**（`rec_attempts=1`，`core_max≈0.7`），
  核阈值 `thresh≈0.437`、合成图 29 点 / 21–24 边 / 密度 0.025–0.029。

对 Cora 的判定：**差距不是 Cora 特有**——Citeseer 同样低约 12 个点、方差同样大一个数量级。

## 2026-09-13 Citeseer `lr_rec=0.001` 对照（否证"塌缩降 lr"假设）

背景：Pubmed 能到 79 附近，是因为 `lr_rec=0.01` 令核塌缩，代码按 `--rec_retries`
把 lr 降到 `0.001` 后重分解成功。由此提出假设：Citeseer 低 12 点是否也因为没走
"降到 0.001"这条路径？做 10 seed 对照。

```bash
bash repro/run_gctd.sh citeseer 0.009 --num_workers 0 --lr_rec 0.001 --edge_topk 12 --seed <S>
```

批量日志 `results/gctd/runs/20260913_181552_citeseer_009_lrrec1e3_seeds0to9.batch.log`；
逐运行 CSV `results/gctd/citeseer_0p009_lrrec1e3_runs.csv`。

| seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|------|---|---|---|---|---|---|---|---|---|---|
| test | 60.0 | 66.2 | 64.3 | 61.7 | 69.0 | 73.1 | 71.8 | 72.7 | 66.0 | 59.7 |

- 10 seed：**66.45 ± 5.09**（最好 73.10，seed 5）。
- 对照 `lr_rec=0.01` 的 64.92 ± 7.72：均值只 **+1.53**，σ 从 7.72 降到 5.09。
- 论文 76.8 ± 0.4 的差仍是 **−10.35**；σ 仍是论文的 **约 13 倍**。
- 关键：`lr_rec=0.001` 下核 **同样没有塌缩**（`rec_attempts=1`，`lr_rec_used=1.0e-03`），
  阈值升到 `thresh≈0.578–0.597`，仍 22–24 边。

结论：**假设否证**。Pubmed 的成功不能归因于 lr 落到 0.001；在 Citeseer 上主动降到
0.001 既不能带来 10 点提升，也不能把方差压到论文量级。

## 2026-09-13 Pubmed 0.08%（R-GCTD-1 第二格）

```bash
bash repro/run_gctd.sh pubmed 0.0008 --num_workers 0 --lr_rec 0.01 --edge_topk 12 --seed <S>
```

烟雾 `20260913_174155_pubmed.log`（2+2）与 `20260913_174311_pubmed.log`（20+2）通过后跑正式。
批量日志 `20260913_pubmed_0008_seed42.batch.log`、`20260913_181359_pubmed_0008_seeds0to4.batch.log`、
`20260913_182606_pubmed_0008_seeds5to9.batch.log`；
逐运行 CSV `results/gctd/pubmed_0p0008_runs.csv`。

| seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 42（单次） |
|------|---|---|---|---|---|---|---|---|---|---|-----------|
| test | 79.0 | 75.2 | 79.4 | 76.7 | 79.8 | 76.8 | 78.8 | 77.0 | 78.3 | 78.0 | 79.7 |

- 10 seed：**77.90 ± 1.45**（最好 79.80，seed 4）。
- 论文 Table 2（Pubmed 0.08%）：**79.9 ± 0.2**。差值 **−2.00**。
- seed 42 单次的 79.70 只是落在高端；**不能用单次代表该格**。
- 全部 10 次都先塌缩、再按 `--rec_retries` 降到 `lr_rec=0.001`（`rec_attempts=2`），
  之后 15 个合成点、20–24 边、密度 0.089–0.107。

对 R-GCTD-1 的判定：差距 **幅度随数据集下降**（Cora −15.4、Citeseer −11.9、Pubmed −2.0），
但 **三个格没有一个是严格命中**（Pubmed 的 σ 差 7 倍）。Pubmed 最接近，与它的合成图最稀疏、
塌缩后落到稳定分支一致。

## 2026-09-13 Table 2 三格汇总（差距是否 Cora 特有）

新增 `results/gctd/table2_summary.csv`：一行一格，含设定 / 环境 / seed 数 / 均值 / σ /
单次最好 / 论文对照，并列出三个 `paper_*` 参照行。数字由 `scripts/parse_gctd_log.py`
从原始日志重算，与逐运行 CSV 交叉校验一致。

| 数据集（比例） | 我们（10 seed） | 论文 | 差 | σ 比 |
|----------------|-----------------|------|-----|------|
| Cora 1.3% | 65.96 ± 9.43 | 81.4 ± 1.6 | −15.4 | 5.9× |
| Citeseer 0.9% | 64.92 ± 7.72 | 76.8 ± 0.4 | −11.9 | 19.3× |
| Citeseer 0.9%（lr_rec=0.001 对照） | 66.45 ± 5.09 | 76.8 ± 0.4 | −10.4 | 12.7× |
| Pubmed 0.08% | 77.90 ± 1.45 | 79.9 ± 0.2 | −2.0 | 7.3× |

**判定**：不是 Cora 特有。三个数据集全部低于论文，且除 Pubmed 外 σ 都大一个数量级。
问题指向**统一的配方/协议层面**（官方 wandb 搜索到的完整超参、或官方表格所用的
稀疏化/配额策略与我们实现的差异），而不是某个数据集的数据特性。

同步更新的文件：`results/gctd/{citeseer_0p009_runs,citeseer_0p009_lrrec1e3_runs,
pubmed_0p0008_runs,table2_summary}.csv`、`scripts/parse_gctd_log.py`（新增）、
`GCTD_README.md`、`results/SUMMARY.md`、`CLOSEOUT_PLAN.md`（R-GCTD-1 状态）。

R-GCTD-3（GCond 外部对照）与 R-GCTD-5（冻结条目）仍未做，冻结条件尚未满足。
