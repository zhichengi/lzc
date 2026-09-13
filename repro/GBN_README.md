# 09 GBN 预处理 / 复现入口

论文：*Deeper with Riemannian Geometry: Overcoming Oversmoothing and Oversquashing for Graph Foundation Models*（NeurIPS 2025）。论文库编号 09。学习模块：`LEARNING_PLAN.md` M1。

- 官方仓库：`repro/gbn/`（https://github.com/ZhenhHuang/GBN）
- 固定提交：`72ad3692916ecc60f2c78d5bd01a55d7c6297a4f`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[GBN_REPRO_LOG.md](GBN_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/09_Riemannian_GBN_NeurIPS2025.pdf`
- 读书笔记：`paper/notes/09_gbn.md`
- 运行产物：`results/gbn/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-13 更新）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上（未改动；改动以 `repro/gbn-ablation.patch` 为准） |
| 环境 | **`dtgb`**（Python 3.10.20、torch 2.2.1+cu121、PyG 2.8、torch_scatter 可用）。未新建 `gbn` 环境 |
| 数据 | **8/8 就绪**，含论文 Table 3 的 7 个数据集 + 额外 Cora。节点/边数与论文 Table 7 吻合 |
| 配置 | `results/gbn/configs/<DS>.json`（论文 Table 8 超参，含必需的 `layer_wise`） |
| 主表 | `repro/run_gbn_table.sh`（8 数据集 × 10 iters） |
| 消融 | `repro/run_gbn_ablation.sh` + `repro/gbn-ablation.patch`（论文 Table 4） |
| 解析 | `scripts/parse_gbn_log.py` |

对照目标：论文 Table 3（节点分类 ACC）与 Table 4（消融）。

## 当前结果（2026-09-14）

**主表（论文 Table 3）**已跑完：8 数据集 ×10 iters（22:29→00:11）。7 个论文对照项中
**4 个落在论文 1σ 内**：

| 数据集 | 我们（3090） | 论文（4090） | 差 | < 1σ |
|--------|--------------|--------------|-----|------|
| CS | **95.80 ± 0.28** | 95.78 ± 0.21 | +0.02 | 是 |
| computers | **91.12 ± 0.37** | 91.33 ± 0.32 | −0.21 | 是 |
| Wisconsin | **85.29 ± 3.43** | 86.78 ± 3.84 | −1.49 | 是 |
| Texas | **82.16 ± 3.46** | 85.01 ± 6.51 | −2.85 | 是 |
| Amazon-ratings | 51.95 ± 0.51 | 53.51 ± 0.88 | −1.56 | 否（1.8σ） |
| WikiCS | 84.91 ± 0.70 | 86.21 ± 0.39 | −1.30 | 否（3.3σ） |
| Roman-empire | 86.87 ± 0.43 | 89.83 ± 0.46 | −2.96 | 否（6.4σ） |

**消融（论文 Table 4）**已跑完：4 变体 × 4 数据集（00:14→04:46）。**4/16 格落在 1σ 内**，
并定位两个失配：`γ0, β0` 的常数论文未公开（我们取 1.0，过度退化）；`βi = 0` 在我们实现里
几乎无效（β 映射不完整）。详见 [`GBN_REPRO_LOG.md`](GBN_REPRO_LOG.md)。

### 为什么必须注入配置 json

`main.py` 的 argparse **没有** `layer_wise`，但 `node_classification.py:load_model`
读 `configs.layer_wise`。官方只预置了 `configs/NC/CS.json`，其余数据集首次运行时
`main.py` 会把 CLI 值另存一份 json —— 里面没有 `layer_wise`，随即
`AttributeError: 'Namespace' object has no attribute 'layer_wise'`。

因此外层用 `scripts/gen_gbn_configs.py` 按论文 Table 8 生成配置到
`results/gbn/configs/`（入库），运行时由 `run_gbn_table.sh` 拷进
`repro/gbn/configs/NC/`（官方克隆不入库）。

```bash
conda run -n dtgb python scripts/gen_gbn_configs.py --smoke --ablation
```

### 数据来源与哈希

- **复用已有**：`roman_empire.npz`、`amazon_ratings.npz` 直接来自
  `repro/ignn/data/`（哈希见 `IGNN_CUSTOM_SPLIT.md`）。PyG
  `HeterophilousGraphDataset` 的 `raw` 路径是
  `<root>/<name.lower().replace('-','_')>/raw/<name>.npz`，所以放到
  `repro/gbn/datasets/roman_empire/raw/` 与 `.../amazon_ratings/raw/` 即被识别，
  无需联网。
- **PyG 下载**：CS / computers / WikiCS（Coauthor / Amazon / WikiCS），走 GitHub
  raw，可直连。
- WebKB（Texas / Wisconsin）与 Planetoid（Cora）此前已下。
- **注意**：`load_data` 里 `Amazon-ratings` / `Roman-empire` 用的是连字符名字，
  经 PyG 规范化后对应 `amazon_ratings` / `roman_empire` 目录；而 `computers` 走
  `Amazon(root, name='computers')`（PyG 内部映射到 `amazon_computers`）。

## 主表（论文 Table 3）

```bash
# 烟雾（2 epoch，验证管线与计时；exp_iters 保持 10，见下）
EXECUTE=1 SMOKE=1 bash repro/run_gbn_table.sh

# 全量（8 数据集 × 10 iters，小→大排序）
EXECUTE=1 DATASETS="Texas Wisconsin Roman-empire Amazon-ratings CS WikiCS computers Cora" \
  bash repro/run_gbn_table.sh
```

**烟雾不能把 `exp_iters` 设成 1**：官方 `node_classification.py` 用
`data.train_mask[:, split]`，要求 2-D 掩码；CS / WikiCS / computers / Cora 走
`RandomNodeSplit`，当 `num_splits=1` 时掩码退化为 1-D，会
`IndexError: too many indices for tensor of dimension 1`。
WebKB / Heterophilous 用数据集原生 `[N, 10]` 掩码，不受影响。烟雾只减
`epochs_nc`。

## 消融（论文 Table 4）

```bash
# 前置：应用补丁（默认关闭，ablate=none 与官方逐位一致）
cd repro/gbn && git apply ../gbn-ablation.patch && cd -

EXECUTE=1 bash repro/run_gbn_ablation.sh
# 默认 5 变体 × {CS, WikiCS, Texas, Amazon-ratings}
```

变体语义（论文 7.2 节）：`gamma_all0`（γ_i=0，去外部输入）、`beta_all0`
（β_i=0，去边界交互）、`gamma_beta_all0`（两者皆零，论文称退化为 GCN）、
`gamma0_beta0`（两者换固定常数）。**论文未给出 `γ0,β0` 的常数取值**，本仓库取
1.0，属待澄清项。

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
