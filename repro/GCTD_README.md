# GCTD 复现

论文：*Multi-view Graph Condensation via Tensor Decomposition*（WSDM 2026）。论文库编号 40。

- 官方仓库：`repro/gctd/`（https://github.com/nicolasrsantos/gctd）
- 过程日志：[REPRO_LOG.md](REPRO_LOG.md)
- Cora 总表：`results/gctd/cora_summary.csv`
- 向作者求证草稿（未发出）：[gctd_issue_draft.md](gctd_issue_draft.md)
- 本地论文：`papers/gnn-frontier-2025-2026/10-wsdm/40_GCTD_WSDM2026.pdf`
- 读书笔记：`paper/notes/40_gctd.md`

## 当前结论

Cora 1.3%：官方默认约 30%（合成图塌成完全图）→ 建议命令 10-run **66.0 ± 9.4**（`dtgb`，topk + 配额 + 重试）；单次最好 76.3%。论文 **81.4 ± 1.6**。L1 达到，L2 部分，L3 否。按冻结规则不再在 Cora 上扫参；下一步是 Citeseer / Pubmed 与向作者求证，见 `CLOSEOUT_PLAN.md` R-GCTD-*。

## 目录

```
repro/gctd/                 # 官方代码 + 少量移植补丁（路径、wandb、num_workers）
    ├── data/               # Planetoid 等（不入 git）
    └── saved_ours/         # 压缩图缓存（不入 git）
repro/run_gctd.sh
repro/requirements-gctd.txt
results/gctd/runs/
```

相对路径由 `repro/gctd/src/utils/paths.py` 锚定到 `repro/gctd/`，与从哪启动无关。

## 环境

入口脚本**优先用 `gctd`**：

| 环境 | 用途 |
|------|------|
| `gctd` | 与官方钉扎对齐：Python 3.11、torch 2.1.2+cu121、pyg 2.6.1 |
| `dtgb` | 工作区原环境：torch 2.2.1+cu121、pyg 2.8；作对照 |

```bash
bash scripts/setup_gctd_conda.sh     # 新建/修复官方钉扎环境（不改 dtgb）
conda activate dtgb && bash scripts/setup_gctd_env.sh   # 只在 dtgb 里补缺的包
```

对齐官方版本**没有**把 Cora 10 次平均抬到 81.4%（钉扎环境 61.0 ± 13.1）。

`dtgb` 里 wandb 0.19.6 曾把 protobuf 降到 5.x，与 tensorboard 2.21 冲突。GCTD 默认 `--no_wandb`，一般不必修。

## 运行

在**工作区根**执行（会自动 `conda activate gctd`）：

```bash
# 建议：不塌缩的压缩学习率 + topk 稀疏化
bash repro/run_gctd.sh cora 0.013 --num_workers 0 --lr_rec 0.01 --edge_topk 12

# GCond 协议（Cora 上未超过上一行，不要当默认）
bash repro/run_gctd.sh cora 0.013 --num_workers 0 --gcond_protocol 1 --weighted 0 \
  --lr_rec 0.01 --rec_proj 1 --edge_topk 12
```

日志：`results/gctd/runs/<时间戳>_cora.log`。

## 数据

不要让 PyG 直连 GitHub。先放本地：

```bash
bash repro/download_planetoid.sh cora      # 小写目录名
# bash repro/download_planetoid.sh citeseer
# bash repro/download_planetoid.sh pubmed
```

文件落在 `repro/gctd/data/cora/raw/`（必须小写，与 `Planetoid(..., "cora")` 一致）。

Flickr / Reddit 需自行把 GraphSAINT 文件放到 `repro/gctd/data/flickr` 与 `repro/gctd/data/reddit`。`ogbn-arxiv` 在官方代码里按 GraphSAINT 文件格式读取，**不会**走 OGB 自动下载。
