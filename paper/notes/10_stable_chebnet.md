# 10 STABLE_CHEBNET（NeurIPS 2025 Spotlight）

## 一句话
Return of ChebNet: Understanding and Improving an Overlooked GNN on Long-Range Tasks

## 方法拆解
- 待精读论文第 3 节与官方入口后填写 → 代码位置 `repro/stable_chebnet/`

## 实验协议
对照目标：Peptides-func / Peptides-struct（LRGB）；Barbell 与 GraphProp 为合成/属性任务

## 论文写的 vs 代码做的
| 项 | 论文 | 代码 | 影响 |
|----|------|------|------|
| 测试用模型 | 最佳 val | **checkpoint 保存/加载被注释**（`:195`、`:206-207`）→ 用末 epoch 模型 | 放弃最佳 val（70.35）改用末 epoch（69.76） |
| 损失 | LRGB 惯用 `BCEWithLogitsLoss` | `nn.CrossEntropyLoss()` 作用于 `[B,10]` | 把多标签当互斥软标签，改变优化目标 |
| metrics 打印 | AP | `eval_ap()` 实为 sklearn `average_precision_score`，但日志标签写作 `Acc` | 口径正确，命名误导 |
| 位置编码 | 强调不依赖 PE | `pos_enc="None"`，脚本里 `AddLaplacianEigenvectorPE` 构造但未用 | 与论文一致 |

## 依赖的基础知识（对应 LEARNING_PLAN 模块）
- M1（谱滤波 / ChebNet）、M5（图级任务 / LRGB）

## 复现结论（2026-09-16，步骤 6）

- **L1 是**：真实 LRGB 数据（15,535/2,344,859/4,773,974 与论文 Table 1 逐项吻合），
  200 epoch 退出 0，55.5 分钟。
- **L2 部分**：单 run **Test AP 67.869** vs 论文 **70.32 ± 0.26**，差 −2.45；
  候选原因已定位两条（末 epoch 评测、损失函数口径），待步骤 7 对照。
- **L3 未评估**：仅 1 seed。
- 观测：Train AP 升到 95%，Val AP 在 epoch 30 后长期停在 0.69–0.70（已过拟合）。

## 可以延伸的点
- 量化“最佳 val 模型 vs 末 epoch 模型”的差异（不动官方默认路径）
- 查官方是否有 BCE 版本的脚本/说明
- 多种子（3–5 次）对 70.32 ± 0.26
- Peptides-struct（`ChebStable_Struc.py`）尚未跑
