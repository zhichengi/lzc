# 已开线收尾方案（2026-09-12 制定）

本文覆盖 **IGNN / ScaDyG / GCTD** 如何收尾冻结，以及工作区整理。
第四条线 **SGPC** 已按 ROADMAP 启动，不在本文任务编号里；进度见 [`SGPC_REPRO_LOG.md`](SGPC_REPRO_LOG.md)。
后续选题与标准流程见 [`REPRO_ROADMAP.md`](../REPRO_ROADMAP.md)；学习计划见 [`LEARNING_PLAN.md`](../LEARNING_PLAN.md)。
任务编号（R-IGNN-*、R-SCADYG-*、R-GCTD-*、R-WS-*）被那两份文档引用。

---

## 0. 进度快照（2026-09-13 傍晚）

| 编号 | 状态 |
|------|------|
| R-IGNN-1 … R-IGNN-4 | **完成**。public split 已冻结：Actor 37.43±0.97、roman-empire 90.64±0.40、chameleon 49.55±3.25，另顺带 pubmed / wikics。镜像脚本 `download_critical.sh` 已落地 |
| R-IGNN-5 / R-IGNN-6 | 未做（可选）。custom split 准备完成（`IGNN_CUSTOM_SPLIT.md`、`run_ignn_custom_cignn.sh`），训练未启动 |
| R-SCADYG-1 … R-SCADYG-3 | **未完成**。组件对照、消融、BitcoinAlpha 都还没有 |
| R-SCADYG-4 | **初稿完成**：`repro/SCADYG_REPORT.md`（未含消融 / 第二数据集） |
| R-SCADYG-5 | **草稿完成、未发出**：`repro/scadyg_issue_draft.md` |
| R-GCTD-1 | **完成**（2026-09-13）：Citeseer 0.9% **64.92 ± 7.72**（`lr_rec=0.01`，10 seed）与 Pubmed 0.08% **77.90 ± 1.45**（10 seed）；另有 Citeseer `lr_rec=0.001` 对照 **66.45 ± 5.09**（否证"塌缩降 lr"假设）。论文 76.8±0.4 / 79.9±0.2。汇总 `results/gctd/table2_summary.csv` |
| R-GCTD-3 | **完成**（2026-09-13）：用 GCond 官方自带压缩图（`repro/gcond/saved_ours/`，论文 Table 2 原始产物）走同一 GCTD 评测链路，Cora 1.3% **79.34 ± 0.69**（论文 GCond 79.8±1.3）、Citeseer 1.8% **69.64 ± 0.59**（70.5±1.2），均在 1σ 内 → 评测链路正确，差距在压缩/学习侧 |
| R-GCTD-4 | **收口：决定不发出**（2026-09-13）。草稿保留 `repro/gctd_issue_draft.md`；目标仓库 `nicolasrsantos/gctd` 已核实（`has_issues: true`，维护者即一作） |
| R-GCTD-5 | **完成**（2026-09-13）：冻结条目见 `REPRO_LOG.md` 文末「2026-09-13 冻结（R-GCTD-5）」。L1 是 / L2 部分 / L3 否；不再扫超参，重启需作者给出 Table 2 完整超参 |
| R-GCTD-2 | **完成**：`results/gctd/cora_summary.csv` |
| R-WS-1 | **完成**：`.gitignore` 已排除官方克隆与 PDF；GCTD 完整补丁 `gctd-repro.patch` 已生成并验证（2026-09-13）；ScaDyG 的 `eval_protocols.py` 已拷到 `repro/scadyg-extra/` |
| R-WS-2 | 未提交（大量未跟踪文件） |
| R-WS-3 | **完成**：根 README 已改为工作区说明 |
| R-WS-4 | **完成**：`results/SUMMARY.md` 已存在，含四条线 |
| R-WS-5 | **完成**：`scripts/README.md` |
| R-WS-6 | 未修 protobuf；GCTD 默认 `--no_wandb`，在 README 注明即可 |
| P4 第四篇 | **SGPC 已冻结**（2026-09-13）：9/9 数据集官方原样跑完，冻结条目见 `SGPC_REPRO_LOG.md` 文末。步骤 1–7 全部完成 |

下文第 2–5 节是制定时的原文，正文任务表只在 R-GCTD-1 上补了完成状态与数字；以本节快照为准。

---

## 1. 沿用的原则

见 `REPRO_ROADMAP.md` 第 4 节，此处不重复。

---

## 2. 优先级与理由

| 优先级 | 任务组 | 预计 GPU 时间 | 理由 |
|--------|--------|---------------|------|
| P0 | IGNN public split 收尾（3 个数据集） | < 1 小时 | 已经最接近完成；Actor 10-run 37.43 ± 0.97 与官方 38.01 ± 1.11 差 0.58，在标准差内。剩下只差数据下载和两条命令 |
| P0 | 把 IGNN Actor 正式结果写入 `IGNN_REPRO_LOG.md` | 0 | 结果已在 `results/ignn/runs/20260912T054919Z_official_actor_c_public_r10/`，日志未更新 |
| P1 | ScaDyG 消融 + 第二个数据集 + 复现报告 | 3–5 小时 | 这条线的发现（checkpoint bug、评测协议差异）最有价值，值得收成一份完整报告 |
| P2 | GCTD 收口：Citeseer / Pubmed ✅ + 外部基线对照 + 向作者求证，然后冻结 | 1–2 小时 | Citeseer/Pubmed 已完成（2026-09-13）：三格差距 15.4 / 11.9 / 2.0 点，非数据集特有；继续调参边际收益低 |
| P3 | 工作区整理：git 策略、根 README、结果汇总、大文件 | 0 | 目前只有 1 个初始提交，全部工作都是未跟踪状态，有丢失风险 |
| P4 | 第四篇论文选题与启动 | 视选题 | **已执行**：SGPC 已开，见 `SGPC_REPRO_LOG.md` |

---

## 3. 各项目具体方案

### 3.1 IGNN（P0）

**当前状态（2026-09-12 更新）**

- 环境：`/home/lab_user/tools/miniconda3/envs/ignn`（Python 3.8.16、torch 2.1.2+cu121、DGL 2.0.0+cu121）。
- **public split 已冻结**（见 `IGNN_REPRO_LOG.md` 末表）。Actor / PubMed / WikiCS 为严格 public mask。chameleon / roman-empire 因 `graph_datasets` 丢 NPZ mask，实际读的是仓库 48/32/20 npy，超参仍来自 public 脚本；数字保留，但记账时必须注明协议不纯。
- R-IGNN-1 至 R-IGNN-4 已完成。R-IGNN-5（跨 seed）不做。R-IGNN-6 升级为下面的 custom 首轮三数据集。
- custom split：**只完成准备，未训练**。清单 `repro/IGNN_CUSTOM_SPLIT.md`，排队脚本 `repro/run_ignn_custom_cignn.sh`（默认 dry-run）。

**任务**

| 编号 | 任务 | 命令 / 做法 | 验收 |
|------|------|-------------|------|
| R-IGNN-1 | Actor 结果入日志 | 在 `IGNN_REPRO_LOG.md` 追加"2026-09-12 Actor public 正式结果"条目：运行目录、命令、10 次逐次精度、均值±std、与 V100 表差值、每 run 早停 epoch | 日志有条目，与 `run.log` 数字一致 |
| R-IGNN-2 | 结束卡住的下载并改用镜像 | 先 `kill` 卡住的进程（确认 PID 命令行是 roman-empire 烟雾测试）；然后手动下载两份文件到 `repro/ignn/data/`：`roman_empire.npz`、`chameleon_filtered_directed.npz`（文件名来自 `graph_datasets/datasets/critical.py`，源为 `yandex-research/heterophilous-graphs` 提交 `a431395` 的 `data/` 目录）；用 `sha256sum` 记入日志。把镜像下载写成 `repro/download_critical.sh`，与 `download_planetoid.sh` 同风格 | `python -c "import numpy as np; np.load('data/roman_empire.npz').files"` 能列出 `node_features / node_labels / edges` |
| R-IGNN-3 | roman-empire、chameleon 烟雾测试 | 官方命令，`--n_epochs 2 --repeat 1`，标签含 `smoke` | 退出码 0 |
| R-IGNN-4 | roman-empire、chameleon 正式运行 | `scripts/00-best-racIGNN-public.sh` 第 5、3 行原样，通过 `repro/run_ignn.sh official_<ds>_c_public_r10 ...` 执行 | 两个 10-run 结果写入日志，与官方 90.75 ± 0.51、49.04 ± 4.68 对照 |
| R-IGNN-5（可选） | 硬件差异的量化 | 对 Actor 追加 `--seed` 0–4 的独立进程（每个仍 `--repeat 10` 是官方语义，不必改），看跨 seed 的均值分布是否覆盖 38.01 | 一张 seed × 均值表 |
| R-IGNN-6（可选） | custom split 一个数据集 | `scripts/01-best-cIGNN.sh` 中 Actor 一行；对照 `results/table_our.csv` 的 38.51 ± 0.94 | 一条结果 |
| R-IGNN-7 | custom 10×48/32/20 首轮三数据集 | GPU 空闲后 `IGNN_EXECUTE=1 bash repro/run_ignn_custom_cignn.sh`；c-IGNN Actor / chameleon / squirrel；对照 `table_our.csv` | 三条 10-run 写入日志；划分 SHA 未变；不搜参 |

**冻结条件（public，已满足）**：3 个 public 数据集都有 10-run 结果，且每个都写明与 V100 表的差值和作者自己承认的 V100/3090 差异（chameleon 50.79 → 47.53）。**不以"完全一致"为通过条件**。

**冻结条件（custom，待跑）**：首轮三数据集达 L2，或偏差可用 V100/3090 解释并写明；不把 public 数字改记为 custom。

**风险**：chameleon 官方 std 4.68，单次波动大，不要因为一次 45% 就去改超参。

### 3.2 ScaDyG（P1）

**当前状态**

- 四层结果已齐：官方原样（0.025，checkpoint bug）→ checkpoint-fix（seed 2023：0.9278；seeds 0–4：0.915 ± 0.009）→ MRR 选模（0.922 ± 0.014）→ 严格 full-item 协议（0.204 ± 0.004）。
- 合法二部图训练负采样对 filtered MRR 无改进（配对差 −0.0006）。
- 默认行为回归检查通过（1 epoch official MRR 逐位一致）。

**任务**

| 编号 | 任务 | 做法 | 验收 |
|------|------|------|------|
| R-SCADYG-1 | 核对消融开关 | 论文的三个组件：时间感知拓扑重构、指数时间编码、Hypernetwork 自适应聚合。CLI 目前没有直接的消融开关（`--fusion v2t` 引用不存在的文件，`--recursive_sum`、`--hop` 语义待查）。先读 `model/` 与 `transformer/` 源码，把每个组件对应到代码位置，写进日志；需要时新增 `--ablate {topo,time,hyper}`，默认关闭，保持 official 回归不变 | 日志有"组件 → 代码位置 → 开关"对照表；默认 1 epoch 仍为 0.6247271678 |
| R-SCADYG-2 | 三个消融 × seeds 0–4 | `--eval_protocol both --selection_metric mrr`，同时输出 official 与 filtered MRR；用 `repro/run_scadyg_multiseed.sh` 的方式起独立进程 | 消融表：每行 official 均值±std、filtered 均值±std；与论文消融表对照 |
| R-SCADYG-3 | 第二个数据集 | 仓库有 `process_raw_data/process_bitcoin.py` 但没有原始数据。先从镜像取 BitcoinAlpha 原始文件，重建快照并记录哈希；然后官方原样 + checkpoint-fix 各跑 seeds 0–4。注意 Bitcoin 不是二部图，`mooc_full_item` 协议不适用，只比较 official 协议 | 与论文对应数据集的 MRR 对照；日志说明协议差异 |
| R-SCADYG-4 | 复现报告 | 新建 `repro/SCADYG_REPORT.md`，结构：目标 / 环境 / 数据核验 / 官方原样结果 / 根因 1（checkpoint 只存预测层） / 根因 2（AP 选模 vs MRR 主指标） / 根因 3（排名协议：每源取最佳正边、全节点负采样、共享 RNG） / 双协议结果 / 训练负采样对照 / 未解决因素 / 结论分层 | 一份可以直接给导师看的 4–6 页报告 |
| R-SCADYG-5（可选） | 向上游反馈 | 把 `repro/scadyg-checkpoint-fix.patch` 与最小复现步骤整理成 issue 文本（先不提评测协议争议，只报确定的 bug） | issue 文本存 `repro/scadyg_issue_draft.md` |

**冻结条件**：消融表与第二个数据集结果入日志，报告初稿完成。

**风险**：消融若需要改模型代码，务必新增开关而不是改默认路径；每次改完跑一次 1 epoch 默认回归。

### 3.3 GCTD（P2）

**当前状态**

- Cora 1.3%：官方默认 30.2%（完全图）→ 单次最好 76.3%（seed 42 网格）→ 10-run 最好 66.0 ± 9.4（`dtgb`，配额+重试）；官方钉扎环境 61.0 ± 13.1；GCond 协议 58.1 ± 9.6。论文 81.4 ± 1.6。
- Citeseer 0.9%（2026-09-13）：`lr_rec=0.01` 10-run **64.92 ± 7.72**；`lr_rec=0.001` 对照 10-run **66.45 ± 5.09**。论文 76.8 ± 0.4。
- Pubmed 0.08%（2026-09-13）：10-run **77.90 ± 1.45**（10/10 先塌缩再重试到 0.001）；seed 42 单次 79.70。论文 79.9 ± 0.2。
- 已排除：环境版本、阈值形式、簇内特征、GCond 协议、小网格 R/add_ratio/lr_gnn、"未走塌缩降 lr 路径"（Citeseer 0.001 对照否证）、**评测链路本身**（GCond 官方图在 GCTD harness 上命中论文数字）。
- 未排除：官方 wandb 贝叶斯搜索得到的完整超参；`weighted` / `drop_ratio` 等与图增强相关的设定；K-Means 初始化。差距定位在**压缩/学习侧**。

**任务**

| 编号 | 任务 | 做法 | 验收 |
|------|------|------|------|
| R-GCTD-1 ✅ | Citeseer / Pubmed | `bash repro/download_planetoid.sh citeseer`、`pubmed`；用当前建议命令 `--lr_rec 0.01 --edge_topk 12`，压缩比取论文 Table 2 对应值；先 seed 42，再 seeds 0–9 | **完成 2026-09-13**：Citeseer 0.9% 64.92±7.72、Pubmed 0.08% 77.90±1.45；另加 Citeseer `lr_rec=0.001` 对照 66.45±5.09。差距**不是 Cora 特有** |
| R-GCTD-2 | Cora 实验总表 | 把 `REPRO_LOG.md` 里散落的 E/Qk/网格/10-run/环境/GCond 各表合并成 `results/gctd/cora_summary.csv`（列：设定、环境、seed 数、均值、std、单次最好、日志），并在日志末尾加"总表"条目 | 一张表能回答"我们到底试过什么" |
| R-GCTD-3 ✅ | 外部基线对照 | 用 GraphSlim 或 GC-Bench 跑 GCond 在 Cora 1.3%（论文 Table 2 里 GCond 的数字作参照）。目的不是复现 GCond，而是确认**我们的评测代码**（合成图训 GCN、原图测）在一个已知方法上能否得到公认数字 | **完成 2026-09-13**（改用更直接的方案）：GCond 官方仓库自带论文 Table 2 的压缩图产物，直接喂给 GCTD 评测链路。Cora 1.3% 79.34±0.69、Citeseer 1.8% 69.64±0.59，均命中论文 GCond 列 → 评测侧排除，差距在压缩侧。脚本 `scripts/gcond_eval_official.py` / `repro/run_gcond_eval.sh` |
| R-GCTD-4 ✅ | 向作者求证 | 整理 issue：默认 `lr_rec=0.001` 下 `to_edge_index` 的 0.05 阈值必得完全图（附诊断数字：35 点 1225 边、核值 min 0.057）；请求 Table 2 的完整超参或 wandb sweep 导出 | **收口 2026-09-13：决定不发出**。草稿含 GCond 对照证据，保留待用 |
| R-GCTD-5 ✅ | 冻结 | 在 `REPRO_LOG.md` 追加"冻结"条目：三级结论（管线闭环：是；数值量级：部分；统计一致：否）、剩余假设、重启条件 | **完成 2026-09-13**。L1 是 / L2 部分 / L3 否。issue 决定不发出，重启条件是作者给出 Table 2 完整超参 |

**冻结条件**：R-GCTD-1 到 R-GCTD-5 完成。**不再在 Cora 上继续扫超参**，除非作者给出新信息。

**风险**：GraphSlim / GC-Bench 依赖版本可能与 `gctd` 环境冲突，用新环境或 `dtgb` 试装，不要动 `gctd`。

### 3.4 工作区整理（P3）

| 编号 | 任务 | 做法 |
|------|------|------|
| R-WS-1 | git 策略 | 四个官方克隆（`repro/gctd`、`scadyg`、`ignn`、`sgpc`）各自带 `.git`，已加入根 `.gitignore`。追溯靠提交 SHA + `repro/*.patch` + 外层脚本。GCTD 完整 `gctd-repro.patch` 已生成并验证（2026-09-13）；ScaDyG 的 `model/eval_protocols.py` 已拷到 `repro/scadyg-extra/`。`results/*/runs/` 文本日志可入库（`results/gctd/runs/` 目前仍被 ignore） |
| R-WS-2 | 提交 | 先提交文档与脚本（`repro/*.md`、`repro/*.sh`、`repro/*.patch`、`scripts/`、`papers/*.md|csv|bib`），再提交结果 CSV 与日志。`papers/**/*.pdf`（117 MB）建议不入 git，或走 LFS；`papers-to-DIG.zip` 已忽略 |
| R-WS-3 | 根 README | **已做**（2026-09-12）：工作区定位、四个 conda 环境、四条线入口与一句话结论、骨架目录说明 |
| R-WS-4 | 顶层结果汇总 | **已做**：`results/SUMMARY.md` |
| R-WS-5 | 环境清单 | **已做**：`scripts/README.md` |
| R-WS-6 | 小修 | `dtgb` 里 wandb 降级 protobuf 与 tensorboard 冲突（GCTD 日志待办）：GCTD 已默认 `--no_wandb`，可以直接 `pip uninstall wandb` 后把 protobuf 升回，或干脆不管并在 README 注明 |

### 3.5 下一篇论文

选题准则、完整复现队列（下一篇为 09 GBN；29 SGPC 已开工）与标准十一步流程见根目录 `REPRO_ROADMAP.md` 第 2–4 节，此处不再单列。

---

## 4. 收尾时间表

与 `LEARNING_PLAN.md` 的 P0 阶段（第 1–3 周）对应；收尾任务穿插在下一篇论文的等待时间里完成。

| 时间 | 里程碑 | 对应任务 |
|------|--------|----------|
| 第 1 周 | IGNN public split 三数据集冻结；开始 SGPC 步骤 1–3 | R-IGNN-1 至 R-IGNN-4 |
| 第 2 周 | ScaDyG 消融表；ScaDyG 第二数据集 | R-SCADYG-1 至 R-SCADYG-3 |
| 第 3 周 | ScaDyG 报告初稿；GCTD Citeseer / Pubmed + 总表 + 外部对照 + issue + 冻结 | R-SCADYG-4、R-GCTD-1 至 R-GCTD-5 |
| 贯穿 | 仓库可提交、顶层汇总 | R-WS-1 至 R-WS-6 |

GPU 排队顺序：IGNN（分钟级）→ ScaDyG 消融（每次 5–10 分钟，15 次约 2 小时）→ GCTD 多 seed（每次 1 分钟）→ ScaDyG 第二数据集。

---

## 5. 四条线的当前判定（按 `REPRO_ROADMAP.md` 第 5 节的三级标准）

| 线 | 冻结状态 | L1 | L2 | L3 |
|----|----------|----|----|----|
| 11 IGNN | **已冻结**（public；custom 不在范围） | 是 | 是 | 是* |
| 40 GCTD | **已冻结**（2026-09-13） | 是 | 部分 | 否 |
| 29 SGPC | **已冻结**（2026-09-13） | 是 | 部分 | 否 |
| 43 ScaDyG | **未冻结**，冻结条件是消融表 + 第二数据集入日志 | 是 | 是 | 否 |

- GCTD：L2 部分（Cora 66.0 ± 9.4、Citeseer 64.9 ± 7.7、Pubmed 77.9 ± 1.5，对论文 81.4 ± 1.6 / 76.8 ± 0.4 / 79.9 ± 0.2；只有 Pubmed 接近）；L3 否（σ 普遍大一个数量级）。评测链路已由 GCond 官方图验证，差距在压缩侧。issue 决定不发出。
- SGPC：L2 部分（oracle 在 6 个数据集上与论文差 0.4–1.2 点；val 选模系统性偏低 0.07–3.43；Wisconsin 偏高 +2.43/+6.35）；L3 否（协议不同：异配用 geom-gcn 10 划分而非"每类 20 点"；σ 为论文 2–5 倍）。冻结条目见 `SGPC_REPRO_LOG.md` 文末。
- IGNN public：L2 是；L3 在 Actor / wikics 上按「均值差 < 官方 σ」成立（硬件 3090 vs V100）。chameleon / roman-empire 的 public 命令因加载器丢 NPZ mask，实际读的是仓库 48/32/20 npy，协议不纯，数字仍与 V100 表同量级。custom split 未跑，不在冻结范围。
- ScaDyG：L2 是（0.922 ± 0.014 对 0.931 ± 0.009）；L3 否（方差偏大，且发现协议差异）。完成消融与 BitcoinAlpha 后才能冻结。

\* IGNN 的 L3 只在 Actor / wikics 成立，且硬件跨卡（3090 vs V100），作者自述存在差异。

---

## 6. 2026-09-12 整库审核（不训练）

### 四条线

| 线 | 该停 / 该做 | 主要风险 |
|----|-------------|----------|
| IGNN | **已冻结**（public）。下一步 custom 三数据集（可选）。不要补跑"真 public"、不要搜参、不要大图 | critical public 协议不纯；`run_ignn.sh` 现含 85% cap，与提交 `7adde1c` 的无 cap 版本不一致 |
| ScaDyG | **未冻结**：缺消融（R-SCADYG-1/2）、BitcoinAlpha（R-SCADYG-3）；报告初稿已有 | checkpoint 只存预测层已确认；严格 item 协议 ~0.204 不要和官方 MRR 混排 |
| GCTD | **已冻结**（2026-09-13）。不要重扫 Cora；重启条件是作者给出 Table 2 完整超参 | 官方默认完全图；三格 66.0±9.4 / 64.9±7.7 / 77.9±1.5 均低于论文，差距非数据集特有；评测链路已由 GCond 官方图验证正确 |
| SGPC | **已冻结**（2026-09-13，9/9 数据集）。不要补跑 seed 或重做划分 | 论文写每类 20 点，代码用 PyG 自带 split；`Best Test` 是 test 选模，不可当 Table 1 数字；∆t 代码 0.15 vs 论文 0.5 |

### 仓库

- 根 `README.md`、`repro/README.md`、`scripts/README.md`、`results/SUMMARY.md` 已按四条线现状改写（R-WS-3/4/5）。`main.py` / `configs/example.yaml` / `src/` 仍是空壳，README 已标明不用。
- `.gitignore` 排除官方克隆、论文 PDF、数据与缓存。GCTD 完整 `gctd-repro.patch` 已生成并验证；ScaDyG `eval_protocols.py` 已拷到 `repro/scadyg-extra/`（2026-09-13）。
- 已跟踪提交主要是早期 IGNN public（到 WikiCS）与骨架文件。未入库：chameleon/roman 正式结果、capped 脚本、custom 准备、GCTD/ScaDyG/SGPC 文档与产物。需要一次文档+脚本提交（R-WS-2），未要求时不 commit。
- `IGNN_REPRO_LOG.md` 有重复段落（Actor / roman / chameleon 写了两遍）；只追加、不改写历史。
- conda：`dtgb` / `gctd` / `scadyg` / `ignn` 隔离，不要混装。GitHub 直连常超时，走镜像。
- 长任务走 85% cap（`scripts/capped_env.sh`）。CUDA MPS 可能残留，custom / SGPC 前确认只跑一个训练进程。

### 现在不要做

- 启动 IGNN custom 训练（等用户确认 GPU 空闲）。
- 把 49.55 / 90.64 当成 custom。
- 修 `graph_datasets` 再重跑 public。
- 开 30 基线、Optuna、arxiv/products/pokec。
- 把嵌套 `.git` 打进根仓库。
- 未要求时 commit / push。
