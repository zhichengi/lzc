# 43 ScaDyG（TNNLS 2026）

*ScaDyG: A New Paradigm for Large-Scale Dynamic Graph Learning*。
复现日志：`repro/SCADYG_REPRO_LOG.md`。入口：`repro/SCADYG_README.md`。

## 一句话

快照式大规模动态图：预传播 + Transformer + Hypernetwork；论文 MOOC 链接预测 MRR 0.931 ± 0.009。

## 方法拆解

- 时间感知拓扑 / 指数时间编码 / Hypernetwork 自适应聚合 → `model/`、`transformer/`（消融开关尚未做成 CLI）
- 官方评测：每源取最佳正边 + 从全部节点抽 100 负样本
- 严格协议：逐正边、合法 item、当前快照 filtered full-item → `model/eval_protocols.py`

## 实验协议

MOOC 70/15/15 时间划分；主指标 MRR。发布代码用 AP 早停。本机 RTX 3090，环境 `scadyg`。

## 论文写的 vs 代码做的

| 项 | 论文 | 代码 |
|----|------|------|
| checkpoint | 应能恢复最佳模型 | 默认只存预测层，修之前 test MRR ~0.025 |
| 选模 | MRR 主指标 | AP 早停 |
| 排名 | 「100 个负样本」 | 每源一条最佳正边 + 全节点负采样，不是 TGB 式逐正边 |

## 依赖的基础知识

- M4：快照 vs 事件流、TGB 评测、二部图负采样
- M3：预传播 / SIGN 系可扩展思路

## 复现结论（未冻结）

L1 是。L2 是：checkpoint + MRR 选模后 **0.922 ± 0.014** vs 0.931 ± 0.009。L3 否（方差偏大；严格协议仅 0.204）。消融与 BitcoinAlpha 待做。

## 可以延伸的点

- 三个组件的消融开关（默认路径禁止改）
- 用 TGB Evaluator 重评保存的 `best_*.pt`
- 把 checkpoint bug 整理成 upstream issue（草稿 `repro/scadyg_issue_draft.md`，未发出）
- 完整叙述见 `repro/SCADYG_REPORT.md`
