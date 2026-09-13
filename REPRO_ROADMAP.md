# 论文复现方案：选题准则、复现队列与标准流程

> 本文回答三个问题：**下一篇复现什么**（第 2、3 节）、**每一篇怎么做**（第 4 节）、**什么时候算做完 / 什么时候停**（第 5、6 节）。
> 学习内容与时间线见 [`LEARNING_PLAN.md`](LEARNING_PLAN.md)；已开线的收尾细节见 [`repro/CLOSEOUT_PLAN.md`](repro/CLOSEOUT_PLAN.md)。
> 顶层数字见 [`results/SUMMARY.md`](results/SUMMARY.md)；工作区入口见 [`README.md`](README.md)。

---

## 1. 硬件与环境约束

所有选题与流程都受以下条件限制，不要选超出条件的论文：

| 条件 | 现状 | 对选题的影响 |
|------|------|--------------|
| GPU | 单张 RTX 3090，24 GB | 排除多 GPU / 集群系统类论文（14、17、36–39）；十亿级预训练（03 预训练、06）只能做下游评测 |
| 内存 / 磁盘 | 60 GB / 726 GB 可用 | ogbn-papers100M 需 memmap，可做但要预留时间；其余公开数据集无压力 |
| 网络 | GitHub 直连超时，`ghfast.top` 镜像可用；PyPI 用清华源 | 所有克隆与数据下载走镜像；下载后核对哈希 / 提交 SHA |
| LLM API | 暂无预算 | GraphRAG 类（18–22、30、42）只复现不依赖 LLM 的算法部分 |
| conda 环境 | `dtgb`（torch 2.2.1+cu121，PyG 2.8，DGL 2.2.1）、`gctd`、`scadyg`、`ignn` | 新论文优先复用 `dtgb`；版本差距大时新建独立环境，命名 `<论文简称小写>` |
| 资源上限 | 用户态 85%（CPUQuota / 内存 / 显存 fraction / GPU 占空比）；无 root 不能钉功耗 | 长任务走 `scripts/run_capped.sh`；同一时刻只跑一个训练进程 |

---

## 2. 选题准则

从 `papers/gnn-frontier-2025-2026/papers_index.csv` 筛选，按以下顺序过滤：

1. **可复现性评级为"高"或"中高"**（`reproducibility` 列），且官方代码链接有效。
2. **单卡一小时内能跑完一组主表实验**（至少一个数据集的完整多 seed）。
3. **数据公开且可镜像下载**：Planetoid、critical 异配集、OGB、LRGB、TU 数据集都可以；工业数据、需申请的数据不选。
4. **与主线相关**：主线是 GNN + 数据挖掘 / 图压缩 / 大规模训练（见论文库 README 第 5 节）。同配性 / 深层 GNN、图压缩、可扩展、动态图、链接预测为核心；GFM、安全、GraphRAG 为扩展。
5. **知识依赖已满足**：`LEARNING_PLAN.md` 对应模块的前置模块已完成检验。

被过滤掉的论文不是不读，而是进入"只读"清单（第 3.4 节）。

---

## 3. 复现队列

### 3.1 进行中

| 编号 | 论文 | 状态（2026-09-12） | 下一步 |
|------|------|--------------------|--------|
| 29 | SGPC（AAAI 2026） | 步骤 1–6 完成：8/9 数据集官方原样单次已跑，Pubmed 未跑 | **当前主线**：步骤 7 划分遍历、val 选模、Pubmed。入口 [`repro/SGPC_README.md`](repro/SGPC_README.md) |
| 11 | IGNN（NeurIPS 2025） | public split 已冻结；custom 48/32/20 只完成准备 | GPU 空闲后按 [`repro/IGNN_CUSTOM_SPLIT.md`](repro/IGNN_CUSTOM_SPLIT.md) 跑；不改已冻结 public 表 |
| 43 | ScaDyG（TNNLS 2026） | 官方协议 0.922 ± 0.014 vs 0.931 ± 0.009；严格协议 0.204 | 三个消融；BitcoinAlpha；写 `repro/SCADYG_REPORT.md`；冻结 |
| 40 | GCTD（WSDM 2026） | Cora 10-run 66.0 ± 9.4 vs 81.4 ± 1.6 | Citeseer / Pubmed；GCond 对照；向作者提 issue；冻结，**不再扫参** |

收尾任务编号见 [`repro/CLOSEOUT_PLAN.md`](repro/CLOSEOUT_PLAN.md)。GPU 只有一张：**不要并行开第五篇**；SGPC 等待时间里穿插三条线的收尾。

### 3.2 队列（SGPC 之后按顺序，每篇 1–2 周）

| 序 | 编号 | 论文 | 会议 | 为什么排在这里 | 主表实验（单卡预估） | 环境 | 学习模块 |
|----|------|------|------|----------------|----------------------|------|----------|
| 1 | 09 | GBN：Riemannian geometry 对抗过平滑 / 过挤压 | NeurIPS 2025 | 可复现性高；小图（WikiCS、Texas 等）；补"深层 GNN"这一块，与 35 TPAMI 理论对照 | 深度 64–256 层，单数据集 10–30 分钟 | `dtgb` | M1 |
| 2 | 10 | Stable-ChebNet：长程任务上的谱方法 | NeurIPS 2025 Spotlight | 可复现性高；进入图级任务与 LRGB；谱滤波知识承接 SGPC | Peptides-func / struct 各约 1–3 小时 | 视 PyG 版本，可能新建 `chebnet` | M1、M5 |
| 3 | 31 | PUMA：持续图学习 + 图压缩 | TKDE 2025 | 可复现性高；直接复用 GCTD 积累的图压缩知识；把"压缩"从静态扩到流式 | 节点分类流式任务，单数据集小时级 | 新建 `puma` | M2 |
| 4 | 15 | ScaleGNN：自适应高阶邻居融合 | WWW 2026 | 可复现性中高；ogbn-arxiv 单卡可做；补"大规模"主线；预传播思想与 ScaDyG 同源 | ogbn-arxiv 10 seed 约 1 小时；products 视内存 | `dtgb` | M3 |
| 5 | 44 | Labeling Trick | JMLR 2025 | 可复现性高；进入链接预测；理论清楚，是 SEAL 系方法的统一 | LinkPred 子仓库，Cora / Citeseer / Pubmed 分钟级 | `dtgb` | M5 |
| 6 | 13 | MAVN：自适应虚拟节点 | KDD 2026 | GitHub + Zenodo 双备份；图级任务；与 Stable-ChebNet 在 LRGB 上对照 | 图分类数据集小时级 | 视依赖 | M5 |
| 7 | 08 | Fair Evaluation of GFMs | ICML 2026 Workshop | 评测框架；先把框架跑起来，再把 IGNN / SGPC 接进去当 baseline | 框架自带数据集与模型链接，按需选子集 | 新建 `gfm` | M6 |
| 8 | 01 或 04 | EquivarianceEverywhere / MF-GIA | NeurIPS 2025 / ICLR 2026 | 两篇都可复现性高、单卡（01 用 L40 单卡）；选一篇进入 GFM 方法 | 节点分类迁移任务，小时级 | `gfm` | M6 |
| 9 | 23 或 41 | GraphRP / Unlearning Inversion | KDD 2026 / WSDM 2026 | 可复现性高，标准小图；进入安全主题，两篇构成攻防对照 | 分钟到小时级 | `dtgb` | M7 |
| 10 | 12 | STEM-GNN：Tokenized MoE | KDD 2026 | 可复现性高；节点 / 边 / 图三类任务 | 视任务 | 视依赖 | M7 |
| 11 | 22 | Core-based Hierarchies for GraphRAG | KDD 2026 | 只复现 k-core 层次构建与"Leiden 不可复现"的验证；LLM 评测等预算 | CPU 即可 | `dtgb` | M8 |

### 3.3 条件成熟后再做

| 编号 | 论文 | 条件 |
|------|------|------|
| 03 | GraphPFN | 只做作者发布 checkpoint 的微调 / ICL 评测；预训练不做 |
| 16 | IO-aware GNN kernels | 需要 CUDA / Triton 基础；单卡可以做速度与显存对比，属于系统方向可选 |
| 02、05 | SCR、AnyGraph | 38 数据集全量复现工作量大；先做子集 |
| 30、20、18 | Quest-GNN、MemGraphRAG、GraphRAG-R1 | 需要 LLM API 或本地大模型 |
| 34 | 熵视角过平滑（图分类） | 可复现性高，但与 09 GBN 主题重叠；作为 P1 阶段的备选 |

### 3.4 只读不复现

- 系统 / 集群：14 Plexus、17 4D 并行、36 NeutronTP、37 NeutronTask、38 NeutronCloud、39 Hyperion
- 工业规模无代码：06 GraphBFF
- 无公开代码：07 SPG、26 GraPHFormer、27 HyperSheaflets、28 HyperNoRA、46 正交等变基
- 理论 / 综述：32 图压缩综述、33 异配综述、35 TPAMI 稳定性、45 Implicit vs Unfolded
- 依赖 GPT-4 API：42 DesiGNN、21 GraphRAG-Router
- 视觉图（偏离主线）：24 Robo-SGG、25 FunFact

### 3.5 队列调整规则

- 队列顺序服从 `LEARNING_PLAN.md` 的模块依赖；同一模块内可按兴趣换序。
- 一篇论文在标准流程第 6 步（官方原样）就失败且两天内定位不出原因，先冻结、记录，跳到下一篇；不要像 GCTD 那样连续投入多天调参。
- 新进论文库的论文，先按第 2 节准则打分，再插入队列，同时更新 `papers_index.csv`。

---

## 4. 标准复现流程

每一篇都走同样 11 步，每步在 `repro/<NAME>_REPRO_LOG.md` 留一条时间戳条目。模板见 [`repro/_TEMPLATE_REPRO_LOG.md`](repro/_TEMPLATE_REPRO_LOG.md)。

### 4.1 目录与命名约定

```
repro/
├── <name>/                      # 官方仓库克隆（自带 .git，不入根仓库；见 4.3）
├── <NAME>_REPRO_LOG.md          # 过程日志，只追加（GCTD 历史文件名是 `REPRO_LOG.md`）
├── <NAME>_README.md             # 入口说明：环境、命令、当前结论一句话
├── run_<name>.sh                # 入口脚本：固定 cwd、GPU、日志路径；记录提交与补丁哈希
├── run_<name>_multiseed.sh      # 多 seed 独立进程
├── <name>-*.patch               # 对官方代码的改动，能 git apply
└── diagnose_<name>_*.py         # 诊断脚本（可选）
scripts/setup_<name>_conda.sh    # 环境安装脚本
results/<name>/runs/             # 每次运行的文本日志（可入 git）
results/<name>/*.csv             # 结构化汇总
results/<name>/checkpoints/      # 权重（不入 git）
paper/notes/<编号>_<name>.md      # 读书笔记（LEARNING_PLAN 6.1 模板）
```

### 4.2 十一步

| 步 | 做什么 | 产出 / 记录 | 常见坑（来自已开四条线） |
|----|--------|-------------|--------------------------|
| 1 固定源码 | 镜像克隆；记录提交 SHA；与 GitHub API 返回的默认分支 SHA 比对 | 日志"源码固定"条目 | 直连超时；仓库可能只有一个提交，之后作者推送会改变结果 |
| 2 环境隔离 | 优先 `dtgb`；版本差距大则新建；`pip check` 无冲突；记录 torch / CUDA / PyG / DGL / GPU | `scripts/setup_<name>_conda.sh` | 官方 `requirements.txt` 常是整机导出（ScaDyG）；DGL wheel 需要系统 CUDA runtime（IGNN） |
| 3 数据核验 | 镜像下载；能重建就重建并逐元素比对；记录 SHA-256 | `repro/download_<name>.sh` | PyG 数据目录名大小写（`cora` 不是 `Cora`）；`graph_datasets` 直连 GitHub |
| 4 代码审计 | 读入口与训练循环，列"运行前发现的问题"：cwd 依赖、写死 GPU、无条件 wandb、seed 位置、选模指标 vs 论文主指标、checkpoint 覆盖范围、负采样、README 与实现不一致 | 日志"审计"条目，**只记录不改** | ScaDyG 只存一半 checkpoint；GCTD 无条件 `wandb.login()`；SGPC 用 test 选模且无 seed；`--repeat` 重复同一 seed |
| 5 烟雾测试 | 1–2 epoch，`repeat=1`，标签含 `smoke` | 退出码 0 | 不要拿烟雾数字和论文比 |
| 6 官方原样 | 默认命令完整跑一次 | 基线数字，无论多离谱原样记录 | GCTD 默认 30%、ScaDyG 默认 0.025、SGPC 的 `Best Test` 都是这一步发现的 |
| 7 定位失配 | 归类：超参未公开 / 代码 bug / 硬件与环境 / 协议与论文文字不一致；写诊断脚本 | `diagnose_<name>_*.py` + 日志 | 先看合成物（GCTD 的合成图密度）、再看选模与 checkpoint（ScaDyG）、最后才怀疑环境（IGNN） |
| 8 修正版 | 每个修正一个 CLI 开关，默认关闭；改完跑一次默认 1 epoch 回归，数字须逐位一致 | `.patch` 文件 + 补丁 SHA-256 | 不要改默认路径；修正版与原样结果永远分表 |
| 9 多 seed | 独立进程，seeds 0–4（快）或 0–9（慢）；报告样本标准差 | `results/<name>/*_multiseed_summary.csv` | 不用官方 `--repeat`；早停 epoch 不同会改变评测随机数消耗（ScaDyG） |
| 10 分层结论 | L1 管线闭环 / L2 数值量级 / L3 统计一致，分别回答是或否 | 日志"结论"条目 | 不要把 L1 说成 L3 |
| 11 冻结 | 写剩余假设、停止理由、给作者的 issue 草稿（若有确定 bug） | 日志"冻结"条目；`results/SUMMARY.md` 更新；`paper/notes/` 定稿 | 冻结后除作者回复外不再回头 |

### 4.3 版本管理

- 官方克隆目录自带 `.git`，加入根 `.gitignore`；根仓库通过"提交 SHA + `.patch` 文件 + 新增文件副本"追溯改动。
- 新增的未跟踪源码文件（如 ScaDyG 的 `model/eval_protocols.py`）要复制到 `repro/<name>-extra/` 纳入根仓库，并在日志里记 SHA-256。
- 每篇论文冻结时至少一次 `git commit`，提交信息形如 `repro(<name>): freeze, L2 reached, see <NAME>_REPRO_LOG.md`。
- `results/*/runs/` 文本日志入库；`*.pt` / `*.pth` / 数据 / 缓存不入库；`papers/**/*.pdf` 不入库或走 LFS。

---

## 5. "复现完成"的三级判定

| 层级 | 含义 | 判定 |
|------|------|------|
| L1 管线闭环 | 数据、训练、评测、日志全部可运行，结果可重跑 | 退出码 0；同 seed 重跑数字一致 |
| L2 数值量级 | 修正版在官方评测协议下落入论文报告区间，或差距能被已确认的失配类型解释 | 单次或均值落入 \([\mu - \sigma, \mu + \sigma]\)，或差距有明确归因 |
| L3 统计一致 | 多 seed 均值与标准差都与论文相当 | 均值差小于论文 \(\sigma\)，且我们的 \(\sigma\) 与论文同量级 |

达到 L2 并写清 L3 未达到的原因即可冻结。三级里最有价值的往往不是 L3，而是第 7 步定位出的失配原因——那是能写进报告、能向作者反馈、能变成自己研究切口的东西。

---

## 6. 时间盒与冻结规则

| 情形 | 上限 | 到期动作 |
|------|------|----------|
| 步骤 1–5（环境到烟雾） | 2 个工作日 | 超时记录阻塞点（通常是依赖或下载），跳下一篇，回头再补 |
| 步骤 6–7（原样到定位） | 3 个工作日 | 定位不出就冻结在 L1，写清怀疑方向 |
| 步骤 8–9（修正到多 seed） | 3 个工作日 | 不再扫超参；有多少写多少 |
| 整篇 | 2 周 | 无条件冻结 |

GCTD 是反例：从 09-10 到现在在 Cora 上做了约 15 轮实验仍未到 L3。按本规则应在第 4 天冻结并转向 Citeseer / Pubmed 与外部对照。

---

## 7. 现在开始的第一步

预处理（克隆、审计、烟雾入口、全量 dry-run）已按篇独立落地，总表 [`repro/PREP_STATUS.md`](repro/PREP_STATUS.md)。之后想复现哪篇，打开该篇 README，用 `FULL=1 bash repro/run_<name>_full.sh`，不要再从零搭环境。

1. **SGPC 步骤 7 收尾**（当前主线训练）：Squirrel / Actor 10 划分。入口 [`repro/run_sgpc_full.sh`](repro/run_sgpc_full.sh)（默认不跑）。
2. 继续 `LEARNING_PLAN.md` 的 M0 / M1。
3. GPU 空闲：IGNN custom（`bash repro/run_ignn_full.sh`）；ScaDyG / GCTD 用各自 `run_*_full.sh`。
4. 下一篇新训练按队列是 **09 GBN**，但必须等 SGPC 冻结后再 `FULL=1`。GraphRP（23）源码未发布，跳过。
