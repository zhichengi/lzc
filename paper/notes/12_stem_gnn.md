# 12 STEM_GNN（KDD 2026）

## 一句话
Generalizing GNNs with Tokenized Mixture of Experts

## 方法拆解
- 待精读论文第 3 节与官方入口后填写 → 代码位置 `repro/stem_gnn/`

## 实验协议
对照目标：先 finetune Cora 节点任务；预训练 `pretrain.py --pretrain_dataset all` 很重，有 ckpt 则跳过

## 论文写的 vs 代码做的
| 项 | 论文 | 代码 | 影响 |
|----|------|------|------|
| （审计摘要） | 见 `repro/STEM_GNN_REPRO_LOG.md` 步骤 4 |  |  |

## 依赖的基础知识（对应 LEARNING_PLAN 模块）
- M7

## 复现结论（冻结时填写）
预处理完成；L1/L2/L3 待全量。

## 可以延伸的点
- （全量后再写）
