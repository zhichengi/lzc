# 边复现边学习：GNN 论文复现学习计划

> 目标读者：本人。目标：以 `papers/gnn-frontier-2025-2026/` 的 46 篇论文为驱动，
> 通过逐篇复现把图神经网络的基础知识补完整，同时形成一套可迁移的复现方法论。
>
> 配套文档：
> - 论文复现队列与标准流程：[`REPRO_ROADMAP.md`](REPRO_ROADMAP.md)
> - 已开线的收尾细节：[`repro/CLOSEOUT_PLAN.md`](repro/CLOSEOUT_PLAN.md)
> - 论文库总说明与评级：[`papers/gnn-frontier-2025-2026/README.md`](papers/gnn-frontier-2025-2026/README.md)
> - 工作区入口与四条线现状：[`README.md`](README.md)
> - 顶层数字：[`results/SUMMARY.md`](results/SUMMARY.md)

---

## 1. 计划的组织方式

学习不是先把教材读完再动手，而是**每一篇复现的论文决定这一段要补哪些基础**。
因此本计划分为：

1. **知识模块**（第 3 节）：把 46 篇论文涉及的基础知识拆成 9 个模块，每个模块写清"必须会什么、读什么、用哪篇论文来练、怎么检验"。
2. **阶段时间线**（第 4 节）：按 `REPRO_ROADMAP.md` 的复现队列排出阶段，每阶段对应若干模块。
3. **每周节奏与产出**（第 5、6 节）：固定的读 / 做 / 写循环和笔记模板。

复现顺序服从"知识依赖"而不是"论文热度"：先把谱图理论、消息传递、评测规范打牢（这是全部 46 篇的公共前提），再进入同配性 / 深层 GNN、图压缩、可扩展训练、动态图、图基础模型、安全等专题。

---

## 2. 当前起点（2026-09-12 傍晚更新）

已经通过四条复现线接触过的知识：

| 已开线 | 论文 | 已经实际接触的内容 | 暴露出的基础缺口 |
|--------|------|--------------------|------------------|
| GCTD | 40，WSDM 2026，图压缩 | 张量分解的 `tensorly` 用法、K-Means 超点、"合成图训 / 原图测"评测、GCN 在完全图上的过平滑 | CP / Tucker 分解原理；图压缩的标准协议（GCond 系）；过平滑的数学解释 |
| ScaDyG | 43，TNNLS 2026，动态图 | 快照式动态图、MRR / AP 评测、负采样、checkpoint 与早停、二部图排名协议 | 连续时间动态图模型谱系（TGN / TGAT / DyGFormer）；TGB 评测规范；解耦式 GNN（SGC / SIGN） |
| IGNN | 11，NeurIPS 2025，同配/异配 | public / custom split、异配数据集（critical 版）、硬件差异带来的数值漂移；public split 已冻结 | 同配性度量；平滑–泛化理论；异配基准的批评（Platonov 2023） |
| SGPC | 29，AAAI 2026，Sheaf + PAC-Bayes | 官方 `main.py` 审计：标量加权拉普拉斯、test 选模、稠密谱间隙、Sinkhorn 退化为一步 | sheaf 限制映射 vs 实现里的标量权；PAC-Bayes 界哪一项由谱控制；CG 隐式扩散 |

当前主线复现是 SGPC 步骤 7 收尾；队列其余论文已按篇预处理（见 `repro/PREP_STATUS.md`），M0 检验与 IGNN custom 可并行准备、不要并行训练。

---

## 3. 知识模块

每个模块的结构固定：**必须掌握 → 阅读材料 → 论文库对应篇目 → 用来练手的复现 → 检验标准**。
"阅读材料"优先选经典原文与免费教材，不列付费书。论文库篇目用 `papers/.../README.md` 里的编号。

### M0 公共基础：谱图理论 + 消息传递 + 训练评测规范

所有后续模块的前提。与 IGNN custom 收尾、SGPC 审计并行完成。

**必须掌握**

- 邻接矩阵、度矩阵、归一化拉普拉斯 \(L = I - D^{-1/2} A D^{-1/2}\)、特征分解、谱与"频率"的对应
- GCN 一层的推导：为什么是 \(\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2} X W\)，自环和对称归一化各自的作用
- 消息传递框架（MPNN）：message / aggregate / update；GraphSAGE、GAT、GIN 是同一框架下的三种聚合
- 解耦式模型：SGC、APPNP、SIGN——把传播和变换分开，这是 ScaDyG、ScaleGNN 的共同祖先
- 评测规范：public split vs random split；seed 的所有来源；早停与选模指标；样本标准差；多 seed 独立进程
- PyG 与 DGL 的数据结构（`Data` / `DGLGraph`）、`MessagePassing` 基类、稀疏矩阵乘

**阅读材料**

- Hamilton, *Graph Representation Learning*（免费电子书）第 1–5 章
- Kipf & Welling, *Semi-Supervised Classification with GCNs*（ICLR 2017）第 2 节
- Wu et al., *Simplifying GCNs*（SGC，ICML 2019）；Klicpera et al., *APPNP*（ICLR 2019）
- Gilmer et al., *Neural Message Passing for Quantum Chemistry*（ICML 2017）第 2 节
- PyG 官方文档 "Creating Message Passing Networks"
- Platonov et al., *A Critical Look at the Evaluation of GNNs under Heterophily*（ICLR 2023）第 3 节——评测规范的反面教材集

**论文库对应**：11 IGNN（public 已冻结）、33 异配综述第 2 节

**练手复现**：IGNN custom split（Actor / chameleon / squirrel）；手写 GCN / SGC / APPNP。

**检验标准**

- 能手推 2 层 GCN 前向，并解释在完全图上为什么输出趋于常数（GCTD 日志里的 30% 现象）
- 能用 PyG `MessagePassing` 在 30 分钟内写出 GCN / SGC / APPNP 并在 Cora 上到 80% 左右
- 能列出一个训练脚本里的全部随机性来源（至少 6 项）

### M1 同配 / 异配与深层 GNN：过平滑、过挤压、谱滤波

**必须掌握**

- 同配性度量：edge / node / class homophily、adjusted homophily；为什么 chameleon / squirrel 要用 filtered 版本
- 过平滑：Dirichlet 能量随层数指数衰减（Oono & Suzuki 2020）；残差、初始残差、归一化为什么有效
- 过挤压：瓶颈与 Ricci 曲率（Topping et al. 2022；Alon & Yahav 2021）；增大谱间隙的副作用（GBN 的出发点）
- 谱滤波器：ChebNet 的切比雪夫多项式、BernNet 的伯恩斯坦基；高通 / 低通滤波与异配的关系
- 平滑–泛化困境（IGNN 第 3 节）
- Sheaf（层）拉普拉斯：把每条边配一个线性映射，为什么能表达异配（Hansen & Ghrist；Bodnar et al. NSD）
- PAC-Bayes 泛化界的基本形式（McAllester）；最优传输 / Sinkhorn 的基本概念（SGPC 用它学 restriction map）

**阅读材料**

- 33 异配综述（TKDE 2026）全文
- Oono & Suzuki, *Graph Neural Networks Exponentially Lose Expressive Power*（ICLR 2020）
- Topping et al., *Understanding Over-squashing and Bottlenecks via Curvature*（ICLR 2022）
- Defferrard et al., *ChebNet*（NeurIPS 2016）；He et al., *BernNet*（NeurIPS 2021）
- Bodnar et al., *Neural Sheaf Diffusion*（NeurIPS 2022）第 2–3 节
- Alquier, *User-friendly Introduction to PAC-Bayes Bounds* 第 1–2 章
- Peyré & Cuturi, *Computational Optimal Transport* 第 4 章（Sinkhorn）

**论文库对应**：11 IGNN、09 GBN、10 Stable-ChebNet、29 SGPC、34 熵视角过平滑、35 TPAMI 深层 GCN 稳定性

**练手复现**：29 SGPC（进行中）→ 09 GBN → 10 Stable-ChebNet（顺序见 ROADMAP）。

**检验标准**

- 给一个数据集能算出三种同配性并预测 GCN / MLP 谁更强
- 能解释 IGNN 的 `n_hops`、`IN`、`RN` 开关分别对应论文哪一节
- 能画出 ChebNet 与 BernNet 在 \([0,2]\) 上的滤波响应曲线
- 能说清 SGPC 的 PAC-Bayes 界里哪一项由 sheaf 的谱控制

### M2 图压缩与持续学习

**必须掌握**

- 数据集蒸馏 → 图压缩的谱系：GCond（梯度匹配）、DosCond（一步）、SFGC（轨迹匹配）、结构无关压缩
- 图压缩的标准协议：在合成图上训练、在原图 val/test 上评测；压缩比、跨架构泛化、效率
- CP / Tucker 分解、非负约束、初始化与学习率对塌缩的影响（GCTD 遇到的全部问题）
- 持续图学习：任务增量 / 类增量、灾难性遗忘、经验回放、压缩图作记忆库（PUMA）

**阅读材料**

- 32 图压缩综述（TKDE 2025）第 2、3、5 节
- Jin et al., *Graph Condensation for GNNs*（GCond，ICLR 2022）
- Zheng et al., *Structure-free Graph Condensation*（SFGC，NeurIPS 2023）
- Kolda & Bader, *Tensor Decompositions and Applications*（SIAM Review 2009）第 3、4 节
- GraphSlim 或 GC-Bench 的 README 与协议说明

**论文库对应**：40 GCTD（已做）、32 综述、31 PUMA

**练手复现**：GCTD 收尾（Citeseer / Pubmed + GCond 对照）→ 31 PUMA。

**检验标准**

- 能用 GraphSlim 跑出 GCond 在 Cora 1.3% 的公认数字，并说明与我们 GCTD 评测代码的差异
- 能解释 GCTD 的 `lr_rec`、`edge_thresh` 为什么会决定合成图是不是完全图
- 能画出 PUMA 的记忆库更新流程图

### M3 可扩展 GNN 与 OGB 协议

**必须掌握**

- 邻居爆炸问题；采样式（GraphSAGE、ClusterGCN、GraphSAINT）与解耦式（SGC、SIGN、PPRGo）两条路线
- 高阶邻居的贡献与过平滑的权衡（ScaleGNN 的 Local Contribution Score）
- OGB 节点分类协议：固定 split、`Evaluator`、ogbn-arxiv / products / papers100M 的规模差异
- 内存与 IO：特征矩阵 memmap、稀疏矩阵格式（CSR / COO）、SpMM

**阅读材料**

- Hamilton et al., *GraphSAGE*（NeurIPS 2017）；Chiang et al., *Cluster-GCN*（KDD 2019）；Zeng et al., *GraphSAINT*（ICLR 2020）
- Frasca et al., *SIGN*（arXiv 2020）；Bojchevski et al., *PPRGo*（KDD 2020）
- Hu et al., *Open Graph Benchmark*（NeurIPS 2020）第 3、4 节
- 16 IO-aware（ICML 2026）第 2、3 节——即使不复现，也要知道瓶颈在哪

**论文库对应**：15 ScaleGNN、16 IO-aware、43 ScaDyG（预传播思想）

**练手复现**：15 ScaleGNN（ogbn-arxiv）。

**检验标准**

- 能在 ogbn-arxiv 上用 SIGN 风格预传播写一个 baseline 到 70% 左右
- 能估算 papers100M 的特征矩阵占多少内存并说明为什么要 memmap

### M4 动态图学习

**必须掌握**

- 离散快照 vs 连续时间事件流；EvolveGCN / ROLAND vs TGN / TGAT / DyGFormer
- 时间编码（Bochner 特征、指数时间编码）；记忆模块
- 动态链接预测评测：TGB 协议（逐正边、历史负样本 + 随机负样本、MRR）；与"每源取最佳正边 + 全节点负采样"的区别
- 二部图上的合法候选集与负采样
- Hypernetwork 的基本形式

**阅读材料**

- Rossi et al., *TGN*（ICML 2020 GRL+ Workshop）；Yu et al., *DyGFormer*（NeurIPS 2023）
- Huang et al., *Temporal Graph Benchmark*（NeurIPS 2023 D&B）第 3 节 + `py-tgb` 的 `Evaluator` 源码
- Ha et al., *HyperNetworks*（ICLR 2017）引言

**论文库对应**：43 ScaDyG（已做）

**练手复现**：ScaDyG 收尾（消融、BitcoinAlpha）。

**检验标准**

- 能说清 ScaDyG 三个组件分别对应代码哪个类
- 能用 TGB 的 `Evaluator` 重评我们保存的 `best_*.pt`，并解释与 filtered MRR 的差异

### M5 链接预测、表达力与图级任务

**必须掌握**

- WL 测试与 GIN；为什么单节点嵌入聚合刻画不了多节点关系（labeling trick 的出发点）
- SEAL、DRNL 标注；Hits@K / MRR 评测
- 图级任务：readout / pooling、虚拟节点、LRGB 长程基准（Peptides-func / struct）
- 等变 / 不变性；k-WL 与高阶 GNN（46 的背景）

**阅读材料**

- Xu et al., *How Powerful are GNNs*（GIN，ICLR 2019）
- Zhang & Chen, *Link Prediction Based on Graph Neural Networks*（SEAL，NeurIPS 2018）
- Dwivedi et al., *Long Range Graph Benchmark*（NeurIPS 2022 D&B）
- 44 Labeling Trick（JMLR 2025）第 1–4 节

**论文库对应**：44 Labeling Trick、13 MAVN、10 Stable-ChebNet（LRGB 部分）、46 正交等变基

**练手复现**：44 Labeling Trick（LinkPred 子仓库）→ 13 MAVN。

**检验标准**

- 能在 Cora 链接预测上用 SEAL 达到 Hits@100 90% 左右
- 能解释 Peptides-func 上为什么 MPNN 需要虚拟节点或谱方法

### M6 图基础模型与公平评测

**必须掌握**

- 跨图迁移的三个障碍：特征维度、标签空间、图规模；对应的解决路线（等变配方、KG 预训练、PFN、in-context）
- Prior-Data Fitted Networks（TabPFN）原理：在合成先验上预训练、推理时 in-context
- 公平评测：为什么多数 GFM 打不过调好的 GNN（08 的结论）
- 置换等变 / 特征置换不变（01 的 Triple-Symmetry）

**阅读材料**

- 08 FairEval（ICML 2026 Workshop）全文——作为本模块的"评测教科书"
- Hollmann et al., *TabPFN*（ICLR 2023）第 2、3 节
- 01 EquivarianceEverywhere 第 3 节；03 GraphPFN 第 3 节

**论文库对应**：01、02、03、04、05、07、08

**练手复现**：08 FairEval（评测框架）→ 01 EquivarianceEverywhere 或 04 MF-GIA（单卡可跟）。03 GraphPFN 只做微调 / ICL 评测，不做预训练。

**检验标准**

- 能把 IGNN 作为一个 baseline 接进 08 的评测框架
- 能解释 GraphPFN 的合成先验用了哪三种生成机制

### M7 MoE、鲁棒与安全

**必须掌握**

- MoE 路由与负载均衡；路由在分布偏移下的脆弱性（STEM-GNN 的风险分解）
- 模型窃取 / 模型提取攻击与防御；成员推断；图遗忘与遗忘反演
- Lipschitz 正则、向量量化 token

**阅读材料**

- Shazeer et al., *Outrageously Large Neural Networks*（MoE，ICLR 2017）第 2 节
- 23 GraphRP 第 3 节；41 遗忘反演第 3 节

**论文库对应**：12 STEM-GNN、23 GraphRP、41 Unlearning Inversion

**练手复现**：23 GraphRP 或 41（二选一，都是标准小图）→ 12 STEM-GNN。

### M8 GraphRAG 与 LLM 交叉（受 API 条件限制）

**必须掌握**

- GraphRAG 基本流水线：抽三元组 → 建图 → 社区 / 层次 → 检索 → 生成
- k-core 分解与社区发现的可复现性问题（22 的核心论点）
- RL for LLM（GRPO）的基本形式，只需理解奖励设计

**阅读材料**

- 22 Core GraphRAG 第 3、4 节；Microsoft GraphRAG 技术报告
- Batagelj & Zaveršnik, *An O(m) Algorithm for Cores Decomposition*

**论文库对应**：18、19、20、21、22、30、42

**练手复现**：22 Core GraphRAG 的**算法部分**（k-core 层次、确定性验证）；LLM 评测部分等有 API 预算再做。

### M9（可选）系统与并行

单卡机器无法复现，只读不做。目的是写 related work 和理解瓶颈。

**阅读材料**：14 Plexus、36 NeutronTP、37 NeutronTask、38 NeutronCloud、39 Hyperion 各读引言 + 系统设计一节；16 IO-aware 的 kernel 分类。

**检验标准**：能画一张"全图训练 vs mini-batch、切图 vs 切特征 vs 任务并行、内存 vs SSD"的对照表。

---

## 4. 阶段时间线

假设每周 5 个工作日、单卡 RTX 3090。每篇论文复现按 1–2 周预算，超时按 ROADMAP 的冻结规则处理。

| 阶段 | 时间 | 复现内容（详见 ROADMAP） | 同步学习模块 | 阶段产出 |
|------|------|--------------------------|--------------|----------|
| P0 收尾 + 打底 | 第 1–3 周 | IGNN public 已冻结，custom 待跑；ScaDyG 消融 + 报告；GCTD 收口冻结；**SGPC 步骤 1–7** | M0 全部；M1 随 SGPC 启动；M4 补 TGB；M2 补张量分解 | IGNN public 冻结表；SGPC 官方原样数字；ScaDyG/GCTD 收口；M0 检验通过；`results/SUMMARY.md` |
| P1 同配 / 深层 GNN | 第 4–9 周 | 29 SGPC 收尾冻结 → 09 GBN → 10 Stable-ChebNet | M1 全部；M5 的 LRGB 部分 | 三份 `*_REPRO_LOG.md`；一份"异配 GNN 方法对照笔记" |
| P2 压缩 + 可扩展 | 第 10–15 周 | 31 PUMA → 15 ScaleGNN | M2、M3 | 图压缩基线表（GCond / GCTD / PUMA 同协议）；ogbn-arxiv 基线 |
| P3 链接预测 + 图级 | 第 16–19 周 | 44 Labeling Trick → 13 MAVN | M5 | 链接预测评测笔记 |
| P4 图基础模型 | 第 20–25 周 | 08 FairEval → 01 或 04 | M6 | 把 IGNN / SGPC 接入 08 框架的对比表 |
| P5 安全 / MoE | 第 26–29 周 | 23 或 41 → 12 STEM-GNN | M7 | 攻防对照笔记 |
| P6 GraphRAG 算法侧 | 第 30–32 周 | 22 Core GraphRAG 算法部分 | M8 | k-core 层次可复现性验证 |
| 贯穿 | — | — | M9 只读 | 系统对照表 |

阶段边界可以按实际进度前后移动，但**不要并行开两篇新论文**：GPU 只有一张，注意力也只有一份。SGPC 已开，在它冻结前不要启动 GBN。IGNN custom / ScaDyG / GCTD 是收尾，不算新开。

---

## 5. 每周节奏

固定的"读 / 做 / 写"循环，比例约 30 / 50 / 20：

| 时段 | 内容 |
|------|------|
| 周一 | 精读本周论文的方法与实验节（2–3 小时）；对照代码找"论文写的 vs 代码做的"差异；写读书笔记初稿 |
| 周二–周四 | 复现推进（按 ROADMAP 标准流程的当前步骤）；每天补 1–1.5 小时当前模块的基础材料 |
| 周五 | 整理日志、更新结果表；回答第 6 节自检问题；决定下周是继续、冻结还是换题 |

GPU 长任务放晚上或周末，白天用于读代码和写笔记。

---

## 6. 笔记与自检

### 6.1 读书笔记模板

放 `paper/notes/<编号>_<简称>.md`，每篇论文一份，复现开始前写初稿、冻结时定稿：

```markdown
# <编号> <论文简称>（<会议 年份>）

## 一句话
研究什么问题、提出什么、主要数字。

## 方法拆解
- 组件 1：… → 代码位置 …
- 组件 2：… → 代码位置 …

## 实验协议
数据集 / split / 指标 / seed 数 / 选模指标 / 早停 / 硬件。

## 论文写的 vs 代码做的
| 项 | 论文 | 代码 | 影响 |

## 依赖的基础知识（对应 LEARNING_PLAN 模块）
- M?：…

## 复现结论（冻结时填写）
L1 / L2 / L3 各是否达到；剩余假设。

## 可以延伸的点
```

### 6.2 每周自检

1. 本周复现的数字和论文差多少？属于"超参未公开 / 代码 bug / 硬件与环境"哪一类？
2. 我改了哪些官方代码？每一处能说出"为什么必须改"以及"论文文字支持哪一种"吗？
3. 本周新增的随机性来源有没有写进日志？
4. 当前模块的"检验标准"我能通过几条？没通过的下周怎么补？
5. 如果作者问"你确定不是你环境的问题"，我能拿出哪个对照实验回答？

### 6.3 阶段结束时

- 当前模块检验标准全部通过，或写明哪条未通过与原因
- 每篇复现论文有 `repro/<NAME>_REPRO_LOG.md` 冻结条目 + `paper/notes/` 定稿
- `results/SUMMARY.md` 更新
- 用一页纸写"这个阶段学到的最重要的三件事"，放 `paper/notes/phase_<n>_review.md`
