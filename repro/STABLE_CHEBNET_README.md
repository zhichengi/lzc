# 10 STABLE_CHEBNET 预处理 / 复现入口

论文：*Return of ChebNet: Understanding and Improving an Overlooked GNN on Long-Range Tasks*（NeurIPS 2025 Spotlight）。论文库编号 10。学习模块：`LEARNING_PLAN.md` M1,M5。

- 官方仓库：`repro/stable_chebnet/`（https://github.com/ahariri13/Stable-ChebNet）
- 固定提交：`7d7a7e2696119891d277fd3fa2b32fdda454b814`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[STABLE_CHEBNET_REPRO_LOG.md](STABLE_CHEBNET_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/10_Stable-ChebNet_NeurIPS2025.pdf`
- 读书笔记：`paper/notes/10_stable_chebnet.md`
- 运行产物：`results/stable_chebnet/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-16 更新）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | `dtgb`（烟雾已跑通，未新建环境） |
| 数据 | **Peptides-func 已就绪**：Dropbox 不通，改走 `hf-mirror`（见下）；train/val/test = 10,873 / 2,331 / 2,331 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | **已用真实数据跑通**：官方脚本 2ep，退出 0，参数 659,069 |
| 全量 | `FULL=1 bash repro/run_stable_chebnet_full.sh`（默认 dry-run） |

对照目标：Peptides-func / Peptides-struct（LRGB）；Barbell 与 GraphProp 为合成/属性任务

## 数据获取（不依赖 Dropbox）

官方 `LRGBDataset` 从 Dropbox 拉 `peptidesfunc.zip`，本机不可达。改写后的入口走 HF 镜像：

```bash
bash repro/download_stable_chebnet.sh
```

它下载两份并对图顺序、划分完整性、分层性做校验，再由
`repro/build_stable_chebnet_peptides.py` 还原成 PyG 需要的 `raw/{train,val,test}.pt`：

| 来源 | 文件 | SHA-256 |
|------|------|---------|
| `LRGB/peptides-functional` | `geometric_data_processed.pt` | `0a5fe87d…2db1fd` |
| `scikit-fingerprints/LRGB_Peptides-func` | `lrgb_splits_peptides_func.json` | `39ca1b14…f85b14` |

**待确认**：划分取自 scikit-fingerprints 镜像，非官方 Dropbox 的
`splits_random_stratified_peptide.pickle`；尺寸与分层性吻合，但未逐位比对。详见日志步骤 3。

## 烟雾（短）

```bash
export WANDB_MODE=offline
bash repro/run_stable_chebnet.sh smoke_peptides_2ep -- bash -c 'cd Peptides/Stable && python ChebStable_peptide.py --epochs 2'
```

官方脚本已有 `--epochs`（配置默认 200）。Barbell 在 dtgb/PyG 2.8 下会因 `normalize=` 失败，
不要当主表烟雾。

## 全量（默认不跑）

```bash
bash repro/run_stable_chebnet_full.sh          # 只打印命令
FULL=1 bash repro/run_stable_chebnet_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
