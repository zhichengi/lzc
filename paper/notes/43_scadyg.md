# 43 ScaDyG（TNNLS 2026）

*ScaDyG: A New Paradigm for Large-Scale Dynamic Graph Learning*。
复现日志：`repro/SCADYG_REPRO_LOG.md`。入口：`repro/SCADYG_README.md`。

## 一句话

快照式大规模动态图：预传播 + Transformer + Hypernetwork；论文 MOOC 链接预测 MRR 0.931 ± 0.009。

## 方法拆解

- 时间感知拓扑 / 指数时间编码 / Hypernetwork 自适应聚合 → `model/`、`transformer/`（已做成 `--ablate {none,time,topo,hyper}`，默认 `none` 走官方路径）
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

## 复现结论（2026-09-16 定稿，可冻结）

- **L1 是**；**L2 是**：checkpoint-fix + MRR 选模后 MOOC **0.922 ± 0.014** vs 论文 0.931 ± 0.009；**L3 否**（方差 0.014 > 0.009，且论文未给 seed 列表）。
- 严格 item 协议同一批 checkpoint 仅 **0.204 ± 0.004**：说明 0.93 与 0.20 的差距来自**评测候选与排名单位**，不是训练负采样（改成合法 item 负采样后 filtered 不变）。
- 消融（seeds 0–4）：`none` 0.9225 > `time` 0.8277 ≈ `hyper` 0.8032 ≫ `topo` **0.0099**（随机）。`topo` 是模型能工作的前提，非可选增强；5 seed 数值完全一致（确定性结构性失效）。
- BitcoinAlpha 第二数据集（SNAP 原始数据 + 723000 秒切片 = 226 快照）：5 seed **0.719470 ± 0.006932**，L1 闭环，不与 MOOC 论文数值直接比较。
- 完整源码补丁：`repro/scadyg-current.patch`（基线 `28ca94a`，已在干净 worktree 应用并逐字节比对、通过编译）。

## 可以延伸的点

- 用 TGB `Evaluator` 重评保存的 `best_*.pt`，解释与 filtered MRR 的差异（M4 检验标准之一）
- UCI 数据集（未跑）
- checkpoint bug 的 upstream issue（草稿 `repro/scadyg_issue_draft.md`，**未发出**，待决定）
- 完整叙述见 `repro/SCADYG_REPORT.md`
