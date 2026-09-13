# 图神经网络前沿论文集（2025–2026）

本目录收集与**图神经网络（GNN）**、**图基础模型（Graph Foundation Models）**、**大规模图学习 / 大数据处理**、**数据挖掘**以及 **GraphRAG / LLM+图** 相关的最新顶会、CCF 期刊与前沿预印本论文。检索日期为 **2026-09-09**（CVPR / CCF 条目于同日补全；**SIGMOD / VLDB / ICDE / WSDM / TNNLS / JMLR** 于同日第二轮补全）。

本地 PDF 现为 **46 篇**，约 **117 MB**。

### 为何第一版没有单独列出 CVPR 与 CCF 期刊？

第一版按**方法主战场**筛选：GNN 理论、图基础模型、大规模训练、数据挖掘系统，优先取 NeurIPS / ICML / ICLR / KDD / WWW。这造成两处遗漏：

1. **CVPR 是 CCF-A，但属于计算机视觉。** 其上的图工作多为场景图（Scene Graph）、3D 功能图、点云图 Transformer，而不是通用 GNN 理论。对“图学习方法”主线不是第一优先级，但对视觉图挖掘、具身智能仍重要。
2. **CCF 不是一套独立会议，而是对已有期刊/会议的分级。** 第一版其实已经包含大量 CCF-A 会议（NeurIPS、ICML、KDD、WWW、ACL、SC），只是没有按 CCF 目录标注；漏掉的是 **CVPR、AAAI、IJCAI、SIGIR** 以及 **TPAMI / TKDE** 等期刊。另外，期刊审稿周期长，2026 年“最新”方法往往先出现在会议上，期刊更多是理论深化与综述。

**说明：** ICLR 在现行 CCF 目录中为 **B 类**；TNNLS 为 **B 类**。IJCAI 2026 正式论文集 PDF 检索时尚未开放，故先收入已公开的 **IJCAI 2025** CCF-A 论文。

---

## 1. 数据来源与检索入口

| 来源 | 说明 | 网址 |
|------|------|------|
| arXiv | 开放预印本，本目录 PDF 主要从此下载 | https://arxiv.org |
| NeurIPS 2025 Proceedings | 图学习、图基础模型正式论文 | https://proceedings.neurips.cc/paper_files/paper/2025 |
| ICML 2026 | GraphPFN、IO-aware GNN kernels | https://icml.cc/virtual/2026 |
| ICLR 2026 | 图 in-context / 跨域对齐 | https://iclr.cc/virtual/2026 |
| KDD 2026 | 数据挖掘、图挖掘、GraphRAG、GNN 安全 | https://kdd.org |
| WWW 2026（The Web Conference） | 大规模 GNN、GraphRAG | https://www2026.thewebconf.org |
| SC 2025 | 超算上的十亿边图训练系统 | https://sc25.supercomputing.org |
| ACL 2026 Findings | 文本属性图基础模型 | https://aclanthology.org |
| ACM Digital Library | KDD / WWW / SC 正式 DOI 页面 | https://dl.acm.org |
| OpenReview | ICLR / NeurIPS / ICML 审稿与终稿 | https://openreview.net |
| CVPR Open Access | CVPR 2026 视觉图 / 场景图开放论文 | https://openaccess.thecvf.com/menu |
| AAAI Proceedings | AAAI-26 超图 / Sheaf GNN | https://ojs.aaai.org |
| IJCAI Proceedings | IJCAI 正式论文（2026 集检索时未上线） | https://www.ijcai.org/proceedings |
| IEEE Xplore / 作者 arXiv | TPAMI、TKDE、TNNLS 等 CCF 期刊 | https://ieeexplore.ieee.org |
| PVLDB / VLDB | 数据库系统上的大规模 GNN 训练 | https://www.vldb.org/pvldb |
| ICDE / 作者主页 | 核外 / SSD 图训练系统 | https://ieeexplore.ieee.org |
| WSDM Proceedings | Web 搜索与数据挖掘（CCF-B） | https://wsdm-conference.org |
| JMLR | 开放获取机器学习期刊（CCF-A） | https://jmlr.org |
| CCF 推荐目录 | 中国计算机学会期刊会议分级 | https://www.ccf.org.cn/Academic_Evaluation/By_category |

**检索关键词（示例）**：`graph foundation model`、`graph neural network`、`oversmoothing oversquashing`、`scalable GNN billion-edge`、`GraphRAG reinforcement learning`、`model extraction GNN`、`scene graph generation CVPR`、`heterophily TKDE`。

**版权说明**：本目录保存的是作者在 arXiv / ACL Anthology / 会议开放页面上公开的 PDF，仅供个人学习与科研使用。正式引用请以会议/期刊最终版本与 DOI 为准。

---

## 2. 目录结构

```
papers/gnn-frontier-2025-2026/
├── README.md                          # 本说明文档
├── papers_index.csv                   # 一览表（便于筛选）
├── 01-graph-foundation-models/        # 图基础模型、跨图迁移、评测
├── 02-gnn-architecture-theory/        # 架构、同配性、长程依赖、专家混合
├── 03-scalable-bigdata-gnn/           # 大规模 / 分布式 / GPU 内核
├── 04-graphrag-llm/                   # GraphRAG、检索增强、智能体
├── 05-data-mining-security/           # 图挖掘场景下的模型窃取防御
├── 06-cvpr-vision-graph/              # CVPR 场景图 / 3D 功能图 / 形态图
├── 07-ccf-aaai-ijcai-sigir/           # AAAI / IJCAI / SIGIR（CCF-A）
├── 08-ccf-journals/                   # TPAMI / TKDE（CCF-A 期刊）
├── 09-db-systems-sigmod-vldb-icde/    # VLDB / ICDE 大规模 GNN 系统
├── 10-wsdm/                           # WSDM 图压缩 / 安全 / AutoGNN
└── 11-journals-tnnls-jmlr/            # TNNLS（CCF-B）/ JMLR（CCF-A）
```

### CCF 分级对照（本目录已收录）

| CCF | 类型 | 本目录中的venue | 论文编号 |
|-----|------|-----------------|----------|
| A | 会议 | NeurIPS | 01, 02, 09, 10, 11 |
| A | 会议 | ICML | 03, 16 |
| A | 会议 | KDD | 12, 13, 20, 22, 23 |
| A | 会议 | WWW | 15, 18 |
| A | 会议 | ACL | 05 |
| A | 会议 | SC | 14 |
| A | 会议 | **CVPR** | 24, 25, 26 |
| A | 会议 | **AAAI** | 27, 28, 29 |
| A | 会议 | **IJCAI** | 34（2025；2026 论文集尚未公开 PDF） |
| A | 会议 | **SIGIR** | 30 |
| A | 期刊 | **IEEE TPAMI** | 35 |
| A | 期刊 | **IEEE TKDE** | 31, 32, 33 |
| A | 会议 | **VLDB / PVLDB** | 36, 37, 38 |
| A | 会议 | **ICDE** | 39 |
| A | 期刊 | **JMLR** | 44, 45, 46 |
| B | 会议 | ICLR | 04 |
| B | 会议 | **WSDM** | 40, 41, 42 |
| B | 期刊 | **IEEE TNNLS** | 43 |
| — | 预印本/Workshop | arXiv / ICML Workshop | 06, 07, 08, 17, 19, 21 |

**SIGMOD（CCF-A）说明：** 近年 SIGMOD 研究论文先发在 *Proceedings of the ACM on Management of Data*（PACMMOD）。东北大学 iDC 组的 **NeutronHeter**（PACMMOD 3(4), Article 257, 2025；DOI [10.1145/3749175](https://doi.org/10.1145/3749175)，作者页标注 SIGMOD 2026）针对异构集群分布式 GNN，ACM 付费墙下本次未能保存开放 PDF。同组已开放的 VLDB 系统论文见 36–38。

---

## 3. 可研究性与可复现性评级标准

**可研究性**（对后续选题的价值）

- **很高**：正在形成新范式，空白多，适合作为主线课题
- **高**：方法明确、可改进点清楚，适合跟进实验或理论
- **中**：工程或评测价值大，创新空间相对收敛

**可复现性**

- **高**：公开代码 + 公开数据 + 超参较完整
- **中**：有代码或补充材料，但数据/算力门槛较高
- **低**：工业数据或十亿参数规模，外部难以完整复现

---

## 4. 论文详细说明

### A. 图基础模型（`01-graph-foundation-models/`）

#### 01. Equivariance Everywhere All At Once: A Recipe for Graph Foundation Models

| 项目 | 内容 |
|------|------|
| 本地文件 | `01-graph-foundation-models/01_EquivarianceEverywhere_NeurIPS2025.pdf` |
| 会议 | **NeurIPS 2025** |
| 作者 | Ben Finkelshtein, İsmail İlkan Ceylan, Michael Bronstein, Ron Levie 等 |
| arXiv | https://arxiv.org/abs/2506.14291 |
| 会议 PDF | https://proceedings.neurips.cc/paper_files/paper/2025/file/2b89783b68cdcfa7c8d7b08c09f47b2a-Paper-Conference.pdf |
| 开源代码 | **有** — https://github.com/benfinkelshtein/EquivarianceEverywhere |
| 研究目的 | 从对称性第一性原理给出节点级图基础模型配方：提出对节点/标签置换等变、对特征置换不变的 Triple-Symmetry Network（TSNet），并证明其在多重集上的万能逼近性；该配方可与任意 GNN 聚合结合，实现跨图规模、跨特征维、跨标签空间的迁移。 |
| 可研究性 | **很高**。图基础模型的“共享词汇表 / 跨通道对齐”仍是开放问题；可沿等变性、标签通道消息传递、回归任务扩展、与 PFN 类方法对比继续做。 |
| 可复现性 | **高**。官方仓库完整，实验在单卡 L40 上完成，数据集为公开节点分类基准。 |

#### 02. Towards Graph Foundation Models: Training on Knowledge Graphs Enables Transferability to General Graphs（SCR）

| 项目 | 内容 |
|------|------|
| 本地文件 | `01-graph-foundation-models/02_SCR_KG_GraphFoundation_NeurIPS2025.pdf` |
| 会议 | **NeurIPS 2025** |
| 作者 | Kai Wang, Siqiang Luo, Caihua Shan, Yifei Shen（NTU / Microsoft Research Asia） |
| arXiv | https://arxiv.org/abs/2410.12609 |
| 会议 PDF | https://proceedings.neurips.cc/paper_files/paper/2025/file/de04896f011beff76c91e094f72727f4-Paper-Conference.pdf |
| 开源代码 | **有** — 会议版给出 https://github.com/KyneWang/SCR ；arXiv 版说明实现基于 ULTRA（https://github.com/DeepGraphLearning/ULTRA） |
| 研究目的 | 将知识图谱的零样本归纳推理作为图基础模型预训练目标。设计任务专用 KG 结构统一节点/边/图级任务，提出 Semantic Conditioned Reasoner（SCR）与语义条件消息传递，缓解传统 KG 推理的语义隔离，并在 38 个跨域数据集上验证迁移。 |
| 可研究性 | **很高**。把 KG 推理当预训练是较新路线，可研究更好的任务统一图构造、语义编码器、以及与 GraphRAG / 多模态图的结合。 |
| 可复现性 | **中高**。代码与公开 KG/图数据集可用；跨 38 数据集的完整复现工作量较大。 |

#### 03. GraphPFN: A Prior-Data Fitted Graph Foundation Model

| 项目 | 内容 |
|------|------|
| 本地文件 | `01-graph-foundation-models/03_GraphPFN_ICML2026.pdf` |
| 会议 | **ICML 2026** |
| 作者 | Dmitry Eremeev, Oleg Platonov, Gleb Bazhenov, Artem Babenko, Liudmila Prokhorenkova（Yandex Research） |
| arXiv | https://arxiv.org/abs/2509.21489 |
| 开源代码 | **有** — https://github.com/yandex-research/graphpfn |
| 研究目的 | 把表格领域成功的 Prior-Data Fitted Networks（PFN / TabPFN）范式引入图。设计多层随机块模型 + 优先连接 + 图感知因果模型的合成图先验，在 LimiX 上增加邻域注意力聚合，于百万级合成图上预训练，使节点级任务支持 in-context learning 与微调。 |
| 可研究性 | **很高**。2026 年 GFM 评测显示 PFN 路线目前最强之一；先验设计、图级任务扩展、推理成本、与真实图分布对齐都是可做课题。 |
| 可复现性 | **中**。代码公开，但预训练规模大、依赖合成数据生成与较强算力；微调/ICL 评测相对可跟。 |

#### 04. Modality-Free Graph In-context Alignment（MF-GIA）

| 项目 | 内容 |
|------|------|
| 本地文件 | `01-graph-foundation-models/04_MF-GIA_ICLR2026.pdf` |
| 会议 | **ICLR 2026** |
| 作者 | Wei Zhuo, Siqiang Luo |
| arXiv | https://arxiv.org/abs/2603.13434 |
| OpenReview | https://openreview.net/forum?id=cDc95lucVL |
| 开源代码 | **有** — https://github.com/JhuoW/MF-GIA |
| 研究目的 | 现有 GFM 常依赖模态专用编码器，跨域对齐失败。MF-GIA 用梯度指纹刻画域特性，以 Dual Prompt-Aware Attention 做无参数更新的 in-context 对齐，追求跨异构图域的少样本节点/边预测。 |
| 可研究性 | **高**。图上真正的 in-context learning 仍不成熟；可研究指纹稳定性、提示构造、未见域泛化。 |
| 可复现性 | **高**。官方仓库含环境与评测脚本，基准多为公开图数据。 |

#### 05. AnyGraph: Graph Foundation Model in the Wild

| 项目 | 内容 |
|------|------|
| 本地文件 | `01-graph-foundation-models/05_AnyGraph_ACL2026.pdf` |
| 会议 | **ACL 2026 Findings** |
| 作者 | Lianghao Xia, Chao Huang 等（HKUDS） |
| 正式 PDF | https://aclanthology.org/2026.findings-acl.44.pdf |
| 开源代码 | **有** — https://github.com/HKUDS/AnyGraph |
| 研究目的 | 面向文本属性图的统一基础模型，用 Graph Mixture-of-Experts 同时处理结构异构、文本特征异构与快速适应，强调零样本跨域与 scaling law。在 38 个数据集上验证。 |
| 可研究性 | **高**。文本图 + MoE 路由是数据挖掘/推荐/社交网络中的实用方向；可改进专家路由、灾难性遗忘与域发现。 |
| 可复现性 | **中高**。代码开源；38 数据集与预训练成本不低，但公开基准可部分复现。 |

#### 06. Billion-Scale Graph Foundation Models（GraphBFF）

| 项目 | 内容 |
|------|------|
| 本地文件 | `01-graph-foundation-models/06_GraphBFF_BillionScale_arXiv.pdf` |
| 状态 | **arXiv 预印本（Meta，2026）**，工业级规模工作 |
| 作者 | Maya Bechler-Speicher, Yoel Gottlieb, Andrey Isakov 等（Meta） |
| arXiv | https://arxiv.org/abs/2602.04768 |
| 开源代码 | **未见公开仓库**（论文未给出 GitHub） |
| 研究目的 | 给出十亿参数异构图基础模型的端到端配方（GraphBFF Transformer）：类型条件/类型无关注意力、批处理、预训练与微调，并报告异构图上的神经缩放律。在未见过的十项下游任务上，冻结主干 + 探测头最高可提升约 31 PRAUC。 |
| 可研究性 | **很高（方向）/ 中（跟实验）**。缩放律与工业异构图 GFM 是前沿空白；但数据为内部企业图，外部难以原样复现，更适合借鉴架构思想做公开大规模图实验。 |
| 可复现性 | **低**。无公开代码与十亿规模公开异构图；可作为系统设计文献阅读。 |

#### 07. A Graph Foundation Model with Spectral Parsing and Prototype-Guided Spatial Propagation（SPG）

| 项目 | 内容 |
|------|------|
| 本地文件 | `01-graph-foundation-models/07_SPG_SpectralParsing_arXiv.pdf` |
| 状态 | **arXiv:2606.03315（2026-06）**，投稿补充材料含代码 |
| 作者 | Ankang Yang, Jitao Zhao, Dongxiao He, Di Jin（天津大学） |
| arXiv | https://arxiv.org/abs/2606.03315 |
| 开源代码 | **论文声明随投稿提供补充代码，检索时未见独立公开 GitHub** |
| 研究目的 | 用可学习 Chebyshev 谱滤波把节点特征分解为多频响应，再用 Gromov–Wasserstein 原型几何蒸馏跨图可迁移的成对结构，并将原型核投影回各图指导传播，门控融合局部邻接、热核扩散与原型传播。 |
| 可研究性 | **高**。谱域解析 + 最优传输原型是较新的跨图迁移组合，适合做理论（对齐稳定性）与少样本迁移实验。 |
| 可复现性 | **中**。数据集公开（Cora、OGB 等），但官方仓库未独立发布时需自行按论文实现。 |

#### 08. A Fair Evaluation of Graph Foundation Models for Node Property Prediction

| 项目 | 内容 |
|------|------|
| 本地文件 | `01-graph-foundation-models/08_FairEval_GFM_ICML2026Workshop.pdf` |
| 会议 | **ICML 2026 Workshop on Graph Foundation Models** |
| 作者 | Oleg Platonov, Gleb Bazhenov, Dmitry Eremeev, Liudmila Prokhorenkova |
| arXiv | https://arxiv.org/abs/2606.24509 |
| 开源代码 | **有** — https://github.com/yandex-research/gnn-fair-evaluation |
| 研究目的 | 指出当前 GFM 评测数据集窄、基线弱、设定不统一。在统一协议下重评 9 个近期 GFM，发现多数无法稳定超过调好的 GNN，仅 PFN 路线（GraphPFN / G2T-FM / TAG）表现突出。 |
| 可研究性 | **很高（作为起点）**。做 GFM 必读；可直接沿其协议加入新模型，或研究“为何非 PFN 的 GFM 失败”。 |
| 可复现性 | **高**。评测代码与各模型官方实现链接齐全。 |

---

### B. GNN 架构与理论（`02-gnn-architecture-theory/`）

#### 09. Deeper with Riemannian Geometry: Overcoming Oversmoothing and Oversquashing for Graph Foundation Models（GBN）

| 项目 | 内容 |
|------|------|
| 本地文件 | `02-gnn-architecture-theory/09_Riemannian_GBN_NeurIPS2025.pdf` |
| 会议 | **NeurIPS 2025** |
| 作者 | ZhenhHuang 等 |
| arXiv | https://arxiv.org/abs/2510.17457 |
| 会议 PDF | https://proceedings.neurips.cc/paper_files/paper/2025/file/e4e5d01075906f9d8522911a736aa5d9-Paper-Conference.pdf |
| 开源代码 | **有** — https://github.com/ZhenhHuang/GBN |
| 研究目的 | 证明用增大谱间隙缓解 oversquashing 会导致对输入特征的梯度消失。将局部黎曼几何与 MPNN 联系，建立非齐次 Robin 边界条件，提出 Graph Boundary-conditioned Network（GBN），在保留原图结构下局部调节瓶颈。同配/异配图上有效，深度超过 256 层仍不崩溃。 |
| 可研究性 | **很高**。oversmoothing / oversquashing 是 GNN 经典开放问题；局部几何条件可扩展到动态图、异配图与更深 GFM 骨干。 |
| 可复现性 | **高**。代码公开，数据集为 WikiCS、Texas 等常用基准。 |

#### 10. Return of ChebNet: Understanding and Improving an Overlooked GNN on Long-Range Tasks（Stable-ChebNet）

| 项目 | 内容 |
|------|------|
| 本地文件 | `02-gnn-architecture-theory/10_Stable-ChebNet_NeurIPS2025.pdf` |
| 会议 | **NeurIPS 2025 Spotlight** |
| 作者 | Ali Hariri, Álvaro Arroyo, Alessio Gravina 等（EPFL / Oxford / Pisa / Cambridge / NVIDIA） |
| arXiv | https://arxiv.org/abs/2506.07624 |
| 会议 PDF | https://proceedings.neurips.cc/paper_files/paper/2025/file/c6de943558fe0b1bf4ea8f09fbcede44-Paper-Conference.pdf |
| 开源代码 | **有** — https://github.com/ahariri13/Stable-ChebNet |
| 研究目的 | 重新审视被忽视的谱方法 ChebNet，分析其在长程任务上的不足，提出加入 Euler 步的 Stable-ChebNet。在 LRGB（Peptides 等）上缩小甚至超过 Graph Transformer / Graph Mamba，且无需拉普拉斯位置编码。 |
| 可研究性 | **高**。说明“经典谱 GNN + 数值稳定化”仍能打长程任务；可研究更高阶稳定性、与重连边/SSM 的结合。 |
| 可复现性 | **高**。仓库含 Peptides、OGB、GraphProp 脚本。 |

#### 11. Making Classic GNNs Strong Baselines Across Varying Homophily（IGNN）

| 项目 | 内容 |
|------|------|
| 本地文件 | `02-gnn-architecture-theory/11_IGNN_Homophily_NeurIPS2025.pdf` |
| 会议 | **NeurIPS 2025** |
| 作者 | Ming Gu, Zhuonan Zheng, Sheng Zhou, Jiawei Chen, Qiaoyu Tan, Jiajun Bu 等 |
| arXiv | https://arxiv.org/abs/2412.09805 |
| 会议 PDF | https://proceedings.neurips.cc/paper_files/paper/2025/file/4913941ed905b81b47d642e05494e648-Paper-Conference.pdf |
| OpenReview | https://openreview.net/forum?id=IAGbhDARZd |
| 开源代码 | **有** — https://github.com/galogm/IGNN |
| 研究目的 | 指出同配 GNN 在仔细调参后跨同配性也能表现良好，但缺乏理论。提出 smoothness–generalization 困境：跳数增加提升平滑却损害泛化。据此设计 Inceptive GNN（分离变换、分跳聚合、邻域关系学习），对 30 个基线全面评测。 |
| 可研究性 | **很高**。同配/异配是数据挖掘图分类的长期主题；该文同时提供强基线与理论切口，适合做新架构或更公平的评测协议。 |
| 可复现性 | **高**。含 30 个基线实现、统一划分与搜参脚本。 |

#### 12. Generalizing GNNs with Tokenized Mixture of Experts（STEM-GNN）

| 项目 | 内容 |
|------|------|
| 本地文件 | `02-gnn-architecture-theory/12_STEM-GNN_KDD2026.pdf` |
| 会议 | **KDD 2026** |
| 作者 | Xiaoguang Guo, Zehong Wang, Jiazheng Li 等 |
| arXiv | https://arxiv.org/abs/2602.09258 |
| DOI | https://doi.org/10.1145/3770855.3817952 |
| 开源代码 | **有** — https://github.com/GXG-CS/STEM-GNN |
| 研究目的 | 分析 MoE 路由在分布偏移与扰动下的脆弱性，提出风险分解；设计 STEM-GNN：多样专家编码器 + 向量量化 token 接口吸收表示漂移 + Lipschitz 正则预测头。面向节点/边/图任务的稳健泛化。 |
| 可研究性 | **高**。GNN+MoE 在跨域数据挖掘中很实用；可研究更好的路由正则、token 码本与对抗鲁棒。 |
| 可复现性 | **高**。代码与数据在仓库中公开。 |

#### 13. Learn When and Where to Connect: Adaptive Virtual Nodes for Dynamic Message Passing（MAVN）

| 项目 | 内容 |
|------|------|
| 本地文件 | `02-gnn-architecture-theory/13_MAVN_KDD2026.pdf` |
| 会议 | **KDD 2026** |
| 作者 | Jaejun Lee, Joyce Jiyoung Whang（KAIST） |
| arXiv | https://arxiv.org/abs/2606.03068 |
| DOI | https://doi.org/10.1145/3770855.3818013 |
| 开源代码 | **有** — https://github.com/bdi-lab/MAVN ；Zenodo：https://doi.org/10.5281/zenodo.20446608 |
| 研究目的 | 现有 Virtual Node 方法连接数固定、预先连边。MAVN 可端到端、可微地按层动态引入虚拟节点，并用双向打分决定节点–VN 连接。理论证明可模拟任意节点–VN 连接模式。 |
| 可研究性 | **高**。虚拟节点是缓解 oversquashing 的轻量手段；可研究大规模图上的 VN 预算、动态图与异配图。 |
| 可复现性 | **高**。GitHub + Zenodo 双备份。 |

---

### C. 大规模 / 大数据 GNN（`03-scalable-bigdata-gnn/`）

#### 14. Plexus: Taming Billion-edge Graphs with 3D Parallel Full-graph GNN Training

| 项目 | 内容 |
|------|------|
| 本地文件 | `03-scalable-bigdata-gnn/14_Plexus_SC2025.pdf` |
| 会议 | **SC 2025**（国际超算顶会） |
| 作者 | Aditya K. Ranjan, Siddharth Singh, Cunyang Wei, Abhinav Bhatele（University of Maryland） |
| arXiv | https://arxiv.org/abs/2505.04083 |
| DOI | https://doi.org/10.1145/3712285.3759890 |
| 作者主页 PDF | https://pssg.cs.umd.edu/assets/papers/2025-11-plexus-sc.pdf |
| 开源代码 | **有** — https://github.com/hpcgroup/plexus |
| 研究目的 | 针对全图训练的通信开销与负载不均，提出 3D 并行 + 双置换负载均衡 + 性能模型选配置。在 Perlmutter / Frontier 上扩至 2048 GPU，相对已有方法加速 2.3–12.5×，处理十亿边图。 |
| 可研究性 | **很高（系统方向）**。大数据图学习的系统瓶颈仍在；可研究混合并行、流水线、与采样训练统一。需超算资源。 |
| 可复现性 | **中**。代码开源，但完整扩展实验需要大规模 GPU 集群；单机可验证正确性与小规模并行。 |

#### 15. ScaleGNN: Towards Scalable Graph Neural Networks via Adaptive High-order Neighboring Feature Fusion

| 项目 | 内容 |
|------|------|
| 本地文件 | `03-scalable-bigdata-gnn/15_ScaleGNN_WWW2026.pdf` |
| 会议 | **WWW 2026** |
| 作者 | Xiang Li, Haobing Liu, Jianpeng Qi, Yanwei Yu, Yuan Cao, Guoqing Chao |
| arXiv | https://arxiv.org/abs/2504.15920 |
| DOI | https://doi.org/10.1145/3774904.3792347 |
| 开源代码 | **有** — https://github.com/lx970414/ScaleGNN |
| 研究目的 | 大规模图上重复高阶聚合既贵又过平滑。计算每跳纯邻居矩阵，用 Local Contribution Score 掩蔽低相关高阶邻居，可学习稀疏融合低/高阶特征。仓库还给出 papers100M 的 memmap 训练路径。 |
| 可研究性 | **高**。算法层面的可扩展 GNN，比超算系统更容易在实验室跟进；可研究与采样、图重排序、IO-aware kernel 的结合。 |
| 可复现性 | **中高**。代码支持 arxiv/products/papers100M；papers100M 需要较大磁盘与内存，但 ogbn-arxiv 可在单卡复现。 |

#### 16. On Efficient Scaling of GNNs via IO-Aware Layers Implementations

| 项目 | 内容 |
|------|------|
| 本地文件 | `03-scalable-bigdata-gnn/16_IOAware_GNN_ICML2026.pdf` |
| 会议 | **ICML 2026 Spotlight** |
| 作者 | Daria Fomina, Daniil Krasylnikov, Alexey Boykov 等（Yandex Research） |
| arXiv | https://arxiv.org/abs/2605.31500 |
| 开源代码 | **有** — https://github.com/yandex-research/On-Efficient-Scaling-Of-GNNs |
| 研究目的 | 类比 FlashAttention：GNN 层的瓶颈是稀疏不规则访存与边级中间量物化。将常用层归为 SpMM 卷积、reduction 聚合、注意力（GATv2 / Graph Transformer）三类，分别设计 IO-aware CUDA/Triton kernel。GATv2 最高约 8.5× 加速、峰值显存可降约 76×。 |
| 可研究性 | **很高（系统+算法交叉）**。硬件感知 GNN 是 2026 新热点；可做更多层类型、动态图、多 GPU。 |
| 可复现性 | **中高**。提供 PyG/DGL/cuGraph 的 drop-in 替换；需 NVIDIA GPU 与 CUDA 环境。 |

#### 17. Communication-free Sampling and 4D Hybrid Parallelism for Scalable Mini-batch GNN Training

| 项目 | 内容 |
|------|------|
| 本地文件 | `03-scalable-bigdata-gnn/17_4DHybridParallel_MiniBatchGNN_arXiv.pdf` |
| 状态 | **arXiv:2604.02651（2026）**，与 Plexus 同组的 mini-batch 路线（文中亦称 ScaleGNN，请勿与 WWW 的 ScaleGNN 混淆） |
| 作者 | Cunyang Wei, Siddharth Singh, Aishwarya Sarkar, Abhinav Bhatele 等（UMD / NVIDIA / Iowa State / LLNL） |
| arXiv | https://arxiv.org/abs/2604.02651 |
| 开源代码 | **论文声称开源框架，正文未给出独立 GitHub URL**（可关注 https://github.com/hpcgroup ） |
| 研究目的 | 分布式 mini-batch GNN 的采样通信与纯数据并行扩展差。提出无通信均匀顶点采样 + 3D 并行矩阵乘 + 数据并行的 4D 混合并行，在 2048 GPU 上扩展，ogbn-products 端到端约 3.5×。 |
| 可研究性 | **高**。与 Plexus（全图）形成对照；采样无通信是可验证的算法贡献，即使没有超算也可做小规模分析。 |
| 可复现性 | **中低**。完整扩展需超算；公开仓库链接在检索时不如 Plexus 明确。 |

---

### D. GraphRAG 与大模型（`04-graphrag-llm/`）

#### 18. GraphRAG-R1: Graph Retrieval-Augmented Generation with Process-Constrained Reinforcement Learning

| 项目 | 内容 |
|------|------|
| 本地文件 | `04-graphrag-llm/18_GraphRAG-R1_WWW2026.pdf` |
| 会议 | **WWW 2026** |
| 作者 | Chuanyue Yu, Kuo Zhao, Yuhan Li, Heng Chang, Jia Li, Jianxin Li, Ziwei Zhang 等 |
| arXiv | https://arxiv.org/abs/2507.23581 |
| DOI | https://doi.org/10.1145/3774904.3792589 |
| 开源代码 | **有** — https://github.com/ycygit/GraphRAG-R1 |
| 权重 | https://huggingface.co/yuchuanyue/GraphRAG-R1 ；Zenodo：https://doi.org/10.5281/zenodo.18349146 |
| 研究目的 | 现有 GraphRAG 查询/检索依赖启发式，多跳推理弱。用带过程约束的结果型 RL（改进 GRPO）训练 LLM：PRA 奖励鼓励必要检索，CAF 奖励抑制过度思考，分阶段训练格式、行为与智能。 |
| 可研究性 | **很高**。GraphRAG + RL 是 2025–2026 交叉热点，适合跟奖励设计、工具调用、混合图–文本检索。 |
| 可复现性 | **中**。代码与权重公开，但需要 GPU 与 LLM API/本地大模型，训练成本高；推理评测相对可做。 |

#### 19. Graph-R1: Towards Agentic GraphRAG Framework via End-to-end Reinforcement Learning

| 项目 | 内容 |
|------|------|
| 本地文件 | `04-graphrag-llm/19_Graph-R1_Agentic_arXiv.pdf` |
| 状态 | **arXiv:2507.21892（2025–2026 持续更新）** |
| 作者 | Haoran Luo, Haihong E, Guanting Chen, Luu Anh Tuan 等 |
| arXiv | https://arxiv.org/abs/2507.21892 |
| 开源代码 | **有** — https://github.com/LHRLAB/Graph-R1 |
| 研究目的 | 第一篇强调端到端 RL 的智能体 GraphRAG：轻量知识超图构造，将检索建模为多轮 think–retrieve–rethink–generate，用生成质量、检索相关性与路径结构可靠性统一奖励。 |
| 可研究性 | **很高**。智能体 + 超图环境可扩展到动态知识、多工具与可解释路径。 |
| 可复现性 | **中**。代码公开；RL 训练与超图构建对算力和 LLM 调用敏感。 |

#### 20. MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation

| 项目 | 内容 |
|------|------|
| 本地文件 | `04-graphrag-llm/20_MemGraphRAG_KDD2026.pdf` |
| 会议 | **KDD 2026** |
| 作者 | Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Qinggang Zhang, Jinsong Su 等（厦门大学） |
| arXiv | https://arxiv.org/abs/2606.00610 |
| DOI | https://doi.org/10.1145/3770855.3818074 |
| 开源代码 | **有** — https://github.com/XMUDeepLIT/MemGraphRAG |
| 研究目的 | 现有 GraphRAG 抽图是片段级、缺全局视角，导致主题不一致与结构破碎。用共享记忆的多智能体协作建图（schema / fact / passage 三层记忆），并做记忆感知的层次检索。 |
| 可研究性 | **高**。图构建质量常被忽视；记忆冲突消解、本体归纳与大规模语料建图都是可做方向。 |
| 可复现性 | **中高**。官方仓库文档完整；完整流水线依赖 LLM 抽三元组，成本中等。 |

#### 21. GraphRAG-Router: Learning Cost-Efficient Routing over GraphRAGs and LLMs with Reinforcement Learning

| 项目 | 内容 |
|------|------|
| 本地文件 | `04-graphrag-llm/21_GraphRAG-Router_arXiv.pdf` |
| 状态 | **arXiv:2604.16401（2026）** |
| 作者 | Dongzhe Fan, Chuanhao Ji, Zimu Wang, Tong Chen, Qiaoyu Tan（NYU Shanghai / Liverpool） |
| arXiv | https://arxiv.org/abs/2604.16401 |
| 开源代码 | **未见独立官方仓库**；实现基于 https://github.com/RUC-NLPIR/Search-o1 与 https://github.com/verl-project/verl |
| 研究目的 | 固定 GraphRAG + 单一大 LLM 成本高、不适应问题难度。层次路由协调异构 GraphRAG 与生成模型，SFT 预热后两阶段 RL，第二阶段课程式代价感知奖励，大模型过度使用约降 30%。 |
| 可研究性 | **高**。成本–效果权衡对实际部署极重要；可研究更细的查询复杂度估计与在线路由。 |
| 可复现性 | **中低**。无独立完整仓库，依赖多套 GraphRAG 与多个 LLM，复现门槛高。 |

#### 22. Core-based Hierarchies for Efficient GraphRAG

| 项目 | 内容 |
|------|------|
| 本地文件 | `04-graphrag-llm/22_CoreGraphRAG_KDD2026.pdf` |
| 会议 | **KDD 2026** |
| 作者 | Jakir Hossain, Ahmet Erdem Sarıyüce（University at Buffalo） |
| arXiv | https://arxiv.org/abs/2603.05207 |
| DOI | https://doi.org/10.1145/3770855.3818007 |
| 作者主页 PDF | https://sariyuce.com/papers/sigkdd26.pdf |
| 开源代码 | **有** — https://github.com/erdemUB/KDD26 ；Zenodo：https://doi.org/10.5281/zenodo.20500254 |
| 研究目的 | 证明稀疏知识图上模块度优化存在指数多近优划分，Leiden 社区不可复现。用 \(k\)-core 分解得到确定性、线性时间、密度感知的层次，并配合 token 预算采样降低 LLM 成本，提升全局 sensemaking。 |
| 可研究性 | **很高**。把图挖掘经典核分解接到 GraphRAG，理论+系统都清晰；可研究其他可复现社区发现、动态核维护。 |
| 可复现性 | **中高**。代码公开；评测用 LLM-as-judge，存在评委方差，但算法部分可严格复现。 |

---

### E. 数据挖掘中的安全（`05-data-mining-security/`）

#### 23. Defending against Model Extraction for GNNs with Model Reprogramming（GraphRP）

| 项目 | 内容 |
|------|------|
| 本地文件 | `05-data-mining-security/23_GraphRP_KDD2026.pdf` |
| 会议 | **KDD 2026** |
| 作者 | Yan Wen, Zhenyi Wang, Heng Huang（University of Maryland） |
| arXiv | https://arxiv.org/abs/2608.11495 |
| DOI | https://doi.org/10.1145/3770855.3817983 |
| 开源代码 | **有** — https://github.com/overwenyan/GraphRP-KDD2026 |
| 研究目的 | MLaaS 中 GNN 面临模型窃取。指出把图像噪声防御直接搬到图上存在 “Euclidean bias”。提出 GraphRP：结构感知门控 + 可学习拓扑原型构成动态结构防火墙，良性查询保持精度，对抗查询放大估计误差，并给出攻击者误差下界。 |
| 可研究性 | **高**。图模型知识产权与安全是数据挖掘落地痛点；可研究自适应攻击、异构图与归纳设置。 |
| 可复现性 | **高**。论文附录给出实验代码地址；标准图分类基准即可开展。 |

---

### F. CVPR 视觉图（`06-cvpr-vision-graph/`，CCF-A）

> CVPR 上的“图”多数是**视觉场景图 / 3D 功能图**，用图结构表达物体关系，而不是通用消息传递 GNN 理论。适合视觉+图交叉，不宜当作 GNN 主会。

#### 24. Robo-SGG: Exploiting Layout-Oriented Normalization and Restitution Can Improve Robust Scene Graph Generation

| 项目 | 内容 |
|------|------|
| 本地文件 | `06-cvpr-vision-graph/24_Robo-SGG_CVPR2026.pdf` |
| 会议 | **CVPR 2026（CCF-A）** |
| 作者 | Changsheng Lv, Zijian Fu, Mengshi Qi（北京邮电大学） |
| arXiv | https://arxiv.org/abs/2504.12606 |
| 开放 PDF | https://openaccess.thecvf.com/content/CVPR2026/html/Lv_Robo-SGG_Exploiting_Layout-Oriented_Normalization_and_Restitution_Can_Improve_Robust_Scene_CVPR_2026_paper.html |
| 开源代码 | **有** — https://github.com/MICLAB-BUPT/Robo-SGG |
| 研究目的 | 面向噪声/模糊/恶劣天气等损坏图像的鲁棒场景图生成。用布局信息抗域偏移：Instance Normalization 去掉域特异统计，Layout-Oriented Restitution 恢复结构特征，Layout-Embedded Encoder 门控融合布局与视觉。可即插即用到已有 SGG 模型。 |
| 可研究性 | **高**（视觉图方向）。损坏场景下的关系推理、布局先验可迁移到视频 SGG 与具身导航。 |
| 可复现性 | **中高**。代码公开；依赖 Visual Genome / GQA 及损坏基准 VG-C、GQA-C。 |

#### 25. FunFact: Building Probabilistic Functional 3D Scene Graphs via Factor-Graph Reasoning

| 项目 | 内容 |
|------|------|
| 本地文件 | `06-cvpr-vision-graph/25_FunFact_CVPR2026.pdf` |
| 会议 | **CVPR 2026（CCF-A）** |
| 开放 PDF | https://openaccess.thecvf.com/content/CVPR2026/papers/Fu_FunFact_Building_Probabilistic_Functional_3D_Scene_Graphs_via_Factor-Graph_Reasoning_CVPR_2026_paper.pdf |
| 项目页 | https://funfact-scenegraph.github.io/ |
| 开源代码 | 项目页给出资源；仓库以主页为准 |
| 研究目的 | 从位姿 RGB-D 构建开放词汇、带概率的**功能 3D 场景图**。用因子图联合推断所有功能边，融合 LLM 常识先验与几何先验，并发布 FunThor 基准。强调整体功能关系而非孤立物体对。 |
| 可研究性 | **高**。功能场景图连接 GNN、3D 视觉与机器人；校准、开放词汇关系、因子图可扩展。 |
| 可复现性 | **中**。有项目页与合成数据 FunThor；完整 3D 实验对 GPU 与仿真环境要求较高。 |

#### 26. GraPHFormer: A Multimodal Graph Persistent Homology Transformer for the Analysis of Neuroscience Morphologies

| 项目 | 内容 |
|------|------|
| 本地文件 | `06-cvpr-vision-graph/26_GraPHFormer_CVPR2026.pdf` |
| 会议 | **CVPR 2026（CCF-A）** |
| 开放 PDF | https://openaccess.thecvf.com/content/CVPR2026/papers/Shah_GraPHFormer_A_Multimodal_Graph_Persistent_Homology_Transformer_for_the_Analysis_CVPR_2026_paper.pdf |
| 开源代码 | **正文未给出独立 GitHub** |
| 研究目的 | 用图 Transformer + 持续同调图像 + TreeLSTM 分析神经元/胶质细胞骨架形态，面向神经科学形态计量。展示 GNN 在非网格、树状生物图上的应用。 |
| 可研究性 | **中高**。拓扑+图的形态分析可迁移到分子图、血管图；与主线 GNN 理论距离较远。 |
| 可复现性 | **中低**。未见官方仓库；神经形态数据标注异构。 |

---

### G. AAAI / IJCAI / SIGIR（`07-ccf-aaai-ijcai-sigir/`，CCF-A）

#### 27. High-Pass Matters: Theoretical Insights and Sheaflet-Based Design for Hypergraph Neural Networks（HyperSheaflets）

| 项目 | 内容 |
|------|------|
| 本地文件 | `07-ccf-aaai-ijcai-sigir/27_HyperSheaflets_AAAI2026.pdf` |
| 会议 | **AAAI 2026 Oral，Outstanding Paper Award（CCF-A）** |
| 作者 | Ming Li, Yujie Fang, Dongrui Shen, Han Feng, Xiaosheng Zhuang, Kelin Xia, Pietro Lio |
| DOI | https://doi.org/10.1609/aaai.v40i27.39469 |
| 作者 PDF | http://staffweb1.cityu.edu.hk/xzhuang7/pubs/2026-LFSFZXL-AAAI-Sheaflets.pdf |
| 附录 | https://mingli-ai.github.io/HyperSheaflets.pdf |
| 开源代码 | **未见独立仓库**（附录有实现细节） |
| 研究目的 | 证明超图神经网络不能只做低通滤波；高通分量对局部可分结构关键。结合 cell sheaf 与 framelet，提出 HyperSheaflets，显式保留高通与多尺度谱分解。 |
| 可研究性 | **很高**。超图+层体（sheaf）+高通是可发理论文的切口，与异配、高阶关系挖掘直接相关。 |
| 可复现性 | **中**。基准公开，代码需按附录复现。 |

#### 28. HyperNoRA: Hyperedge Prediction via Node-Level Relation-Aware Self-Supervised Hypergraph Learning

| 项目 | 内容 |
|------|------|
| 本地文件 | `07-ccf-aaai-ijcai-sigir/28_HyperNoRA_AAAI2026.pdf` |
| 会议 | **AAAI 2026 Oral（CCF-A）** |
| DOI | https://doi.org/10.1609/aaai.v40i27.39470 |
| 正式 PDF | https://ojs.aaai.org/index.php/AAAI/article/view/39470 |
| 开源代码 | **正文未给出 GitHub** |
| 研究目的 | 超边预测常只看候选超边内的局部聚合。HyperNoRA 建全局节点关系图捕获直接/间接相关，结构感知聚合 + 对比学习防过平滑，做自监督超图表示与超边预测。 |
| 可研究性 | **高**。超边预测是数据挖掘中的高阶链接预测；全局关系图可与对比学习、采样策略结合。 |
| 可复现性 | **中**。标准超图基准可复现，缺官方代码。 |

#### 29. Sheaf Graph Neural Networks via PAC-Bayes Spectral Optimization（SGPC）

| 项目 | 内容 |
|------|------|
| 本地文件 | `07-ccf-aaai-ijcai-sigir/29_SGPC_AAAI2026_official.pdf` |
| 会议 | **AAAI 2026（CCF-A）** |
| 作者 | Yoonhyuk Choi, Jiho Choi, Taewook Ko, JongWook Kim, Chong-Kwon Kim |
| arXiv | https://arxiv.org/abs/2508.00357 |
| DOI | https://doi.org/10.1609/aaai.v40i25.39193 |
| 开源代码 | **有** — https://github.com/ChoiYoonHyuk/SGPC |
| 研究目的 | 针对异配图过平滑：用最优传输学习 sheaf restriction map，方差缩减扩散 + 自适应频率混合，并以 PAC-Bayes 谱正则给出未见节点上的认证置信区间。线性复杂度端到端训练。 |
| 可研究性 | **很高**。Sheaf GNN + 可证明泛化是理论友好选题；可接到更大规模图与动态图。 |
| 可复现性 | **高**。官方脚本覆盖 Cora 等到 Wisconsin 共 9 个基准。 |

#### 30. Question-Adaptive Graph Learning for Multi-hop Retrieval Augmented Generation（Quest-GNN）

| 项目 | 内容 |
|------|------|
| 本地文件 | `07-ccf-aaai-ijcai-sigir/30_Quest-GNN_SIGIR2026.pdf` |
| 会议 | **SIGIR 2026（CCF-A）** |
| arXiv | https://arxiv.org/abs/2510.11541 |
| DOI | https://doi.org/10.1145/3805712.3809693 |
| 开源代码 | **有** — https://github.com/Jerry2398/QSGNN |
| 研究目的 | 多跳 RAG 中问题语义复杂、检索易引入噪声。构建多层信息知识图 Multi-L KG，用问题自适应 GNN（层内/层间消息传递由问题引导）做表示学习，并用合成数据预训练。高跳问题上最高约 33.8% 提升。 |
| 可研究性 | **很高**。GNN 作为检索器，衔接数据挖掘、信息检索与 GraphRAG。 |
| 可复现性 | **中高**。代码公开；完整 RAG 流水线依赖检索语料与 LLM。 |

#### 34. Exploring the Over-smoothing Problem of Graph Neural Networks for Graph Classification: An Entropy-based Viewpoint

| 项目 | 内容 |
|------|------|
| 本地文件 | `07-ccf-aaai-ijcai-sigir/34_Oversmoothing_Entropy_IJCAI2025.pdf` |
| 会议 | **IJCAI 2025（CCF-A）**；IJCAI 2026 论文集 PDF 检索时尚未开放 |
| 正式 PDF | https://www.ijcai.org/proceedings/2025/0360.pdf |
| 开源代码 | **有** — https://github.com/Sophia0830BNU/SDE |
| 研究目的 | 从图分类（而非节点分类）角度用熵刻画过平滑，分析深层 GNN 在图级任务上的表示坍缩，并给出相应缓解思路。 |
| 可研究性 | **高**。过平滑文献以节点分类为主，图分类视角仍有空位；可与 09 GBN、11 IGNN 对照。 |
| 可复现性 | **高**。代码与 IJCAI 正式 PDF 均可获得。 |

IJCAI 2026 已接收、建议跟进但暂无公开 PDF 的相关工作：`A unified spectral-spatial framework for GNNs`（Qin 等）、`ADC-GNN`（Tang 等）、`Mitigating Dynamic Graph Distribution Shifts via Spectral Augmentation`（https://github.com/Qiana/DSPA）。待 https://www.ijcai.org/proceedings/2026/ 上线后可补下载。

---

### H. CCF-A 期刊（`08-ccf-journals/`）

#### 31. PUMA: Efficient Continual Graph Learning for Node Classification with Graph Condensation

| 项目 | 内容 |
|------|------|
| 本地文件 | `08-ccf-journals/31_PUMA_TKDE2025.pdf` |
| 期刊 | **IEEE TKDE 2025, 37(1):449–461（CCF-A）** |
| arXiv | https://arxiv.org/abs/2312.14439 |
| DOI | https://doi.org/10.1109/tkde.2024.3485691 |
| 开源代码 | **有** — https://github.com/superallen13/PUMA |
| 研究目的 | 流式图上灾难性遗忘。用图压缩构造伪标签引导的记忆库，覆盖未标注节点，从头训练平衡新旧图，并用一次性传播与宽编码器加速。面向持续图学习与大数据增量场景。 |
| 可研究性 | **很高**。持续学习 + 图压缩是数据挖掘落地刚需；可接到推荐、反欺诈的流图。 |
| 可复现性 | **高**。代码公开，节点分类基准可跟。 |

#### 32. Graph Condensation: A Survey

| 项目 | 内容 |
|------|------|
| 本地文件 | `08-ccf-journals/32_GraphCondensation_Survey_TKDE2025.pdf` |
| 期刊 | **IEEE TKDE 2025（CCF-A）** |
| arXiv | https://arxiv.org/abs/2401.11720 |
| 资源汇总 | https://github.com/XYGaoG/Graph-Condensation-Papers |
| 开源代码 | 综述；相关库见 GraphSlim、GC-Bench、GCondenser |
| 研究目的 | 系统综述图压缩：有效性、泛化、效率、公平、鲁棒五类评价，以及优化策略与压缩图生成。直接服务大规模 GNN 训练降本。 |
| 可研究性 | **很高（作为起点）**。综述把问题空间划清，适合选题与写 related work。 |
| 可复现性 | **高**（读综述 + 跟链接仓库）；本身不是单一算法复现。 |

#### 33. Graph Neural Networks for Graphs with Heterophily: A Survey

| 项目 | 内容 |
|------|------|
| 本地文件 | `08-ccf-journals/33_HeterophilyGNN_Survey_TKDE2026.pdf` |
| 期刊 | **IEEE TKDE 2026, 38(7):4385–4404（CCF-A）** |
| arXiv | https://arxiv.org/abs/2202.07082 |
| 开源代码 | 综述，文中列出大量方法仓库（H2GCN、CPGNN 等） |
| 研究目的 | 异配图 GNN 全面分类与分析，讨论异配与其他图学习问题的关系，并指出未来方向。是同配/异配主线必读期刊综述。 |
| 可研究性 | **很高**。与 11 IGNN 互补：一个是 2025 会议新理论，一个是期刊系统综述。 |
| 可复现性 | **高**（作为文献地图）；具体方法需分别跟原仓库。 |

#### 35. Deeper Insights into Deep Graph Convolutional Networks: Stability and Generalization

| 项目 | 内容 |
|------|------|
| 本地文件 | `08-ccf-journals/35_DeepGCN_Stability_TPAMI2026.pdf` |
| 期刊 | **IEEE TPAMI 2026, 48(2):1707–1719（CCF-A）** |
| arXiv | https://arxiv.org/abs/2410.08473 |
| DOI | https://doi.org/10.1109/TPAMI.2025.3616350 |
| 开源代码 | **理论文，无独立实现仓库** |
| 研究目的 | 给出深层 GCN 稳定性与泛化上界，关键因子包括图滤波器最大绝对特征值与网络深度。补上以往多集中于单层 GCN 的理论空白。 |
| 可研究性 | **很高（理论方向）**。可与 09 GBN 的深层实践对照，做“理论界 vs 可训练深度”。 |
| 可复现性 | **中**。以证明为主；数值验证可按文中设定自行实现。 |

IEEE TNNLS（CCF-B）上另有 2025 年 SGB-Net 等可扩展 GNN 工作（DOI: https://doi.org/10.1109/tnnls.2025.3552129），IEEE 付费墙下本次未另存 PDF；已收录开放 arXiv 的 **ScaDyG（43）**。

---

### I. 数据库系统：VLDB / ICDE（`09-db-systems-sigmod-vldb-icde/`）

面向**十亿节点级全图训练、核外 SSD、云资源波动**，与目录 `03-scalable-bigdata-gnn/` 互补：那边偏算法与超算内核，这边是数据库/系统顶会的完整训练系统。

#### 36. NeutronTP: Load-Balanced Distributed Full-Graph GNN Training with Tensor Parallelism

| 项目 | 内容 |
|------|------|
| 本地文件 | `09-db-systems-sigmod-vldb-icde/36_NeutronTP_VLDB2025.pdf` |
| 会议/期刊 | **PVLDB 18(2):173–，VLDB 2025（CCF-A）** |
| 作者 | Xin Ai, Hao Yuan, Zeyu Ling, Qiange Wang, Yanfeng Zhang 等（东北大学） |
| arXiv | https://arxiv.org/abs/2412.20379 |
| 正式 PDF | https://www.vldb.org/pvldb/vol18/p173-ai.pdf |
| 开源代码 | **有** — https://github.com/AiX-im/NeutronTP （镜像/组织页亦见 iDC-NEU） |
| 研究目的 | 全图分布式 GNN 的**张量并行**：按特征切片而非切图，消除跨 worker 的顶点依赖；把 NN 运算与图聚合解耦以降低通信频次，并用内存高效子图调度做通信–计算重叠与负载均衡。 |
| 可研究性 | **很高**。与 14 Plexus 的 3D 并行对照，可做“切特征 vs 切图”的系统对比；适合大数据方向的系统论文跟进。 |
| 可复现性 | **中**。代码公开，但完整复现需要多机 GPU 集群；仓库说明仍在重构部分功能。 |

#### 37. NeutronTask: Scalable and Efficient Multi-GPU GNN Training with Task Parallelism

| 项目 | 内容 |
|------|------|
| 本地文件 | `09-db-systems-sigmod-vldb-icde/37_NeutronTask_VLDB2025.pdf` |
| 会议/期刊 | **PVLDB 18(6):1705–1719, VLDB 2025（CCF-A）** |
| 作者 | Zhenbo Fu, Xin Ai, Qiange Wang, Yanfeng Zhang 等 |
| 正式 PDF | https://www.vldb.org/pvldb/vol18/p1705-fu.pdf |
| DOI | https://doi.org/10.14778/3725688.3725700 |
| 开源代码 | **有** — https://github.com/iDC-NEU/NeutronTask |
| 研究目的 | 单机多 GPU 上邻居复制与中间激活常占内存 80%+。提出 **GNN 任务并行**：按层内任务而非图结构切分，减少跨 GPU 邻居复制；任务解耦后尽早释放中间数据。4×A5000 上可支撑十亿边级全图训练。 |
| 可研究性 | **高**。任务并行在 GNN 系统里仍少见，可接到异构 GPU / 流水线调度。 |
| 可复现性 | **中高**。仓库基于 NeutronStar，含 GCN/GAT 工具包；需要多 GPU 与 CUDA 环境。 |

#### 38. NeutronCloud: Resource-Aware Distributed GNN Training in Fluctuating Cloud Environments

| 项目 | 内容 |
|------|------|
| 本地文件 | `09-db-systems-sigmod-vldb-icde/38_NeutronCloud_VLDB2026.pdf` |
| 会议/期刊 | **PVLDB 19(1):56–69（VLDB 2026 / 2025 刊出，CCF-A）** |
| 作者 | Mingyi Cao, Chunyu Cao, Yanfeng Zhang, Zhenbo Fu, Xin Ai, Qiange Wang, Yu Gu, Ge Yu |
| 正式 PDF | https://www.vldb.org/pvldb/vol19/p56-cao.pdf |
| DOI | https://doi.org/10.14778/3772181.3772186 |
| 开源代码 | **有** — https://github.com/Toaoc/NeutronCloud |
| 研究目的 | 云上算力/带宽波动时，静态切图导致负载错配。资源感知地调节“本地计算依赖 vs 远程拉取依赖”的比例，并用依赖感知的 partial-reduce 跳过掉队 worker。相对 SOTA 分布式 GNN 系统约 **1.83×–4.43×** 加速。 |
| 可研究性 | **很高**。云原生图训练、弹性资源与 GraphRAG 后端同属大数据落地问题。 |
| 可复现性 | **中**。代码与技术报告在仓库；完整云波动实验依赖受控带宽/算力注入。 |

#### 39. Hyperion: Optimizing SSD Access is All You Need to Enable Cost-efficient Out-of-core GNN Training

| 项目 | 内容 |
|------|------|
| 本地文件 | `09-db-systems-sigmod-vldb-icde/39_Hyperion_ICDE2025.pdf` |
| 会议 | **ICDE 2025（CCF-A）** |
| 作者 | Jie Sun, Mo Sun, Zheng Zhang, Zuocheng Shi, Jun Xie, Zihan Yang, Jie Zhang, Zeke Wang, Fei Wu（浙江大学等） |
| 作者 PDF | https://wangzeke.github.io/doc/Hyperion-ICDE25.pdf |
| 开源代码 | **有** — https://github.com/RC4ML/Hyperion |
| 研究目的 | TB 级图的**核外训练**：GPU 发起的异步 NVMe IO 栈 + 与 GNN 计算流水线协同，用廉价 SSD 逼近内存级吞吐（TPC，单位成本吞吐）。相对核外基线可更高吞吐，相对加 GPU 服务器的方案 TPC 可高一个数量级。 |
| 可研究性 | **很高**。大数据“存算分离 / 核外图学习”的直接切口；IO 栈也可迁到 RAG/KVCache。 |
| 可复现性 | **中**。开源完整，但需要 NVMe + GPU 的单机实验平台，数据规模大。 |

---

### J. WSDM 数据挖掘（`10-wsdm/`，CCF-B）

WSDM 是 Web 搜索与数据挖掘主会，图压缩、图遗忘安全、AutoGNN 都与数据挖掘选题直接相关。

#### 40. Multi-view Graph Condensation via Tensor Decomposition（GCTD）

| 项目 | 内容 |
|------|------|
| 本地文件 | `10-wsdm/40_GCTD_WSDM2026.pdf` |
| 会议 | **WSDM 2026（CCF-B）** |
| 作者 | Nicolas Roque dos Santos, Dawon Ahn, Diego Minatel, Alneu de Andrade Lopes, Evangelos Papalexakis |
| arXiv | https://arxiv.org/abs/2508.14330 |
| DOI | https://doi.org/10.1145/3773966.3777968 |
| 开源代码 | **有** — https://github.com/nicolasrsantos/gctd |
| 研究目的 | 现有图压缩多为双层优化、代价高且缺少合成节点到原节点的可解释映射。GCTD 用随机边扰动构造多视图，再以**张量分解**合成小图，避免双层优化。六数据集上最多约 4% 精度提升，大图上与现有方法竞争力相当。 |
| 可研究性 | **很高**。与 32 图压缩综述、31 PUMA 同一主线；免双层优化是明确可发点。 |
| 可复现性 | **高**。PyG + TensorLy，Cora 等自动下载；Flickr/Reddit 需 GraphSAINT 数据。 |

#### 41. Unlearning Inversion Attacks for Graph Neural Networks

| 项目 | 内容 |
|------|------|
| 本地文件 | `10-wsdm/41_UnlearningInversion_WSDM2026.pdf` |
| 会议 | **WSDM 2026（CCF-B）** |
| 作者 | Jiahao Zhang, Yilong Wang, Zhiwei Zhang, Xiaorui Liu, Suhang Wang |
| arXiv | https://arxiv.org/abs/2506.00808 |
| DOI | https://doi.org/10.1145/3773966.3777929 |
| 开源代码 | **有** — https://github.com/QwQ2000/WSDM26-Graph-Unlearning-Inversion |
| 研究目的 | 挑战“图遗忘后被删边无法恢复”的假设。提出 **TrendAttack**：利用遗忘边邻接节点的置信度骤降（confidence pitfall），在黑盒 + 部分图知识下重构被删边。四数据集上显著强于已有 GNN 成员推断基线。 |
| 可研究性 | **高**。与 23 GraphRP（模型窃取防御）构成“攻防”对照；隐私合规与推荐/社交图挖掘都需要。 |
| 可复现性 | **高**。公开 PyG 实现与复现命令，Cora 等公开数据。 |

#### 42. Proficient Graph Neural Network Design by Accumulating Knowledge on Large Language Models（DesiGNN）

| 项目 | 内容 |
|------|------|
| 本地文件 | `10-wsdm/42_DesiGNN_WSDM2026.pdf` |
| 会议 | **WSDM 2026（CCF-B）** |
| 作者 | Jialiang Wang, Hanmo Liu, Shimin Di, Zhili Wang, Jiachuan Wang, Lei Chen, Xiaofang Zhou |
| arXiv | https://arxiv.org/abs/2408.06717 |
| DOI | https://doi.org/10.1145/3773966.3777982 |
| 开源代码 | **有** — https://github.com/jilwang84/DesiGNN |
| 研究目的 | LLM 直接设计 GNN 容易给出通用/误导架构。DesiGNN 把历史设计经验沉淀为可元学习的知识先验，对齐基准上的图性质过滤与文献洞察，对未见数据集在数秒内给出约 top-5.77% 的初始架构，并以很小搜索代价 refinement。 |
| 可研究性 | **高**。AutoML + GNN + LLM 交叉，适合数据挖掘里的“模型选择”问题；注意 NAS-Bench-Graph 防泄漏设定。 |
| 可复现性 | **中高**。代码/数据/prompt 公开，但依赖 GPT-4 类 API，成本与版本漂移需自行控制。 |

WSDM 2026 另有 **Towards Multifaceted Graph Condensation in Discrete Realm（DGC）**（DOI [10.1145/3773966.3777965](https://doi.org/10.1145/3773966.3777965)，代码宣称 https://github.com/Yejunda/DGC）以及 Bridge Breaking GNN 等，ACM 付费或未找到稳定开放 PDF，故未入库。

---

### K. TNNLS / JMLR（`11-journals-tnnls-jmlr/`）

#### 43. ScaDyG: A New Paradigm for Large-Scale Dynamic Graph Learning

| 项目 | 内容 |
|------|------|
| 本地文件 | `11-journals-tnnls-jmlr/43_ScaDyG_TNNLS2026.pdf` |
| 期刊 | **IEEE TNNLS 2026（CCF-B）**，DOI [10.1109/TNNLS.2025.3650673](https://doi.org/10.1109/TNNLS.2025.3650673) |
| 作者 | Xiang Wu, Xunkai Li, Rong-Hua Li, Kangfei Zhao, Guoren Wang |
| arXiv | https://arxiv.org/abs/2501.16002 |
| 开源代码 | **有** — https://github.com/BITNEO/ScaDyG |
| 研究目的 | 工业动态图历史交互膨胀导致动态 GNN 难扩展。ScaDyG：时间感知拓扑重构（预处理内无参传播）+ 指数型时间编码 + Hypernetwork 自适应聚合。12 个数据集上节点/链接任务与 SOTA 相当或更好，参数更少、效率更高。 |
| 可研究性 | **很高**。大规模动态图是数据挖掘刚需，可接到反欺诈、推荐时序图。 |
| 可复现性 | **中高**。PyTorch 仓库与 mooc 示例；完整 TGB/zenodo 数据需另下。 |

#### 44. Improving Graph Neural Networks on Multi-node Tasks with the Labeling Trick

| 项目 | 内容 |
|------|------|
| 本地文件 | `11-journals-tnnls-jmlr/44_LabelingTrick_JMLR2025.pdf` |
| 期刊 | **JMLR 26(23):1–44, 2025（CCF-A，开放获取）** |
| 作者 | Xiyuan Wang, Pan Li, Muhan Zhang |
| 正式 PDF | https://www.jmlr.org/papers/volume26/23-0560/23-0560.pdf |
| 开源代码 | **有** — https://github.com/GraphPKU/LabelingTrick |
| 研究目的 | 证明直接聚合单节点嵌入无法刻画多节点依赖；提出 labeling trick：按目标节点集关系先打标签再跑 GNN。统一解释 SEAL 等节点标注方法，覆盖无向/有向链接、超边、子图预测。 |
| 可研究性 | **很高（理论+方法）**。链接预测与子图任务的标准工具；可向超图、时序链接扩展。 |
| 可复现性 | **高**。JMLR 开放获取 + 分任务仓库（LinkPred / DirLinkPred / Hyper / SubG）。 |

#### 45. Implicit vs Unfolded Graph Neural Networks

| 项目 | 内容 |
|------|------|
| 本地文件 | `11-journals-tnnls-jmlr/45_ImplicitUnfoldedGNN_JMLR2025.pdf` |
| 期刊 | **JMLR 26(82):1–46, 2025（CCF-A）** |
| 作者 | Yongyi Yang, Tang Liu, Yangkun Wang, Zengfeng Huang, David Wipf |
| arXiv | https://arxiv.org/abs/2111.06592 |
| 正式 PDF | https://www.jmlr.org/papers/volume26/22-0459/22-0459.pdf |
| 开源代码 | 比较研究；文中引用 IGNN 实现 https://github.com/SwiftieH/IGNN （未见本篇独立仓库） |
| 研究目的 | 系统比较**隐式 GNN（平衡点 / DEQ）**与**展开式 GNN（能量函数梯度下降展开）**：何时解等价、何时在收敛、表达力、可解释性上分叉。实验表明 IGNN 更省显存，UGNN 在对抗扰动、异配、长程上可配注意力与传播规则。 |
| 可研究性 | **很高**。与 11 IGNN-homophily、09 过平滑、10 长程直接对话，适合写理论综述式跟进。 |
| 可复现性 | **中**。公开基准可复现实验设定；需自行拼 IGNN/UGNN 实现。 |

#### 46. Orthogonal Bases for Equivariant Graph Learning with Provable k-WL Expressive Power

| 项目 | 内容 |
|------|------|
| 本地文件 | `11-journals-tnnls-jmlr/46_EquivariantOrthogonal_JMLR2025.pdf` |
| 期刊 | **JMLR 26(29):1–35, 2025（CCF-A）** |
| 作者 | Jia He, Maggie X. Cheng |
| 正式 PDF | https://jmlr.org/papers/volume26/23-0178/23-0178.pdf |
| 开源代码 | **未见独立仓库** |
| 研究目的 | k-IGN 等变层维度随 Bell 数爆炸。给出仅 \(3(2^k-1)-k\) 个基的正交等变层，GNN-a / GNN-b 分别达到 k-WL 与 (k+1)-WL；低阶模型在分子基准上更快且不弱于已知高阶模型。 |
| 可研究性 | **高（表达力理论）**。与 01 EquivarianceEverywhere 同属等变图学习，一个偏基础模型配方，一个偏 WL 表达力降复杂度。 |
| 可复现性 | **中低**。以证明与分子实验为主，需按文中层定义自行实现。 |

---

## 5. 与研究方向的对应建议

若你的主线是 **GNN + 数据挖掘 / 大数据**，建议按下面优先级阅读：

1. **必读评测与范式**：08 FairEval → 03 GraphPFN → 01 EquivarianceEverywhere → 02 SCR  
2. **可发文章的经典 GNN 问题**：11 IGNN（同配性）→ 09 GBN（深图/过平滑）→ 10 Stable-ChebNet（长程）  
3. **大数据 / 系统**：16 IO-aware kernels → **39 Hyperion（核外 SSD）** → **37 NeutronTask（多 GPU）** → 15 ScaleGNN → **36 NeutronTP / 38 NeutronCloud / 14 Plexus**（集群与云）  
4. **LLM 交叉（热且易找应用场景）**：22 Core GraphRAG → 18 GraphRAG-R1 → 20 MemGraphRAG → **42 DesiGNN（用 LLM 设计 GNN）**  
5. **安全与鲁棒**：23 GraphRP → **41 图遗忘反演攻击** → 12 STEM-GNN  

6. **CVPR / 视觉图（CCF-A）**：24 Robo-SGG → 25 FunFact  
7. **CCF-A 期刊与 AAAI/IJCAI/SIGIR**：33 异配综述 → 35 TPAMI 稳定性 → **44 Labeling Trick（JMLR）** → **45 Implicit vs Unfolded（JMLR）** → 27 HyperSheaflets → 29 SGPC → 30 Quest-GNN → 31 PUMA  
8. **WSDM / TNNLS（数据挖掘与动态图）**：**40 GCTD** → 32 压缩综述 → **43 ScaDyG**  

相对更适合作为**学位论文核心**的切口：

- 图基础模型的可迁移表示与公平评测（01/03/08）  
- 大规模图上的算法–系统联合优化（15/16/14/**36–39**）  
- 可复现、低成本的 GraphRAG 图挖掘后端（22）  
- 同配性–泛化理论指导下的通用 GNN（11）；异配综述见 33；多节点任务理论见 44  
- 面向国内毕业要求：优先投 **CCF-A** 的 KDD/WWW/AAAI/IJCAI/CVPR/**VLDB/ICDE/SIGMOD**/TKDE/TPAMI/**JMLR**，同时跟 NeurIPS/ICML 方法前沿；WSDM / TNNLS 可作为 CCF-B 补充发表渠道  

---

## 6. 使用与更新说明

- PDF 文件名中的编号与上文一致，便于对照。  
- 会议最终版若与 arXiv 有差异，请以 DOI / proceedings 为准。  
- 代码链接来自论文正文、项目主页或作者仓库；个别仓库可能改名或后续补开源。  
- 建议引用时同时给出 **会议/期刊 + arXiv ID + DOI**。  
- 本工作区正在复现的篇目：11 IGNN、29 SGPC、40 GCTD、43 ScaDyG。入口与数字见仓库根 [`README.md`](../../README.md) 与 [`results/SUMMARY.md`](../../results/SUMMARY.md)；PDF 本身不入 git。

检索与下载时间：**2026 年 9 月 9 日**。
