# IGNN 复现

论文：*Making Classic GNNs Strong Baselines Across Varying Homophily: A Smoothness–Generalization Perspective*（NeurIPS 2025）。论文库编号 11。

- 官方仓库：`repro/ignn/`，固定提交 `7a1bb0adb3ccb78e193276e181cbf8d2090ed61f`
- 过程日志：[`IGNN_REPRO_LOG.md`](IGNN_REPRO_LOG.md)
- custom split 准备单：[IGNN_CUSTOM_SPLIT.md](IGNN_CUSTOM_SPLIT.md)；排队脚本 `repro/run_ignn_custom_cignn.sh`（默认只打印，不训练）
- 运行入口：工作区根目录 `bash repro/run_ignn.sh LABEL args...`（已接入 85% 资源上限）
- 读书笔记：`paper/notes/11_ignn.md`
- 环境：`/home/lab_user/tools/miniconda3/envs/ignn`（Python 3.8.16、PyTorch 2.1.2+cu121、PyG 2.4.0、DGL 2.0.0）

## 当前状态

- **public split（c-IGNN）已冻结**：Actor / PubMed / WikiCS 为严格 public mask；chameleon / roman-empire 因 `graph_datasets` 丢 NPZ mask，实际读的是仓库 48/32/20 npy，超参仍来自 public 脚本。数字见 [`results/SUMMARY.md`](../results/SUMMARY.md)。
- **custom split 未跑**。划分已核验。GPU 空闲后：

```bash
# 默认只打印命令
bash repro/run_ignn_custom_cignn.sh
# 真正训练（三个烟雾 + 三个 10-run）
IGNN_EXECUTE=1 bash repro/run_ignn_custom_cignn.sh
```

## 不要做的事

- 不要把 chameleon / roman-empire 的 public 数字当成 custom 结果。
- 不要改 `graph_datasets` 去补跑“真 public”后再与已冻结表混排。
- 不要搜参、不要跑 30 个基线、不要跑 arxiv / products / pokec。
- 不要把 `repro/ignn/` 这个带独立 `.git` 的官方克隆直接加入根仓库。
