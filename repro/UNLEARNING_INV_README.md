# 41 UNLEARNING_INV 预处理 / 复现入口

论文：*Unlearning Inversion Attacks for Graph Neural Networks*（WSDM 2026）。论文库编号 41。学习模块：`LEARNING_PLAN.md` M7。

- 官方仓库：`repro/unlearning_inv/`（https://github.com/QwQ2000/WSDM26-Graph-Unlearning-Inversion）
- 固定提交：`3bfc1f17e82a3a9fad9b1cc3ef28281a1323ea16`（分支 `main`，与 `git ls-remote HEAD` 一致）
- 过程日志：[UNLEARNING_INV_REPRO_LOG.md](UNLEARNING_INV_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/10-wsdm/41_UnlearningInversion_WSDM2026.pdf`
- 读书笔记：`paper/notes/41_unlearning_inv.md`
- 运行产物：`results/unlearning_inv/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `dtgb`；echo reuse dtgb |
| 数据 | Planetoid Cora，PyG 默认路径。可复用已有下载。 |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_unlearning_inv_full.sh`（默认 dry-run） |

对照目标：Cora 上 Inversion + GIF；README 示例 num_runs=5。与 23 二选一全量。

## 烟雾（短）

```bash
bash repro/run_unlearning_inv.sh smoke_cora -- python main.py --dataset_name cora --target_model GCN --exp Inversion --method GIF --unlearn_ratio 0.05 --attack_method trend_steal --num_runs 1 --num_epochs 2 --cuda 0 --is_gen_unlearn_request True --is_gen_unlearned_probs True
```

若 METIS/分区失败，记入日志，不要改算法。

## 全量（默认不跑）

```bash
bash repro/run_unlearning_inv_full.sh          # 只打印命令
FULL=1 bash repro/run_unlearning_inv_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
