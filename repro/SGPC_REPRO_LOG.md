# SGPC 复现日志

> 当前：**已冻结**（2026-09-13，见文末「冻结（步骤 7 收口）」）。9/9 数据集官方原样，
> oracle 与论文中心值差 0.4–1.2 点（6 个数据集），val 选模系统性偏低，Wisconsin 偏高。
> **不要**把单次数字写成 Table 1 统计复现，也不要把 oracle 当 Table 1 复现数字。
> 入口：[SGPC_README.md](SGPC_README.md)。

论文：*Sheaf Graph Neural Networks via PAC-Bayes Spectral Optimization*，AAAI 2026。论文库编号 29。  
官方代码：https://github.com/ChoiYoonHyuk/SGPC  
本地论文：`papers/gnn-frontier-2025-2026/07-ccf-aaai-ijcai-sigir/29_SGPC_AAAI2026_official.pdf`；
附录：`repro/sgpc/Supplemental.pdf`  
读书笔记：`paper/notes/29_sgpc.md`  
学习模块：`LEARNING_PLAN.md` M1（sheaf 拉普拉斯、PAC-Bayes、谱间隙、最优传输）

约定：

- 日志按时间追加，不改写既有结论。
- 官方仓库放 `repro/sgpc/`；运行产物放 `results/sgpc/runs/`。
- 先保留官方算法与评测实现，只在外层处理数据路径、环境、GPU 和日志。
- 每次运行记录官方提交哈希、`main.py` 哈希、环境版本、完整命令和独立文本日志。

复现目标（论文 Table 1，SGPC 行，单位 %）：

| Cora | Citeseer | Pubmed | Actor | Chameleon | Squirrel | Cornell | Texas | Wisconsin |
|------|----------|--------|-------|-----------|----------|---------|-------|-----------|
| 83.0 ± 0.55 | 72.6 ± 0.21 | 79.9 ± 0.06 | 38.1 ± 0.52 | 53.3 ± 1.29 | 36.0 ± 0.30 | 81.0 ± 2.33 | 83.2 ± 1.82 | 81.1 ± 2.60 |

论文正文"Implementation"一段写的协议：Adam，lr 1e-3，weight decay 5e-4；
∆t = 0.02（同配）/ 0.5（异配）；"Following Kipf & Welling, 20 labeled nodes per class are
randomly selected for training, with the remaining nodes split into validation and test sets"。
论文未写 seed 数量、划分次数、选模指标。

---

## 2026-09-12 步骤 1：源码固定

- 官方 `main` 提交：`114b585d0d0e32afbf1d7232dd04c013fa8453e2`（2025-11-10，"Update ReadMe.md"）
- 克隆方式：`ghfast.top` 镜像；`git ls-remote` 与 GitHub API 返回的 `main` SHA 均为同一值，一致。
- 仓库共 21 个提交；内容只有 `main.py`（12,313 B）、`ReadMe.md`、`Supplemental.pdf`。
- 文件 SHA-256：
  - `main.py`：`9f852918f355839c1b26a966d88eb5beb9c0d7479cc2f7483f4fc67253a637c3`
  - `Supplemental.pdf`：`235029e1d5606108e0031ef676eb2aeedd42e6b4eda4ad21c09a21223dba02f4`
- 官方没有 `requirements.txt`、没有 seed、没有 CLI 超参；`main.py` 的唯一参数是 0–8 的数据集编号。

## 2026-09-12 步骤 2：环境

- 直接复用 `dtgb`：Python 3.10.20、torch 2.2.1+cu121、PyG 2.8.0.post1、torch_sparse 0.6.18+pt22cu121、RTX 3090。
- 依赖只有 `torch`、`torch_sparse`、`torch_geometric`（`GATConv`、四个数据集类），全部已在 `dtgb` 中。
- 官方未声明任何版本，因此不存在"对齐钉扎版本"的问题；后续若数字不符，环境不是首要怀疑对象。

## 2026-09-12 步骤 3：数据

- 官方 `main.py` 把数据根目录写死为 `/tmp/<Name>`。外层处理：`repro/download_sgpc_data.py`
  把 PyG 的 `download_url` / `fs.cp` 对 GitHub 的请求改写到镜像，其余交给 PyG 自己的
  Dataset 类，数据落到 `repro/sgpc/data/<Name>/`；`repro/run_sgpc.sh` 再用符号链接
  `/tmp/<Name> -> repro/sgpc/data/<Name>`，官方代码原样运行。
- 9 个数据集的规模与 raw 目录 SHA-256（目录内文件名 + 内容的组合哈希）：

| id | 数据集 | 节点 | 边 | 特征 | 类 | mask 维度 | raw_sha256 |
|----|--------|------|----|------|----|-----------|------------|
| 0 | Cora | 2,708 | 10,556 | 1,433 | 7 | 1 | `c5cfb090…20cc5bd` |
| 1 | Citeseer | 3,327 | 9,104 | 3,703 | 6 | 1 | `1c4153a0…3e51ca` |
| 2 | Pubmed | 19,717 | 88,648 | 500 | 3 | 1 | `62337498…1ca1ca40` |
| 3 | Chameleon | 2,277 | 36,101 | 2,325 | 5 | 2（10 组） | `4fa16dd6…6a5d0b` |
| 4 | Squirrel | 5,201 | 217,073 | 2,089 | 5 | 2（10 组） | `d160fab2…6ce4e53` |
| 5 | Actor | 7,600 | 30,019 | 932 | 5 | 2（10 组） | `21996e6d…bd18ed51` |
| 6 | Cornell | 183 | 298 | 1,703 | 5 | 2（10 组） | `c775439a…9120d4d0` |
| 7 | Texas | 183 | 325 | 1,703 | 5 | 2（10 组） | `2ed3ad36…59bb519683` |
| 8 | Wisconsin | 251 | 515 | 1,703 | 5 | 2（10 组） | `bf60ed59…5cd362ce34` |

  完整哈希见 `python repro/download_sgpc_data.py` 的输出。节点 / 边 / 类数与附录 Table 2 一致
  （附录边数是有向计数或含自环，Cora 10,558 vs PyG 10,556 等属于常见差异，不影响结论）。

## 2026-09-12 步骤 4：代码审计（只记录不改）

读完 `main.py` 全部 390 行，以下几点与论文文字或常规协议不一致，先记录：

1. **划分与论文文字不一致。** 论文写"每类随机选 20 个标注节点训练，其余划为 val / test"。
   代码直接用 PyG 数据集自带的 mask：Cora / Citeseer / Pubmed 是 Planetoid public split
   （每类 20 训练、500 val、1000 test，不随机）；其余 6 个数据集 `train_mask.dim()==2`
   时只取 **第 0 组** geom-gcn 60/20/20 划分（不是每类 20 个）。
2. **没有任何随机种子设置**，也没有多次运行的循环。论文 Table 1 的 ± 不知来自多少次、
   多少划分。
3. **`Best Test` 用 test 选模。** 训练循环里 `best_test = max(best_test, test_acc)` 是训练全程
   test 精度的最大值（oracle）；`best_val` 只用于早停计数，**没有**保存"最佳 val 对应的 test"。
   打印行同时给出当前 `Test` 和 `Best Test`。若论文报告的是 `Best Test`，则是 test 泄漏的
   乐观估计；常规协议应取最高 val 时刻的 test。
4. **早停 patience = 1000，最多 2000 epoch**；`ReduceLROnPlateau(patience=50)` 以 val 为指标。
5. **PAC-Bayes 与谱项在 epoch > 300 才加入**（`pacbayes_epoch = 300`），而早停可能在此之前触发
   （Cornell 烟雾测试在 1032 停，已越过 300；但大数据集 val 早饱和时可能不同）。
6. **`spectral_gap_from_sparse` 把 sheaf 拉普拉斯转成 N×N 稠密矩阵做 `eigvalsh`。**
   Pubmed N = 19,717 → 稠密矩阵约 1.5 GB（float32），每个 epoch 一次完整特征分解，
   epoch > 300 后会极慢，且显存压力大。运行 Pubmed 前要预估。
7. **超参与论文文字不完全一致**：论文写异配 ∆t = 0.5，代码 `delta_t = 0.15`；
   论文写"inner gradient steps K = 5"，代码中没有对应的内层循环；
   `set_2 = {3,4,5,6,7,8,9}` 多包含一个不存在的 id 9。
8. **数据集专用硬编码**：`data_id == 3`（Chameleon）时 `alpha_svr / alpha_afm` 初始化为 −8
   而非 −4；`data_id in [0, 1]`（Cora / Citeseer）时输入特征整体减 0.1。属于论文未写的技巧。
9. `sinkhorn_simple(n_iters=1)` 实际只做一次 `exp(-C/ε)` 再 clamp，没有迭代归一化；
   `jko_refine` 也是一步闭式。"Wasserstein–Entropic Sheaf Lifting"在实现上退化为逐边权重。
10. 输出只打印到 stdout，格式 `Epoch %04d | Loss | Val | Test | Best Test`，
    只在 `epoch % 50 == 0` 或 `val_acc == best_val` 时打印；解析用 `scripts/parse_sgpc_log.py`，
    它给出 `val_selected_test`（首次到达最高 val 的 test，常规协议）、`oracle_best_test`（官方 Best Test）。

前两条决定了"论文的 ± 我们无法按同一协议复现"；第 3 条决定了对表时必须同时给两个数字。
第一次运行只做外层移植，不改上述任何一条。

## 2026-09-12 步骤 5：烟雾测试（Cornell，官方原样）

- 日志：`results/sgpc/runs/20260912_142450_smoke_official_Cornell_pid869179.log`
- 命令：`bash repro/run_sgpc.sh smoke_official 6`（等价 `python main.py 6`），`dtgb`，`cuda:0`
- 退出码 0；耗时 70 s；在 epoch 1032 早停（patience 1000）。
- 逐行解析：最高 val 0.8644 首次出现于 epoch 31，此时 test **78.38**；官方 `Best Test` **81.08**
  （出现于 epoch 13，当时 val 仅 0.8136）；论文 Cornell **81.0 ± 2.33**。
- 官方 `Best Test` 与论文中心值几乎重合，`val_selected_test` 低 2.6 个点、仍在论文 ±1.1σ 内。
  这是单次、单划分（geom-gcn split 0），只能说明链路闭环，不能作为结论。

## 2026-09-12 步骤 6 前半：WebKB 三个小图官方原样（未限额，随后中断）

本轮在限额脚本落地前已跑完 Cornell / Texas / Wisconsin；Cora 在第一个 epoch 前被中断。
解析脚本：`scripts/parse_sgpc_log.py`。对照论文 Table 1 的 SGPC 行。

| 数据集 | 日志 | val 选模 test | oracle Best Test | 论文 | 早停 epoch | 秒 |
|--------|------|----------------|------------------|------|------------|----|
| Cornell | `20260912_145107_official_Cornell_pid8636.log` | **81.08**（epoch 57） | 81.08 | 81.0 ± 2.33 | 1058 | 72 |
| Texas | `20260912_145222_official_Texas_pid9144.log` | **81.08**（epoch 510） | 83.78 | 83.2 ± 1.82 | 1511 | 102 |
| Wisconsin | `20260912_145407_official_Wisconsin_pid9725.log` | **84.31**（epoch 162） | 84.31 | 81.1 ± 2.60 | 1163 | 82 |

说明：均为 geom-gcn 划分 0、无 seed 的单次运行。Cornell 的 val 选模与 oracle 碰巧相同且贴论文中心值。
Texas 的 oracle 83.78 贴论文 83.2，但 val 选模 81.08 低约 2 个点。Wisconsin 的 84.31 高于论文中心值约 1.2σ。
Cora 及其余数据集改在 85% 资源上限下重跑（IGNN roman-empire 完成后接着做）。

## 2026-09-12 步骤 6：官方原样九数据集（Pubmed 除外）

限额：`scripts/run_capped.sh`（CPUQuota=1700%、MemoryMax≈51 GiB、CUDA 显存 0.85、MPS 线程 85%）+ `gpu_util_governor.sh` 占空比。
无 root，不能设 `nvidia-smi -pl 297`。SGPC 段采样 GPU util 均值 82.6%，瞬时最高 100%（占空比 RUN 窗口）；CPU ≈5%、内存 ≈4.5/60 GiB、显存最高 2107 MiB。

对照论文 Table 1 SGPC 行。均为发布代码默认：无 seed、异配集只用 geom-gcn 划分 0。`val_selected` = 首次最高 val 的 test；`oracle` = 官方打印的 Best Test。

| 数据集 | 日志 | val 选模 | oracle Best Test | 论文 | 早停 | 秒 |
|--------|------|----------|------------------|------|------|----|
| Cora | `..._cap85_Cora_pid23270.log` | 81.7 | **83.5** | 83.0 ± 0.55 | 1082 | 146 |
| Citeseer | `..._cap85_Citeseer_pid24464.log` | **73.3** | 73.3 | 72.6 ± 0.21 | 1113 | 210 |
| Actor | `..._cap85_Actor_pid26089.log` | **38.29** | 38.88 | 38.1 ± 0.52 | 1029 | 1223 |
| Chameleon | `..._cap85_Chameleon_pid34550.log` | 50.88 | 51.54 | 53.3 ± 1.29 | 1019 | 113 |
| Squirrel | `..._cap85_Squirrel_pid35468.log` | **36.12** | 36.22 | 36.0 ± 0.30 | 1020 | 563 |
| Cornell | `..._official_Cornell_pid8636.log` | **81.08** | 81.08 | 81.0 ± 2.33 | 1058 | 72 |
| Texas | `..._official_Texas_pid9144.log` | 81.08 | **83.78** | 83.2 ± 1.82 | 1511 | 102 |
| Wisconsin | `..._official_Wisconsin_pid9725.log` | **84.31** | 84.31 | 81.1 ± 2.60 | 1163 | 82 |

汇总：`results/sgpc/official_summary.csv`。

分层（单次、划分 0，不能当 L3）：

- L1：除 Pubmed 外 8 个数据集管线闭环。
- L2：oracle 与论文中心值在 Cora / Actor / Squirrel / Cornell / Texas 上接近或落入 ±1σ；Citeseer 略高；Wisconsin 偏高约 1.2σ；Chameleon 低约 1.4σ（50.88/51.54 vs 53.3 ± 1.29）。
- val 选模系统性低于 oracle（Cora −1.8、Texas −2.7），与审计第 3 条一致。
- Pubmed 未跑：`spectral_gap_from_sparse` 对 N=19717 做稠密 `eigvalsh`，epoch>300 后不可接受，留待步骤 7 改 Lanczos 或跳过 PAC 项后再测。

## 2026-09-12 步骤 7：协议开关 + 多划分 / 多种子 + Pubmed

默认关闭：不传额外参数时行为与官方一致（划分 0、无 seed、`spec=dense`、2000 epoch、打印的 `Best Test` 仍是 oracle）。
补丁：`repro/patches/sgpc-protocol.patch`（SHA256 `1095ac78920ad815a7d50e91c59b3499d4d3fa591780737b8d7d8a22e48955ef`），官方 HEAD 仍是 `114b585d0d0e`。
入口：`bash repro/run_sgpc.sh LABEL ID [--seed N] [--split K] [--spec dense|lobpcg|off] [--max_epochs N] [--pacbayes_epoch N]`。
划分脚本：`bash repro/run_sgpc_splits.sh PREFIX ID...`（固定 `--seed 0`）。

新增开关：

| 参数 | 默认 | 作用 |
|------|------|------|
| `--seed` | None | 设 Python / torch / CUDA seed；官方路径不设 |
| `--split` | 0 | 2D geom-gcn mask 的列；1D Planetoid mask 忽略 |
| `--spec` | dense | `dense`=官方 `eigvalsh`；`lobpcg`=稀疏 2 阶；`off`=跳过谱项 |
| `--max_epochs` | 2000 | 官方循环上界 |
| `--pacbayes_epoch` | None | 覆盖 PAC 起始；默认仍 300 |

训练仍按 val 早停。每个 epoch 行的 `Best Test` 仍是 oracle。结束多打一行 `[sgpc] summary`，同时给出 `val_selected_test` 与 `oracle_best_test`。正式表用 val 选模。

### 7a 回归

- Cornell `--max_epochs 1`：退出 0；`n_splits=10`，`spec=dense`。日志 `..._proto_smoke_1ep_Cornell_pid42811.log`。
- Cornell 无额外参数全程：val 78.38 / oracle **81.08**（步骤 6 同划分 oracle 也是 81.08；无 seed 故 val 选模可漂）。日志 `..._proto_default_Cornell_pid43004.log`。

### 7b Pubmed（`--spec lobpcg --seed 0`）

稠密 `eigvalsh` 不再使用。3-epoch 烟雾（`--pacbayes_epoch 1`）退出 0。全程 1062 epoch / 142 s：

| | val 选模 | oracle | 论文 |
|--|----------|--------|------|
| Pubmed public | 78.10（epoch 61） | 78.70 | 79.9 ± 0.06 |

日志：`..._pubmed_lobpcg_Pubmed_pid63156.log`。无 lobpcg 失败打印。单次，不能谈 L3；相对论文中心值约 −1.2（oracle）/ −1.8（val）。

### 7c 异配 geom-gcn 10 划分（`--seed 0`）

六个异配数据集的 10 划分全部完成（Actor / Chameleon / Cornell / Texas / Wisconsin / Squirrel）。

Actor 10 划分于 2026-09-12 23:16 全部退出 0（`actor_splits_0to9.batch.log`），每划分约 20 min，命令 `--split 0-9 --seed 0`（`spec=dense`）。逐次：`results/sgpc/actor_10split_runs.csv`。

| 数据集 | n | val 选模 | oracle | 论文 | val−论文 | oracle−论文 |
|--------|---|----------|--------|------|----------|-------------|
| Actor | 10 | 36.12 ± 1.24 | 37.13 ± 0.90 | 38.1 ± 0.52 | −1.98 | −0.97 |
| Chameleon | 10 | 51.91 ± 2.04 | 52.83 ± 2.02 | 53.3 ± 1.29 | −1.39 | −0.47 |
| Cornell | 10 | 77.57 ± 4.42 | 80.54 ± 3.99 | 81.0 ± 2.33 | −3.43 | −0.46 |
| Texas | 10 | 80.27 ± 6.25 | 85.41 ± 4.63 | 83.2 ± 1.82 | −2.93 | +2.21 |
| Wisconsin | 10 | 83.53 ± 4.91 | 87.45 ± 2.81 | 81.1 ± 2.60 | +2.43 | +6.35 |

Actor 的 val 选模与 oracle 都低于论文中心值（约 1–2 点），但差值与 Cornell 同量级；std 约为论文 ±0.52 的 2 倍，与其余异配集一致。

Squirrel 10 划分（`--seed 0`，每划分退出 0；s0/s1 各有一次未写完的早停日志，表用完整那次）：

| 数据集 | n | val 选模 | oracle | 论文 | val−论文 | oracle−论文 |
|--------|---|----------|--------|------|----------|-------------|
| Squirrel | 10 | 35.93 ± 1.50 | 37.08 ± 1.22 | 36.0 ± 0.30 | −0.07 | +1.08 |

逐次：`results/sgpc/squirrel_10split_runs.csv`。val 选模均值贴近论文中心值，std 约为论文 ±0.30 的 5 倍。oracle 偏高约 1.1 点。仍不能称 L3。

逐次：`results/sgpc/webkb_10split_runs.csv`、`chameleon_10split_runs.csv`、`actor_10split_runs.csv`。汇总：`results/sgpc/hetero_10split_summary.csv`。

读法：

- Cornell / Chameleon 的 **oracle 均值**贴近论文中心值（差 < 0.5 点），但我们的标准差更大。
- **val 选模**在 Cornell / Texas / Chameleon 上系统性低于论文与 oracle，与审计「`Best Test` 用 test 选模」一致。
- Actor 的 val 与 oracle 都低于论文约 1–2 点；oracle−论文（−0.97）与 Cornell（−0.46）/ Chameleon（−0.47）同量级，属同一类偏低现象，不是 Actor 特有。
- Wisconsin 无论 val 还是 oracle 都高于论文；oracle 高约 6 点。可能原因：论文 Table 1 未必是 geom-gcn 10 划分；代码 ∆t=0.15 而论文写 0.5；论文未写选模规则。
- 我们的跨划分方差普遍大于论文 ±，所以还不能称 L3。

### 7d Planetoid 多种子（public split，seed 0–4）

| 数据集 | n | val 选模 | oracle | 论文 | val−论文 | oracle−论文 |
|--------|---|----------|--------|------|----------|-------------|
| Cora | 5 | 82.06 ± 1.23 | 82.58 ± 1.13 | 83.0 ± 0.55 | −0.94 | −0.42 |
| Citeseer | 5 | 71.16 ± 1.26 | 72.02 ± 0.79 | 72.6 ± 0.21 | −1.44 | −0.58 |

Citeseer seed 3 第一次在 ~epoch 1100 于官方 `eigvalsh` 路径报 `LinAlgError`（sheaf 拉普拉斯病态）。dense 路径随后加上与 lobpcg 相同的失败回退（该 epoch 视为 `spec=off`）。重跑 `..._planetoid_s3_retry_Citeseer_pid80284.log` 退出 0，val 72.2 / oracle 72.6，与崩溃前已记下的数字相同。5-seed 表用重跑。

Cora / Citeseer 的 oracle 均值落在论文中心值约 1σ_论文 内，但我们的 std 大约是论文的 2–4 倍（论文可能不是 public split + 5 个 init seed）。

### 7e 分层判定（步骤 7 后）

- L1：9/9 数据集管线闭环（Pubmed 用 `lobpcg`，其余默认 `dense`）。
- L2：Cora / Citeseer / Pubmed / Chameleon / Cornell / Actor 的 oracle 与论文中心值同量级（差约 0.4–1.2 点）。Texas oracle 偏高 2.2；Wisconsin 明显偏高。val 选模除 Wisconsin 外都低于论文。
- L3：否。异配用的是 geom-gcn 10 划分而非论文「每类 20 个随机训练节点」；同配是 public split 的 init seed，不是重新抽样 20/类；论文 ± 更紧。

总表：`results/sgpc/protocol_summary.csv`。解析：`scripts/parse_sgpc_log.py`、`scripts/summarize_sgpc_splits.py`。

## 下一步

- ~~Actor 的 geom-gcn 10 划分（补齐异配主表）~~：**已完成**（2026-09-12 23:16，10/10 退出 0）。
- Pubmed 补 seed 1–4（可选；论文 ±0.06 极紧，预期仍达不到 L3）。
- 异配 ∆t=0.5 对照（论文写 0.5，代码 0.15），尤其 Wisconsin。
- 不把 oracle 写成 Table 1 复现数字；正式引用用 val 选模。
- 穿插 ScaDyG 消融 / GCTD 冻结（GPU 空闲时）。
剩余全量入口（默认 dry-run）：`FULL=1 bash repro/run_sgpc_full.sh`（9/9 数据集与 6 个异配集 10 划分已完成）。

---

## 2026-09-13 冻结（步骤 7 收口）

**范围**：论文 Table 1 的 9 个数据集。同配（Cora / Citeseer / Pubmed）用 public split，
异配（Actor / Chameleon / Squirrel / Cornell / Texas / Wisconsin）用 geom-gcn 10 划分。
正式数字口径为 **val 选模**；`oracle`（官方 `Best Test`，test 取 max）只作对照，不作为
Table 1 复现数字。

### 三级结论

| 级别 | 判定 | 依据 |
|------|------|------|
| L1 管线闭环 | **是** | 9/9 数据集跑通（Pubmed 用 `lobpcg`，其余 `dense`）；Citeseer seed 3 的 `eigvalsh` 病态已加回退并重跑一致；退出码全 0 |
| L2 数值量级 | **部分** | oracle 在 6 个数据集上与论文中心值差 0.4–1.2 点；val 选模系统性偏低 0.07–3.43 点；Wisconsin 偏高（val +2.43 / oracle +6.35） |
| L3 统计一致 | **否** | 协议不同（异配用 geom-gcn 10 划分，论文写"每类 20 个随机训练节点"；同配是 public split 的 init seed，不是重新抽样 20/类）；跨划分 σ 普遍为论文的 2–5 倍 |

### 九数据集总表

`results/sgpc/protocol_summary.csv`（本次已补上此前缺失的 Squirrel 行）。

| 数据集 | n | val 选模 | oracle | 论文 | val−论文 | oracle−论文 |
|--------|---|----------|--------|------|----------|-------------|
| Cora | 5 | 82.06 ± 1.23 | 82.58 ± 1.13 | 83.0 ± 0.55 | −0.94 | −0.42 |
| Citeseer | 5 | 71.16 ± 1.26 | 72.02 ± 0.79 | 72.6 ± 0.21 | −1.44 | −0.58 |
| Pubmed | 1 | 78.10 | 78.70 | 79.9 ± 0.06 | −1.80 | −1.20 |
| Actor | 10 | 36.12 ± 1.24 | 37.13 ± 0.90 | 38.1 ± 0.52 | −1.98 | −0.97 |
| Chameleon | 10 | 51.91 ± 2.04 | 52.83 ± 2.02 | 53.3 ± 1.29 | −1.39 | −0.47 |
| Squirrel | 10 | 35.93 ± 1.50 | 37.08 ± 1.22 | 36.0 ± 0.30 | −0.07 | +1.08 |
| Cornell | 10 | 77.57 ± 4.42 | 80.54 ± 3.99 | 81.0 ± 2.33 | −3.43 | −0.46 |
| Texas | 10 | 80.27 ± 6.25 | 85.41 ± 4.63 | 83.2 ± 1.82 | −2.93 | +2.21 |
| Wisconsin | 10 | 83.53 ± 4.91 | 87.45 ± 2.81 | 81.1 ± 2.60 | +2.43 | +6.35 |

### 关键发现

1. **`Best Test` 是 test 选模**。官方 `main.py` 报告的 `Best Test` 取遍历过程中 test
   准确率的最大值，不是 val 选模。因此 oracle 系统性高于 val 选模（差 0.5–5.1 点），
   不能与论文 Table 1 直接对齐。
2. **∆t 与论文不一致**。论文写 ∆t = 0.02（同配）/ 0.5（异配），代码实际用 0.15。
   Wisconsin 偏高可能与此有关（未验证）。
3. **Squirrel 最接近**（val 差 −0.07），**Wisconsin 最异常**（oracle +6.35）。
4. 官方仓库只有 `main.py`，无 seed / 无 CLI 超参 / 无 `requirements.txt`；`main.py`
   唯一参数是 0–8 的数据集编号。复现按提交 `114b585d0d0e32afbf1d7232dd04c013fa8453e2`
   固定。

### 已知局限（未做，不再补）

- Pubmed 仅 seed 0（论文 ±0.06 极紧，补 seed 1–4 预期仍达不到 L3）。
- 异配 ∆t = 0.5 对照未做（可能解释 Wisconsin）。
- 未按论文文字重建"每类 20 个随机训练节点"的划分。

### 冻结规则

**不再补跑 SGPC 的数据集或 seed**，不重做划分协议。要重启本条线，触发条件是明确要求
重建论文的"每类 20 节点"划分并对照 ∆t。

汇总：`results/sgpc/protocol_summary.csv`、`results/sgpc/hetero_10split_summary.csv`、
`results/sgpc/official_summary.csv`；解析脚本 `scripts/parse_sgpc_log.py`、
`scripts/summarize_sgpc_splits.py`。
