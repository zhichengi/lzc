# 论文预处理总表（互不混淆）

本文件只做**索引**。每篇论文的命令、SHA、审计、烟雾与全量入口都在该篇自己的 `repro/<NAME>_README.md` 和 `repro/<NAME>_REPRO_LOG.md`。
不要把数字抄到别的论文日志里。全量默认 **dry-run**：`FULL=1 bash repro/run_<name>_full.sh` 才会训练。

预处理日期：2026-09-12（各篇状态更新至 2026-09-16）。克隆一律 `ghfast.top`，SHA 已与 `git ls-remote HEAD` 比对。

## 怎么开一篇

1. 打开该篇 README。  
2. 需要时跑该篇 `download_*.sh` / `scripts/setup_*.sh`（不要交叉 `pip` 进别的 conda）。  
3. 先烟雾，确认退出码 0。  
4. GPU 空闲且没有其它训练时：`FULL=1 bash repro/run_<name>_full.sh`。  
5. 同一时刻只占一张 GPU。

登记表：[`PREP_REGISTRY.tsv`](PREP_REGISTRY.tsv)。克隆：`bash scripts/clone_official_repo.sh NAME owner/repo`。

## 已开四条线（收尾，不是新开）

| 编号 | 论文 | README | 全量入口（默认不跑） | 预处理要点 |
|------|------|--------|----------------------|------------|
| 29 | SGPC | [SGPC_README.md](SGPC_README.md) | `repro/run_sgpc_full.sh` | 6 个异配集 ×10 划分完成（含 Actor）；Cora/Citeseer 5 seed |
| 11 | IGNN | [IGNN_README.md](IGNN_README.md) | `repro/run_ignn_full.sh` → custom dry-run | public 已冻结，勿改表 |
| 43 | ScaDyG | [SCADYG_README.md](SCADYG_README.md) | `repro/run_scadyg_full.sh` | 消融与 BitcoinAlpha 已完成（0.719470 ± 0.006932）；可冻结 |
| 40 | GCTD | [GCTD_README.md](GCTD_README.md) | `repro/run_gctd_full.sh` | Citeseer/Pubmed；禁止再扫 Cora |

## 队列论文（各自独立目录）

| 序 | 编号 | 简称 | SHA（12 位） | conda 计划 | 烟雾 | 全量开关 | 阻塞 |
|----|------|------|--------------|------------|------|----------|------|
| — | 09 | [gbn](GBN_README.md) | `72ad3692916e` | dtgb | **已跑** 8/8 | `run_gbn_table.sh` / `run_gbn_ablation.sh` | **主表与消融均完成**（2026-09-14）；详见 [GBN_REPRO_LOG.md](GBN_REPRO_LOG.md)
| 2 | 10 | [stable_chebnet](STABLE_CHEBNET_README.md) | `7d7a7e269611` | dtgb | **已跑** 真实 Peptides-func 2ep，退出 0 | `run_stable_chebnet_full.sh` | 官方原样已跑（200ep）：**Test AP 67.869 vs 论文 70.32 ± 0.26**；待步骤 7 定位 | |
| 3 | 31 | [puma](PUMA_README.md) | `9e4e87f53db0` | dtgb 试跑 | **已跑** CoraFull bare 1ep，退出 0 | `run_puma_full.sh` | 官方钉 torch 1.13；`--repeat 1` 的 std 为 nan |
| 4 | 15 | [scalegnn](SCALEGNN_README.md) | `4825c7ed2ccb` | dtgb | **已跑** Cora 2ep，退出 0 | `run_scalegnn_full.sh` | 官方 yaml 用 test 选模 |
| 5 | 44 | [labeling_trick](LABELING_TRICK_README.md) | `17b71959c854` | dtgb | **已跑** load Cora，退出 0 | `run_labeling_trick_full.sh` | `--test`=10 seed，无短训 CLI |
| 6 | 13 | [mavn](MAVN_README.md) | `3773c40a753a` | dtgb | **已跑** minesweeper 2ep，退出 0 | `run_mavn_full.sh` | LRGB 大文件未拉 |
| 7 | 08 | [fair_eval_gfm](FAIR_EVAL_GFM_README.md) | `0a388f087773` | uv（无 conda gfm） | **已跑** tolokers-2 2 step，退出 0 | `run_fair_eval_gfm_full.sh` | 只用 tolokers-2；Python 3.12.9 |
| 8a | 01 | [equivariance](EQUIVARIANCE_README.md) | `1dfe3870fd8a` | dtgb+neptune | **失败** 退出 1（Triton 需 gcc） | `run_equivariance_full.sh` | PyG2.8 补丁已打；本机无 C 编译器 |
| 8b | 04 | [mf_gia](MF_GIA_README.md) | `9b2946d13af0` | 独立 3.12 | **阻塞** 无 `datasets/`，未训 | `run_mf_gia_full.sh` | 数据目录极严；与 01 二选一 |
| 9a | 23 | [graphrp](GRAPHRP_README.md) | `38b00ecd2cc4` | — | **拒绝（无源码）** | 拒绝 | **仓库只有 README** |
| 9b | 41 | [unlearning_inv](UNLEARNING_INV_README.md) | `3bfc1f17e82a` | dtgb | **已跑** Cora 2ep（py310 补丁），退出 0 | `run_unlearning_inv_full.sh` | 补丁只改 f-string 引号 |
| 10 | 12 | [stem_gnn](STEM_GNN_README.md) | `8995878ca0df` | 未建 stem_gnn | **未训**（缺 lightning/einops；Cora.pt 已核） | `run_stem_gnn_full.sh` | **禁止** `conda env create -f environment.yml` |
| 11 | 22 | [core_graphrag](CORE_GRAPHRAG_README.md) | `37a81bc38b0c` | dtgb | **已跑** karate RkH，退出 0 | 算法侧，无 LLM | pytest/OpenAI 不做 |

## 目录约定（每篇一套，不要混）

```
repro/<name>/                  # 官方克隆（gitignore）
repro/<NAME>_README.md         # 只讲这一篇怎么跑
repro/<NAME>_REPRO_LOG.md      # 只追加这一篇
repro/run_<name>.sh            # 单次（走 85% 限额）
repro/run_<name>_full.sh       # 全量，默认打印命令
repro/download_<name>.sh       # 只写这一篇的数据
paper/notes/<id>_<name>.md
results/<name>/runs/
```

## 预处理阶段明确不做

- 不并行开两篇训练。  
- 不为 13 篇各建一套完整 CUDA 环境。  
- 不跑 SGPC Actor/Squirrel 10 划分、不跑 GBN CS 10-iter、不跑 PUMA table2、不跑 GraphRAG LLM。  
- 不把 GraphRP README 里的假目录当成已有代码。
