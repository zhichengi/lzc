# GNN 论文库与复现工作区

本仓库做两件事：收藏 2025–2026 图神经网络相关论文，并按统一流程复现其中可单卡跑通的若干篇。
机器约束是单张 RTX 3090（24 GB）、约 60 GB 内存；GitHub 直连会超时，克隆与数据一律走镜像。

数字总表：[results/SUMMARY.md](results/SUMMARY.md)。判定标准（L1 管线闭环 / L2 数值量级 / L3 统计一致）见 [REPRO_ROADMAP.md](REPRO_ROADMAP.md) 第 5 节。

## 当前复现线（2026-09-16）

| 编号 | 论文 | 入口 | 当前结论 | 状态 |
|------|------|------|----------|------|
| 09 | GBN（NeurIPS 2025） | [repro/GBN_README.md](repro/GBN_README.md) | 主表 7 项中 4 项在论文 1σ 内（CS 95.80 vs 95.78）；消融 4/16 在 1σ 内 | **已完成，可冻结** |
| 11 | IGNN（NeurIPS 2025） | [repro/IGNN_README.md](repro/IGNN_README.md) | public（Actor 37.43 vs 38.01）与 custom 48/32/20 首轮三数据集均 < 1σ | **已冻结**（public + custom） |
| 43 | ScaDyG（TNNLS 2026） | [repro/SCADYG_README.md](repro/SCADYG_README.md) | 官方协议 0.922 ± 0.014 vs 论文 0.931 ± 0.009；严格 item 0.204 ± 0.004；BitcoinAlpha 0.719470 ± 0.006932 | **可冻结**；报告与完整补丁已收口 |
| 40 | GCTD（WSDM 2026） | [repro/GCTD_README.md](repro/GCTD_README.md) | Cora 1.3% 官方默认 30%；修正后 10-run 66.0 ± 9.4 vs 81.4 ± 1.6 | **已冻结**；不再在 Cora 上扫参 |
| 29 | SGPC（AAAI 2026） | [repro/SGPC_README.md](repro/SGPC_README.md) | 9/9 数据集官方原样已跑；val 选模系统性偏低 0.07–3.43 | **已冻结** |

队列里尚未全量训练的论文已经**按篇做完预处理**（独立克隆、审计、烟雾入口、全量 dry-run），总表：[repro/PREP_STATUS.md](repro/PREP_STATUS.md)。四条收尾线（IGNN / ScaDyG / GCTD / SGPC）＋ GBN 均已收口；按队列下一篇新训练是 **10 Stable-ChebNet**，仍是单卡串行、不要并行开两篇。收尾细节见 [repro/CLOSEOUT_PLAN.md](repro/CLOSEOUT_PLAN.md)。

## 计划与论文库

- [LEARNING_PLAN.md](LEARNING_PLAN.md)：边复现边学的知识模块与阶段时间线
- [REPRO_ROADMAP.md](REPRO_ROADMAP.md)：选题准则、复现队列、标准十一 步与冻结规则
- [repro/CLOSEOUT_PLAN.md](repro/CLOSEOUT_PLAN.md)：已开线的收尾任务与完成情况
- [papers/gnn-frontier-2025-2026/README.md](papers/gnn-frontier-2025-2026/README.md)：46 篇论文的评级与索引
- [paper/notes/](paper/notes/)：正在复现的论文的读书笔记

新开一篇时复制 [repro/_TEMPLATE_REPRO_LOG.md](repro/_TEMPLATE_REPRO_LOG.md)，官方代码放 `repro/<name>/`，日志放 `results/<name>/runs/`。队列论文的预处理入口见 [repro/PREP_STATUS.md](repro/PREP_STATUS.md)；全量默认 `FULL=0`。

## 环境

四个独立 conda 环境，互不覆盖。入口脚本会自己 `conda activate`。

| 环境 | Python | 主要栈 | 用途 |
|------|--------|--------|------|
| `dtgb` | 3.10 | torch 2.2.1+cu121，PyG 2.8，DGL 2.2.1 | 工作区默认；**SGPC** 用它 |
| `gctd` | 3.11 | torch 2.1.2+cu121，PyG 2.6.1 | GCTD 官方钉扎（对照仍可用 `dtgb`） |
| `scadyg` | 3.10 | 从 `dtgb` 克隆，另装 deepsnap / py-tgb | ScaDyG |
| `ignn` | 3.8 | torch 2.1.2+cu121，PyG 2.4.0，DGL 2.0.0 | IGNN（含环境内 CUDA 12.1 runtime） |

```bash
# 只在对应环境缺失时运行，不要交叉安装
bash scripts/setup_env.sh              # dtgb
bash scripts/setup_gctd_conda.sh       # gctd 钉扎环境
bash scripts/setup_gctd_env.sh         # 仅向 dtgb 补 GCTD 缺的包
bash scripts/setup_scadyg_conda.sh     # scadyg
# IGNN 环境已存在于 /home/lab_user/tools/miniconda3/envs/ignn，无单独 setup 脚本
```

长任务默认走 85% 资源上限（CPU / 内存 / 显存 / GPU 占空比），见 [scripts/README.md](scripts/README.md)。无 root，不能用 `nvidia-smi -pl` 钉功耗。

## 目录

```
├── README.md                 # 本文件
├── LEARNING_PLAN.md          # 学习计划
├── REPRO_ROADMAP.md          # 复现队列与流程
├── papers/                   # 论文库（PDF 不入 git；索引 md/csv/bib 入库）
├── paper/notes/              # 读书笔记
├── repro/                    # 复现入口、日志、补丁、官方克隆
│   ├── README.md             # 四条线总入口
│   ├── <NAME>_README.md      # 单篇怎么跑
│   ├── <NAME>_REPRO_LOG.md   # 过程日志（只追加）
│   └── <name>/               # 官方仓库（自带 .git，不入根仓库）
├── results/                  # 运行产物
│   ├── SUMMARY.md            # 顶层数字
│   └── <name>/runs/          # 文本日志（可入库）
├── scripts/                  # 环境安装、限额、解析
├── configs/ example.yaml     # 仓库骨架，当前复现线不用
├── main.py / src/ / tests/   # 同上，预留空壳
├── data/ raw|processed       # 骨架数据目录，当前数据在 repro/<name>/
└── requirements.txt          # 对应 dtgb；实际安装用 scripts/setup_env.sh
```

官方克隆目录带独立 `.git`，根仓库用「提交 SHA + `repro/*.patch` + 外层脚本」追溯，不要 `git add repro/gctd` 这类路径。

## 不要做的事

- 不要对 GCTD 的 Cora 继续扫超参。
- 不要把 IGNN chameleon / roman-empire 的 public 数字当成 custom split 结果。
- 不要把 SGPC 单次、划分 0 的数字写成 Table 1 的统计复现。
- 不要让 PyG / `graph_datasets` 直连 GitHub；用 `repro/download_*.sh` 或镜像脚本。
- 不要用根目录 `python main.py --config configs/example.yaml` 跑论文实验，那只是空壳。
