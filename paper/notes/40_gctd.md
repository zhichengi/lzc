# 40 GCTD（WSDM 2026）

*Multi-view Graph Condensation via Tensor Decomposition*。
复现日志：`repro/REPRO_LOG.md`。入口：`repro/GCTD_README.md`。

## 一句话

用 CP/Tucker 把原图压成少量超点的合成图，在合成图上训 GCN、在原图上测；论文 Cora 1.3% 报 81.4 ± 1.6。

## 方法拆解

- 张量分解学习超点特征 / 邻接核 → `repro/gctd/src/models/gctd.py`
- `to_edge_index` 阈值 0.05 把核变成边
- 评测：合成图训练、原图 val/test

## 实验协议

压缩比 1.3%（Cora 约 35 超点）；10 seed；指标准确率。官方未公开完整 wandb 超参。

## 论文写的 vs 代码做的

| 项 | 论文 | 代码 |
|----|------|------|
| 合成邻接稀疏 | ReLU / 阈值带来稀疏 | 默认 `lr_rec=0.001` 时核值 > 0.05，必得完全图，GCN 过平滑到 ~30% |
| 超点特征 | 簇内平均（文字） | class+split 原型；改成簇内平均在 Cora 上变差 |
| ogbn-arxiv | README 写自动下载 | 按 GraphSAINT 文件格式读，不用 OGB |

## 依赖的基础知识

- M2：GCond 协议、CP/Tucker、过平滑
- M0：完全图上 GCN 输出趋于常数

## 复现结论（未冻结）

L1 是。L2 部分：建议命令 10-run **66.0 ± 9.4**，单次最好 76.3%。L3 否。Cora 总表：`results/gctd/cora_summary.csv`。不再扫 Cora。issue 草稿：`repro/gctd_issue_draft.md`（未发出）。

## 可以延伸的点

- Citeseer / Pubmed 看差距是否 Cora 特有
- GraphSlim 上跑 GCond，确认评测代码本身能否打出公认数字
- 向作者要 Table 2 完整超参
