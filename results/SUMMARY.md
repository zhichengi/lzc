# 复现结果总表

每完成一条线的关键步骤或冻结时更新一次。判定标准见 `REPRO_ROADMAP.md` 第 5 节（L1 管线闭环 / L2 数值量级 / L3 统计一致）。
数字单位：节点分类为准确率 %，动态链接预测为 MRR。更新于 2026-09-13。

| 编号 | 论文 | 数据集 / 设定 | 论文数值 | 我们（官方协议） | 我们（修正 / 严格协议） | L1 | L2 | L3 | 状态 | 日志 |
|------|------|---------------|----------|------------------|--------------------------|----|----|----|------|------|
| 11 | IGNN（NeurIPS 2025） | Actor public，c-IGNN，10 划分 | 38.01 ± 1.11（V100） | **37.43 ± 0.97** | — | 是 | 是 | 是* | public 已冻结 | `repro/IGNN_REPRO_LOG.md` |
| 11 | IGNN | chameleon public，10 划分 | 49.04 ± 4.68 | **49.55 ± 3.25** | — | 是 | 是 | 是* | 已冻结；加载器丢 NPZ mask，实际读仓库 npy | 同上 |
| 11 | IGNN | pubmed public，3 次 | 80.03 ± 0.37 | **79.63 ± 0.26** | — | 是 | 是 | n=3 | 已冻结 | 同上 |
| 11 | IGNN | wikics public，20 次 | 80.55 ± 0.43 | **80.46 ± 0.41** | — | 是 | 是 | 是* | 已冻结 | 同上 |
| 11 | IGNN | roman-empire public，10 划分 | 90.75 ± 0.51 | **90.64 ± 0.40** | — | 是 | 是 | 是* | 已冻结；协议同 chameleon（npy 而非 NPZ mask） | 同上 |
| 43 | ScaDyG（TNNLS 2026） | MOOC 链接预测，seeds 0–4 | 0.931 ± 0.009 | **0.922 ± 0.014**（MRR 选模）；0.915 ± 0.009（AP 选模） | 严格 item 排名协议 **0.204 ± 0.004** | 是 | 是 | 否 | 报告初稿已有；消融与第二数据集待做 | `repro/SCADYG_REPORT.md` |
| 40 | GCTD（WSDM 2026） | Cora 1.3%，seeds 0–9 | 81.4 ± 1.6 | 官方默认 30.2%（完全图） | topk+配额+重试 **66.0 ± 9.4**；单次最好 76.3% | 是 | 部分 | 否 | Cora 总表已收；待 Citeseer/Pubmed 与作者回复 | `results/gctd/cora_summary.csv` |
| 29 | SGPC（AAAI 2026） | 6 异配 10 划分；Cora/Citeseer 5 seed；Pubmed lobpcg | 见表下 | val 选模低于 oracle；Wisconsin 偏高；Pubmed 78.10/78.70 vs 79.9 | 协议开关默认关 | 是 | 部分 | 否 | 步骤 7：6 个异配集 ×10 划分完成 | `repro/SGPC_REPRO_LOG.md` |

\* IGNN 的 L3 按"均值差 < 官方 σ 且方差同量级"成立，但硬件为 RTX 3090 而官方为 V100，作者自己也报告了两者差异，
因此只表述为"官方配置在 3090 上达到与 V100 表一致的水平"。chameleon / roman-empire 的 `--public True` 因 `graph_datasets` 不读 NPZ mask，实际使用仓库固定 48/32/20 npy，不能称为严格 public。

IGNN custom split（论文主协议）尚未训练，准备单：`repro/IGNN_CUSTOM_SPLIT.md`。

## SGPC（步骤 7，不能当 L3）

对照论文 Table 1 SGPC 行。正式数字用 **val 选模**（首次最高 val 的 test）；`oracle` = 官方 `Best Test`（test 取 max）。总表：`results/sgpc/protocol_summary.csv`。

步骤 6 单次划分 0（历史）：

| 数据集 | val 选模 | oracle | 论文 |
|--------|----------|--------|------|
| Cora | 81.7 | 83.5 | 83.0 ± 0.55 |
| Citeseer | 73.3 | 73.3 | 72.6 ± 0.21 |
| Actor | 38.29 | 38.88 | 38.1 ± 0.52 |
| Chameleon | 50.88 | 51.54 | 53.3 ± 1.29 |
| Squirrel | 36.12 | 36.22 | 36.0 ± 0.30 |
| Cornell | 81.08 | 81.08 | 81.0 ± 2.33 |
| Texas | 81.08 | 83.78 | 83.2 ± 1.82 |
| Wisconsin | 84.31 | 84.31 | 81.1 ± 2.60 |
| Pubmed | — | — | 79.9 ± 0.06 |

步骤 7 多划分 / 多种子：

| 设定 | 我们 val | 我们 oracle | 论文 |
|------|----------|-------------|------|
| Cora public 5 seed | 82.06 ± 1.23 | 82.58 ± 1.13 | 83.0 ± 0.55 |
| Citeseer public 5 seed | 71.16 ± 1.26 | 72.02 ± 0.79 | 72.6 ± 0.21 |
| Pubmed lobpcg seed 0 | 78.10 | 78.70 | 79.9 ± 0.06 |
| Actor 10 划分 | 36.12 ± 1.24 | 37.13 ± 0.90 | 38.1 ± 0.52 |
| Chameleon 10 划分 | 51.91 ± 2.04 | 52.83 ± 2.02 | 53.3 ± 1.29 |
| Cornell 10 划分 | 77.57 ± 4.42 | 80.54 ± 3.99 | 81.0 ± 2.33 |
| Squirrel 10 划分 | 35.93 ± 1.50 | 37.08 ± 1.22 | 36.0 ± 0.30 |
| Texas 10 划分 | 80.27 ± 6.25 | 85.41 ± 4.63 | 83.2 ± 1.82 |
| Wisconsin 10 划分 | 83.53 ± 4.91 | 87.45 ± 2.81 | 81.1 ± 2.60 |

## 已确认的失配类型

| 论文 | 类型 | 内容 |
|------|------|------|
| GCTD | 超参未公开 + 实现与论文文字不一致 | README 默认 `lr_rec=0.001` 下 0.05 阈值必得完全图；合成特征取 class+split 原型而非簇内平均 |
| ScaDyG | 代码 bug + 协议与论文文字不一致 | 只保存预测层 checkpoint（修复后 0.025 → 0.928）；AP 选模 vs MRR 主指标；排名评测每源取最佳正边 + 全节点负采样 |
| IGNN | 硬件与环境；critical public 协议 | V100 vs RTX 3090；作者自述 chameleon 50.79 → 47.53；`graph_datasets` 丢 NPZ public mask |
| SGPC | 协议与论文文字不一致 | 论文写每类 20 个随机训练节点，代码用 PyG 自带 split（异配集默认第 0 组）；`Best Test` 为 test 选模；无 seed；稠密 `eigvalsh` 在 Citeseer 上可失败，Pubmed 必须 lobpcg |
