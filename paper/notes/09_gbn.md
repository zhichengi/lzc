# 09 GBN（NeurIPS 2025）

## 一句话
Deeper with Riemannian Geometry: Overcoming Oversmoothing and Oversquashing for Graph Foundation Models

## 方法拆解
- 待精读论文第 3 节与官方入口后填写 → 代码位置 `repro/gbn/`
- 代码侧已核：`BoundaryConvLayer` 是核心。`ind_bd` 是边界指示量（由 `ind_layer` 的
  `logsigmoid` 得出，即论文里"离边界多远"的量），`rate` 是乘在 `out_x`（边界→内部
  方向的聚合）上的可学系数，`gamma`（= `self.gamma(x0)`）是逐层加在输出上的外部输入项。
  论文记号的对应关系见 `repro/GBN_REPRO_LOG.md` 步骤 7 的映射表。

## 实验协议
对照目标：论文 Table 3（7 个数据集的节点分类 ACC，10 runs）与 Table 4（5 个消融变体 ×
4 数据集）；另有 Transfer 任务（Fig. 5，MSE 曲线）。
超参取 Appendix E Table 8；`layer_wise` 必须由 config json 注入（argparse 里没有）。

## 论文写的 vs 代码做的
| 项 | 论文 | 代码 | 影响 |
|----|------|------|------|
| `layer_wise` 来源 | 未提 | argparse 里**没有**，只有 `configs/NC/CS.json` 有；其它数据集首次运行会生成缺字段的 json | 非 CS 数据集直接 `AttributeError`，须外层注入配置 |
| `γ0, β0` 常数 | 只说"换成固定常数"，**未给数值** | 无对应开关 | Table 4 该行无法复现（取 1.0 时 Texas −19.39） |
| `β` 的位置 | β_i=0 掉 2.0–4.5 点 | 只把 `rate` 置零时 CS/WikiCS 仅 ±0.1 | 推测 β 还参与 `ind_bd`/`p_deg`，映射不完整 |
| Table 8 超参 | 只列 7 项 | `tau`/`add_self_loop`/`val_every`/`embed_dim` 靠代码默认 | 主表系统性偏低的可疑来源之一 |
| 划分 | "10 random splits" | `RandomNodeSplit(num_splits=10, num_val=0.2, num_test=0.2)`；`set_seed(3047)` 写死在 `main.py` | 划分随机流是否与作者一致无法核验 |

## 依赖的基础知识（对应 LEARNING_PLAN 模块）
- M1：过平滑 / 过挤压、谱间隙、黎曼边界条件

## 复现结论（冻结时填写）
主表 8/8、消融 16/16 均完成（2026-09-14）。

- **L1 是**；**L2 是（部分）**：主表 7 个论文对照项中 4 个在 1σ 内（CS 95.80 vs 95.78，
  +0.02；computers −0.21；Wisconsin −1.49；Texas −2.85），其余 3 项偏低 1.3–3.0 点且
  方向一致。消融 4/16 格在 1σ 内。**L3 否**。
- 最值得记的一条：**CS 在三个不同设定下都贴合论文**，说明"管线是通的"；而其它数据集
  一致偏低，指向硬件与未公开细节，而不是实现错误。
- 两个已定位的失配：`γ0,β0` 常数未公开；`βi=0` 的代码映射不完整。见
  [`repro/gbn_issue_draft.md`](../../repro/gbn_issue_draft.md)（**2026-09-16 决定不发出**，保留作证据）。

## 可以延伸的点
- 若换到 RTX 4090 重跑主表，可直接检验"硬件差异"这个假设（当前只是未验证的推测）。
- Transfer 任务（Fig. 5）未做：论文以 MSE 曲线呈现，无表格数值，评估口径需要先定义。
- `γ0, β0` 一旦由作者给出，Table 4 那一行可以立刻补上。
