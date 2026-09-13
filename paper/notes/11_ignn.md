# 11 IGNN（NeurIPS 2025）

*Making Classic GNNs Strong Baselines Across Varying Homophily: A Smoothness–Generalization Perspective*。
复现日志：`repro/IGNN_REPRO_LOG.md`。入口：`repro/IGNN_README.md`。

## 一句话

用初始残差、中间归一化、表示归一化把经典 GCN 做成跨同配/异配都强的 baseline（c/r/a-IGNN）；本轮只复现 public split 的 c-IGNN。

## 方法拆解

- `IN` / `RN` / `n_hops`：对应论文平滑–泛化开关 → `ignn/models/IGNN.py`、`IGNNConv.py`
- public vs custom：`--public True` 读数据加载器 mask；False 读仓库 `*-48-32-splitsx10.npy`
- 选模：验证集；`--repeat` 在同一进程内连续跑多个划分（不每划独立设 seed）

## 实验协议

官方 `scripts/00-best-racIGNN-public.sh`；对照 `repro/ignn/results/table_pub.csv`（Tesla V100）。本机 RTX 3090、Python 3.8.16、torch 2.1.2+cu121。

## 论文写的 vs 代码做的

| 项 | 论文 / 仓库表 | 代码 |
|----|----------------|------|
| critical 数据集 public | NPZ 内 10 组 mask | `graph_datasets` 不读这些 mask，回退到仓库 npy |
| `--repeat 10` | 常被理解成独立种子 | 同一进程连续 RNG |
| 硬件 | V100 表；README 承认 3090 会偏 | 本机 3090 |

## 依赖的基础知识

- M0：public vs random split、早停与选模
- M1：同配性、过平滑、IGNN 的 n_hops / IN / RN

## 复现结论（public 已冻结）

L1 / L2 达到。L3 按「均值差 < 官方 σ」在 Actor / wikics / roman-empire / chameleon 上成立，但硬件不同，且后两个协议不纯。custom split 未跑。

## 可以延伸的点

- 修加载器读 NPZ mask，单独成表，不与已冻结 public 混排
- custom 48/32/20 三数据集（准备单已写）
