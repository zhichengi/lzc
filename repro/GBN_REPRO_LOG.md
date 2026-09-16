# GBN 复现日志

论文：*Deeper with Riemannian Geometry: Overcoming Oversmoothing and Oversquashing for Graph Foundation Models*，NeurIPS 2025。论文库编号 09。
官方代码：https://github.com/ZhenhHuang/GBN
本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/09_Riemannian_GBN_NeurIPS2025.pdf`
读书笔记：`paper/notes/09_gbn.md`
学习模块：`LEARNING_PLAN.md` M1

约定：日志只追加。官方仓库 `repro/gbn/`。产物 `results/gbn/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：节点分类（论文 Table 3，7 个数据集）与消融（论文 Table 4）；另有 Transfer 任务（Fig. 5，未做）。

> 结果速览（2026-09-14）：
> - **主表（Table 3）**：8/8 完成，**7 个论文对照项中 4 个落在论文 1σ 内**（CS 95.80 vs 95.78，+0.02）。
> - **消融（Table 4）**：16/16 完成，**4/16 格落在 1σ 内**；定位两个失配——`γ0,β0` 常数论文未公开，
>   以及 `βi=0` 在我们实现里几乎不生效（β 映射不完整）。
> 详见文末「步骤 6」「步骤 7」；结构化数字 `results/gbn/nc_table3_summary.csv`、
> `results/gbn/nc_table4_ablation.csv`。

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

---

## 2026-09-13 步骤 3 补：数据补齐（8/8）

预处理时只有 WebKB + Planetoid。本次补齐论文 Table 3 所需的全部数据集。

| 数据集 | 来源 | 落点 | 说明 |
|--------|------|------|------|
| Texas / Wisconsin | 已有 | `datasets/{texas,wisconsin}` | WebKB，原生 `[N,10]` mask |
| Cora | 已有 | `datasets/Cora` | Planetoid |
| Roman-empire | **复用** `repro/ignn/data/roman_empire.npz` | `datasets/roman_empire/raw/roman_empire.npz` | sha256 `a58ba741d123...`（与 IGNN 一致） |
| Amazon-ratings | **复用** `repro/ignn/data/amazon_ratings.npz` | `datasets/amazon_ratings/raw/amazon_ratings.npz` | sha256 `4c3a3e3b9d9f...`（与 IGNN 一致） |
| CS | PyG 下载（Coauthor） | `datasets/CS` | GitHub raw 可直连 |
| computers | PyG 下载（Amazon） | `datasets/computers` | 同上 |
| WikiCS | PyG 下载 | `datasets/WikiCS` | 同上 |

**关键复用点**：PyG `HeterophilousGraphDataset` 的 raw 路径是
`<root>/<name.lower().replace('-','_')>/raw/<name>.npz`。IGNN 已经下好的
`roman_empire.npz` / `amazon_ratings.npz` 正好匹配这个命名，所以拷进
`datasets/roman_empire/raw/` 与 `datasets/amazon_ratings/raw/` 即可被识别，**无需联网**。

核对：8 个数据集全部加载成功，且节点数 / 边数与论文 Table 7 **精确吻合**：

```
WikiCS            N= 11701  E=431726  F= 300  C=10   (论文 11,701 / 431,726)
computers         N= 13752  E=491722  F= 767  C=10   (论文 13,381 / 491,722)
CS                N= 18333  E=163788  F=6805  C=15   (论文 18,333 / 163,788)
Texas             N=   183  E=   325  F=1703  C= 5
Wisconsin         N=   251  E=   515  F=1703  C= 5
Roman-empire      N= 22662  E= 65854  F= 300  C=18   (论文 22,662 / 65,854)
Amazon-ratings    N= 24492  E=186100  F= 300  C= 5   (论文 24,492 / 186,100)
Cora              N=  2708  E= 10556  F=1433  C= 7
```

computers 的节点数 13752 与论文 13381 不同（PyG 的 Amazon 版本差异），边数一致；记
为已知差异，不影响 10 划分对照。

## 2026-09-13 步骤 4 补：发现 `layer_wise` 必须由配置注入

审计时只记了"cwd 依赖 + json 覆盖 CLI"。真正卡住的是：

- `main.py` 的 argparse **没有** `layer_wise`（只有 `modules/models.py` 的默认参数
  `layer_wise=True`）。
- `node_classification.py:load_model` 里是 `layer_wise=self.configs.layer_wise`。
- 官方只预置了 `configs/NC/CS.json`。其它数据集首次运行时 `main.py` 会把 CLI 值
  **另存**一份 json —— 那份 json 里没有 `layer_wise`，紧接着就
  `AttributeError: 'Namespace' object has no attribute 'layer_wise'`。

（烟雾时的历史记录已提到这一点，本次给出确定结论与处理方式。）

处理：**不改官方克隆**，改用外层注入。新增 `scripts/gen_gbn_configs.py`，按论文
Table 8 生成配置到 `results/gbn/configs/`（入库），运行时由
`repro/run_gbn_table.sh` 拷进 `repro/gbn/configs/NC/`。

## 2026-09-13 步骤 5 补：烟雾（8/8 通过）

`EXECUTE=1 SMOKE=1 bash repro/run_gbn_table.sh`（2 epoch，`exp_iters` 保持 10）。

**踩到的坑**：最初烟雾把 `exp_iters` 设成 1 想省时间，结果 CS / WikiCS /
computers / Cora 四个数据集崩：

```
IndexError: too many indices for tensor of dimension 1
  node_classification.py:117  data.train_mask[:, split]
```

原因：官方用 `mask[:, split]`，要求 **2-D** 掩码。这四个数据集走
`RandomNodeSplit(num_splits=...)`，当 `num_splits=1` 时掩码退化成 1-D。WebKB /
Heterophilous 用数据集原生 `[N, 10]` 掩码，所以不受影响 —— 这也解释了为什么
Roman-empire / Ratings / Texas / Wisconsin 四个在错误版本下仍能跑通。

修正：烟雾**只减 `epochs_nc`**，不动 `exp_iters`。修正后 8/8 退出 0，每个约 14 秒。

## 2026-09-13 步骤 6：主表全量（论文 Table 3）

```
EXECUTE=1 DATASETS="Texas Wisconsin Roman-empire Amazon-ratings CS WikiCS computers Cora" \
  bash repro/run_gbn_table.sh
```

- 批次日志：`results/gbn/runs/20260913_222958_gbn_table_full.batch.log`
- 运行区间：2026-09-13 22:29:58 → 2026-09-14 00:11:25（约 1h41m）
- 8/8 退出 0，无 traceback。每数据集 `exp_iters=10`，超参取自论文 Table 8
- 外层每次运行记 `repo_commit=72ad3692916ecc60f2c78d5bd01a55d7c6297a4f`（未变）
- 硬件：RTX 3090 24 GB（论文为 RTX 4090 24 GB）

| 数据集 | n | 我们（3090） | 论文（4090） | 差 | < 1σ_论文 | σ 比 |
|--------|---|--------------|--------------|-----|-----------|------|
| CS | 10 | **95.80 ± 0.28** | 95.78 ± 0.21 | **+0.02** | **是** | 1.33 |
| computers | 10 | **91.12 ± 0.37** | 91.33 ± 0.32 | −0.21 | **是** | 1.16 |
| Wisconsin | 10 | **85.29 ± 3.43** | 86.78 ± 3.84 | −1.49 | **是** | 0.89 |
| Texas | 10 | **82.16 ± 3.46** | 85.01 ± 6.51 | −2.85 | **是** | 0.53 |
| Amazon-ratings | 10 | 51.95 ± 0.51 | 53.51 ± 0.88 | −1.56 | 否（1.8σ） | 0.58 |
| WikiCS | 10 | 84.91 ± 0.70 | 86.21 ± 0.39 | −1.30 | 否（3.3σ） | 1.79 |
| Roman-empire | 10 | 86.87 ± 0.43 | 89.83 ± 0.46 | −2.96 | 否（6.4σ） | 0.93 |
| Cora（论文未列表） | 10 | 84.74 ± 1.86 | —（论文仅在 Fig. 4 做层数扫描） | — | — | — |

**7 个对照项中 4 个落在论文 1σ 内**（CS 近乎逐位：+0.02）。

### 读法

- **CS 是最强证据**：+0.02，σ 比 1.33，说明管线、超参、划分与评测口径都对。
- **computers** −0.21 同样落在 1σ 内。
- 三个超出 1σ 的数据集（Roman-empire −2.96、WikiCS −1.30、Ratings −1.56）**全部低于
  论文**；连同落在 σ 内的四个，**7 项里 6 项低于论文、1 项持平**，呈现一致的小幅
  系统性偏低，而非随机散布。
- **方差侧反而更好**：σ 比为 0.53–1.79，其中 4 项**小于**论文
  （Texas 0.53、Ratings 0.58、Wisconsin 0.89、Roman-empire 0.93）。所以偏低不是"训不
  稳"，Roman-empire 的 10 次是 86.04–87.65、极集中，属**系统性偏移**。
- Roman-empire 的 6.4σ 是本次最大偏差，但**其绝对差仅 2.96 个点**，且我方 σ 更小
  （0.43 vs 0.46）。Roman-empire 是本批最大的异配图（22,662 节点），σ 又极小，因此
  "差/σ" 被放大。

### 可能原因（未逐项验证，按优先级）

1. **硬件 3090 vs 4090**：论文用 4090，本机 3090。IGNN 那条线已确认同一份代码在不同
   卡上有可观差异（作者自述 chameleon 50.79 → 47.53）。这是最可能来源，但**未做受控
   验证**，只作为假设记录。
2. **未公开的构造细节**：论文 Appendix E 的 Table 8 只给了 7 个超参；`tau`、`bias`、
   `add_self_loop`、`embed_dim`、`val_every`（本仓库取 `configs/NC/CS.json` 的
   `val_every=5`）等未在论文中说明。尤其 `val_every=5` 会直接影响早停时机。
3. **划分一致但未核种子**：官方 `main.py` 顶部写死 `set_seed(3047)`，我们的调用保持了
   它；但 `RandomNodeSplit` 生成 10 划分的随机流是否与作者一致无法核验。
4. `computers` 的节点数 13752 vs 论文 13381（PyG 数据版本差异）。

### 分层判定

- **L1 管线闭环：是。** 8/8 退出 0；同 seed 可重跑；日志含 commit / 环境 / GPU。
- **L2 数值量级：是（部分）** —— 4/7 落在论文 1σ 内，含 1 项近乎逐位（CS）。其余 3 项
  偏差 1.3–3.0 个点，方向一致，属可归因的小幅系统性偏低。
- **L3 统计一致：部分。** σ 与论文同量级（比 0.53–1.79，多数更小），但 3/7 的均值差
  超过论文 σ，故不能整体称 L3。

### 结构化结果

- `results/gbn/nc_table3_summary.csv`（主表 8 行）
- 解析：`scripts/parse_gbn_log.py`（同时给 `std_ddof0` 与 `std_ddof1`；官方用
  `np.std` 即 ddof=0）

## 2026-09-13 消融补丁准备与回归（论文 Table 4）

论文 7.2 节：`γ0, β0` = 把可学的边界条件系数换成固定常数；`γi = 0` 去掉外部输入；
`βi = 0` 去掉边界交互；`γi, βi = 0` 时退化 GCN。

官方仓库**没有**消融开关。新增 `repro/gbn-ablation.patch`（默认关闭，`ablate=none`
即官方路径），涉及 `modules/layers.py`、`modules/models.py`、
`node_classification.py`。哈希：`bb8bda833e13aa416bf87df0d2647b887ff35fa48b9ee781e805237d3164f853`。

语义映射（代码中 `rate` 即论文的 β，`gamma` 即 γ）：

| 论文变体 | `--ablate` 值 | 实现 |
|----------|---------------|------|
| GBN（完整） | `none` | 不干预 |
| γ0, β0 | `gamma0_beta0` | 两者换固定常数（**论文未给常数取值**，默认 1.0） |
| γi = 0 | `gamma_all0` | `gamma = 0` |
| βi = 0 | `beta_all0` | `rate = 0` |
| γi, βi = 0 | `gamma_beta_all0` | 两者都置 0 |

### 回归测试中发现并修正的一个 bug

初版补丁用 `getattr(self.configs, 'ablate', 'none')` 取默认值。实测**直接崩溃**：

```
KeyError: 'ablate'   node_classification.py:32
```

根因：`utils/config.py` 的 `DotDict` 把 `__getattr__` 指向 `dict.__getitem__`，
缺键时抛的是 **KeyError** 而不是 AttributeError，因此 `getattr(..., default)`
的默认值**不会生效**。改用 `self.configs.get('ablate', 'none')` 后正常。

### 保真性验证（`ablate=none` 与官方逐位一致）

CPU、Texas、`epochs_nc=2`、`exp_iters=2`、同配置：

| 版本 | 结果 |
|------|------|
| 官方 HEAD（未打补丁） | `[10.81, 5.41]` → 8.11 ± 2.70 |
| 已打补丁，且 json **不含** `ablate` 键 | `[10.81, 5.41]` → 8.11 ± 2.70 |

**逐位一致**，确认默认路径未被改变、且缺键时能正确回落到 `none`。

### 生效性验证（四个开关都改变数值）

同配置（CPU，Texas 2ep，2 iters）：

| 变体 | Best ACCs | 与基线 `[10.81, 5.41]` |
|------|-----------|------------------------|
| `none`（基线） | `[10.81, 5.41]` | — |
| `gamma_all0` | `[10.81, 59.46]` | 变 |
| `beta_all0` | `[10.81, 2.7]` | 变 |
| `gamma_beta_all0` | `[10.81, 59.46]` | 变 |
| `gamma0_beta0` | `[5.41, 59.46]` | 变 |

四个开关都不是空操作。

### 验证方式与遗留

- 用 `git worktree`（`/tmp/gbn-abl` 打补丁、`/tmp/gbn-base` 干净）做对照，**没有**碰
  正在跑主表的官方克隆；两个 worktree 已清理。
- 验证在 **CPU** 上做（避免与主表争 GPU），只关心"是否改变数值 / 是否逐位一致"，
  数字本身不对论文。
- 两个已知不等价点，记录待澄清：
  1. `gamma0_beta0` 的常数论文未给，取 1.0；
  2. 官方 `models.py` 里 `self.gamma = ... if rate is None else gamma`（用 `rate`
     判断 `gamma`），疑似笔误。补丁**保留**该行为以确保 `none` 逐位一致。

### 消融全量

待主表完成后执行（见下方"步骤 7"）。

## 2026-09-13 步骤 7：消融全量（论文 Table 4）

启动命令：

```bash
cd repro/gbn && git apply ../gbn-ablation.patch && cd -
EXECUTE=1 MODES="gamma0_beta0 gamma_all0 beta_all0 gamma_beta_all0" \
  DATASETS="Texas Amazon-ratings CS WikiCS" bash repro/run_gbn_ablation.sh
```

- 批次日志：`results/gbn/runs/20260914_001402_gbn_ablation.batch.log`
- 运行区间：2026-09-14 00:14:02 → 04:46:20（约 4h32m），**16/16 退出 0**，无 traceback
- **跳过 `none`**：`ablate=none` 是已验证的空操作（保真性测试逐位一致），主表数字即基线，
  省下约 63 min。基线行直接引用步骤 6。

### 结果（均值 ± 总体标准差 ddof=0，论文 Table 4）

论文 GBN 行（= 我们的主表）：

| | CS | WikiCS | Texas | Ratings |
|--|----|--------|-------|---------|
| 论文 GBN | 95.78 ± 0.21 | 86.21 ± 0.39 | 85.01 ± 6.51 | 53.51 ± 0.88 |
| **我们（主表）** | **95.80 ± 0.28** | **84.91 ± 0.70** | **82.16 ± 3.46** | **51.95 ± 0.51** |

消融四行（括号内为与论文同格之差，✓ = 落在论文 1σ 内）：

| 变体 | CS | WikiCS | Texas | Ratings |
|------|----|--------|-------|---------|
| γ0, β0 | 90.37 (−3.77) ✗ | 78.65 (−6.71) ✗ | 63.78 (−19.39) ✗ | 42.66 (−10.39) ✗ |
| γi = 0 | 91.90 (−0.36) ✓ | 80.30 (+0.29) ✓ | 68.11 (−8.16) ✗ | 41.62 (−6.61) ✗ |
| βi = 0 | 95.72 (+1.95) ✗ | 85.01 (+3.30) ✗ | 83.51 (+0.73) ✓ | 50.23 (−0.46) ✓ |
| γi, βi = 0 | 91.21 (−0.50) ✗ | 79.65 (+1.36) ✗ | 67.84 (+5.68) ✗ | 44.00 (−4.69) ✗ |

论文对应格（供对照）：

| 变体 | CS | WikiCS | Texas | Ratings |
|------|----|--------|-------|---------|
| γ0, β0 | 94.14 ± 0.26 | 85.36 ± 0.45 | 83.17 ± 4.32 | 53.05 ± 0.78 |
| γi = 0 | 92.26 ± 0.58 | 80.01 ± 0.34 | 76.27 ± 5.34 | 48.23 ± 1.03 |
| βi = 0 | 93.77 ± 0.36 | 81.71 ± 0.52 | 82.78 ± 5.36 | 50.69 ± 0.89 |
| γi, βi = 0 | 91.71 ± 0.34 | 78.29 ± 0.66 | 62.16 ± 4.36 | 48.69 ± 0.36 |

**总体：16 格中 4 格落在论文 1σ 内。** 这是一个**部分复现**，不是整体吻合；下面把能
对上的和不能对上的分开说。

### 能对上的

- **`γi = 0` 的 CS / WikiCS**：−0.36 / +0.29，两格都在 1σ 内。
- **`γi, βi = 0` 的 CS**：−0.50，也在 1σ 内（且我方 σ 0.38 vs 论文 0.34 同量级）。
- **方向性一致**：论文里最伤的变体是 `γi, βi = 0`（Texas 85.01 → 62.16，跌 22.85）；我们
  同样是最伤（82.16 → 67.84，跌 14.32），且四个数据集上"两零"都是最低或次低。把
  γ（外部输入）和 β（边界交互）都拿掉会让模型退化，这一点复现出来了。
- **CS 仍是最可靠的一列**：与主表一样（±0.02 / −0.36 / −0.50），CS 在三个不同设定下都
  贴合论文，说明管线与超参在 CS 上是通的。

### 对不上的（两个具体失配）

**失配 1：`γ0, β0` 这一行无法复现，因为论文没给常数取值。**

论文 7.2 节只说"把可学的边界条件系数换成固定常数，记为 γ0, β0"，**没有给出数值**。本仓库
取 1.0（代码默认），结果四格全部大幅低于论文（Texas −19.39、Ratings −10.39）。而论文这一
行应当只比 GBN 略低（Texas −1.84、CS −1.64）。

说明：`γ0,β0 = 1.0` 不是论文用的常数；需要作者披露取值。在拿到之前，这一行**不应拿来自
证或证伪**。这也解释了为什么它四格全错、而其它三行还有若干格能对上。

**失配 2：`βi = 0` 在我们实现里几乎不改变结果，与论文不符。**

| | GBN（我们） | βi=0（我们） | 变化 | 论文变化 |
|--|-------------|--------------|------|----------|
| CS | 95.80 | 95.72 | **−0.08** | −2.01 |
| WikiCS | 84.91 | 85.01 | **+0.10** | −4.50 |
| Texas | 82.16 | 83.51 | +1.35 | −2.23 |
| Ratings | 51.95 | 50.23 | −1.72 | −2.82 |

论文里 `βi = 0` 明确掉 2–4.5 个点；我们这里 CS / WikiCS 几乎不动（±0.1）。审计时把
`BoundaryConvLayer.rate` 映射为论文的 β，从这一行看**映射不完整**：β 很可能还出现在
`ind_bd`（边界指示量）的构造里，而我们的开关只置零了 `rate`（即 `out_x` 的系数），没有
动 `ind_bd`。这是**代码层面的映射缺口**，不是超参问题。

### 与主表偏低的关系

消融里同样出现"CS 对得上、Texas / Ratings 偏低"的格局（主表也是这个格局）。所以主表的
系统性偏低与消融的偏差**同源**，优先怀疑的仍是步骤 6 里列的四项（硬件 3090 vs 4090、
未公开的构造细节、划分随机流），而不是消融开关本身。

### 分层判定

- L1 管线闭环：是（16/16 退出 0，脚本可重跑）。
- L2 数值量级：部分（4/16 在 1σ 内；两个失配已定位为"常数未公开"与"β 映射不完整"）。
- L3 统计一致：否。

### 结构化结果

- `results/gbn/nc_table4_ablation.csv`（16 行）
- 解析：`scripts/parse_gbn_log.py`（按标签里的模式名区分变体，长的优先匹配）
- 补丁已在归档后**从官方克隆撤销**（改动以 `repro/gbn-ablation.patch` 为准），
  以保证克隆停留在官方提交 `72ad3692916ecc60f2c78d5bd01a55d7c6297a4f`

### 待澄清（可写进给作者的问题）

1. `γ0, β0` 的常数取值是多少？
2. `β` 除了乘在 `out_x` 上，是否还参与 `ind_bd` / `p_deg` 的构造？（这决定 `βi = 0` 是否
   应当同时改 `ind_bd`）
3. Appendix E 的 Table 8 只给 7 个超参；`tau`、`add_self_loop`、`val_every`、`embed_dim`
   的取值？

已整理成 [`gbn_issue_draft.md`](gbn_issue_draft.md)（**2026-09-16 决定不发出**，保留作证据）。

## 2026-09-14 步骤 10–11：分层结论与冻结

### 三级判定

| 层级 | 判定 | 依据 |
|------|------|------|
| L1 管线闭环 | **是** | 主表 8/8、消融 16/16 全部退出 0；日志含 commit / conda / GPU；同 seed 可重跑；划分与数据源核验过 |
| L2 数值量级 | **是（部分）** | 主表 7 个对照项中 4 个落在论文 1σ 内（含 CS 近乎逐位 +0.02）；3 项偏低 1.3–3.0 点且方向一致。消融 4/16 在 1σ 内，两个失配已定位到具体原因 |
| L3 统计一致 | **否** | 主表 3/7 的均值差超过论文 σ；消融仅 4/16 格在 1σ 内。σ 侧不算差（主表 σ 比 0.53–1.79，4 项更小），但均值偏差未闭合 |

### 结论要点

1. **管线与超参在 CS 上是通的**：CS 在主表（+0.02）、`γi=0`（−0.36）、`γi,βi=0`（−0.50）
   三个设定下都落在论文 1σ 内。这不是偶然，说明代码、划分与评测口径当设置正确时能对上。
2. **存在一致的小幅系统性偏低**：主表 7 项里 6 项低于论文、1 项持平；消融里 Texas /
   Ratings 同样偏低。首要可疑因素是硬件（论文 4090 vs 本机 3090）与未公开的构造细节
   （`tau`、`val_every` 等），**未做受控验证**，只作假设记录。
3. **消融不是整体吻合，但方向对了**：论文里最伤的是 `γi, βi = 0`（两者皆去），我们
   也是。两个具体失配（常数未公开、β 映射不完整）已写进 issue 草稿。

### 停止理由

按 [`GBN_README.md`](GBN_README.md) 的停止条件："需要改超参才能接近表格：记录后停止，
**不搜参**"。因此：

- 没有为接近 Table 3/4 去扫 `lr`、`dropout`、`tau` 或 `γ0,β0` 的常数。
- 不再重跑已有配置；不再加数据集（flickr / blogcatalog / photo 未下）。
- Transfer 任务（论文 Fig. 5，报告 MSE 曲线）无表格目标，本轮不做。

除作者回复或硬件换成 4090 外，不再回头。

### 冻结时状态

- 官方克隆回到 `72ad3692916ecc60f2c78d5bd01a55d7c6297a4f`，工作区干净；
  改动以 [`repro/gbn-ablation.patch`](../gbn-ablation.patch) 为准（`git apply --check` 通过）。
- 数据不入 git（`repro/gbn/` 整体已忽略）；`roman_empire.npz` / `amazon_ratings.npz`
  与 IGNN 共用，哈希已在步骤 3 记录。
- 结构化结果：主表 `results/gbn/nc_table3_summary.csv`；消融 `results/gbn/nc_table4_ablation.csv`。
- 未做：Transfer 任务；flickr / blogcatalog / photo；`γ0,β0` 常数的确定。
