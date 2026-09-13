# papers 论文库说明

本目录是工作区里的论文库副本入口。当前只有一套专题：

| 子目录 | 内容 | 规模 |
|--------|------|------|
| [`gnn-frontier-2025-2026/`](gnn-frontier-2025-2026/) | 图神经网络 / 图基础模型 / 大规模图学习 / GraphRAG / 数据挖掘系统（2025–2026） | 46 篇 PDF，约 117 MB |

检索日期：**2026-09-09**。PDF 来自 arXiv、会议开放页面与作者主页，仅供个人学习与科研。

## 说明文件（请一起保留）

同步到其他磁盘时，**不要只拷 PDF**。下列文件是阅读、筛选和写作用的索引：

| 文件 | 用途 |
|------|------|
| 本文件 `papers/README.md` | 整库入口 |
| `gnn-frontier-2025-2026/README.md` | **主说明**：每篇论文的来源、研究目的、可研究性、可复现性、代码链接与阅读顺序 |
| `gnn-frontier-2025-2026/papers_index.csv` | Excel / WPS 可筛选的一览表（venue、arxiv、DOI、代码、评级） |
| `gnn-frontier-2025-2026/papers.bib` | LaTeX / Zotero / JabRef 引用库 |

在 Windows 资源管理器中可先打开 CSV；完整评注请用 VS Code / Typora / Cursor 打开 Markdown。

## 目录结构

```
papers/
├── README.md
└── gnn-frontier-2025-2026/
    ├── README.md
    ├── papers_index.csv
    ├── papers.bib
    ├── 01-graph-foundation-models/
    ├── 02-gnn-architecture-theory/
    ├── 03-scalable-bigdata-gnn/
    ├── 04-graphrag-llm/
    ├── 05-data-mining-security/
    ├── 06-cvpr-vision-graph/
    ├── 07-ccf-aaai-ijcai-sigir/
    ├── 08-ccf-journals/
    ├── 09-db-systems-sigmod-vldb-icde/
    ├── 10-wsdm/
    └── 11-journals-tnnls-jmlr/
```

工作区中与本专题直接相关的复现不在本目录，而在 `repro/`：

| 编号 | 论文 | 目录 |
|------|------|------|
| 11 | IGNN | `repro/ignn/` |
| 29 | SGPC | `repro/sgpc/` |
| 40 | GCTD | `repro/gctd/` |
| 43 | ScaDyG | `repro/scadyg/` |

入口与数字：[根 README](../README.md)、[results/SUMMARY.md](../results/SUMMARY.md)。

## 建议再补的材料（按优先级）

当前 46 篇已经覆盖方法、系统、CCF-A/B 主会与期刊。若你的主线是 **GNN + 数据挖掘 / 图压缩（GCTD）+ 大规模训练**，建议按下面补，而不是把所有顶会图论文再扫一遍。

1. **图压缩对照实验集（立刻有用）**  
   你已经在复现 GCTD。应补齐可跑的基线 PDF + 代码入口：GCond / DosCond / SFGC、GC-Bench 或 GraphSlim，以及 WSDM 2026 的 **DGC**（离散域压缩，与 GCTD 同场；本次因付费墙未入库）。写 related work 和实验表时这些是刚需。
2. **付费墙漏网（有校园网 / ACM 账号再下）**  
   SIGMOD/PACMMOD 的 **NeutronHeter**（异构集群分布式 GNN）、IJCAI 2026 论文集一旦上线。这两处 README 里已点名。
3. **动态图再补 2–3 篇**  
   现在只有 ScaDyG。若题目会碰到时序/流图，补 TGB 基准论文 + 一篇近期可扩展动态 GNN（与 43 对照即可），不必做成新专题。
4. **引用库用法**  
   用 `papers.bib` 导入 Zotero / JabRef，以后新 PDF 先改 CSV 再补 bib，避免只在磁盘堆文件。作者列表来自论文首页，个别 “et al.” 条目写 related work 前请核对正式 PDF。
5. **不要整库拷代码**  
   PDF + 说明足够备份。只把你真正要复现的仓库放到 `repro/`（现有 IGNN / SGPC / GCTD / ScaDyG 即此模式）。十几个 GitHub 全 clone 会迅速把磁盘撑乱且难以更新。
