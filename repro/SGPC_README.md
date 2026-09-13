# SGPC 复现

论文：*Sheaf Graph Neural Networks via PAC-Bayes Spectral Optimization*（AAAI 2026）。论文库编号 29。

- 官方仓库：`repro/sgpc/`（https://github.com/ChoiYoonHyuk/SGPC），提交 `114b585d0d0e32afbf1d7232dd04c013fa8453e2`
- 过程日志：[SGPC_REPRO_LOG.md](SGPC_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/07-ccf-aaai-ijcai-sigir/29_SGPC_AAAI2026_official.pdf`
- 附录：`repro/sgpc/Supplemental.pdf`
- 读书笔记：`paper/notes/29_sgpc.md`

仓库只有 `main.py`、`ReadMe.md`、`Supplemental.pdf`。无 `requirements.txt`、无 seed、无 CLI 超参；唯一参数是数据集编号 0–8。

## 当前结论

步骤 1–7 基本完成。官方原样 8/9 单次已跑（Pubmed 另用 `--spec lobpcg` 跑通）；协议开关已加（默认关）。geom-gcn 10 划分已完成全部 6 个异配集：Actor / Chameleon / Cornell / Texas / Wisconsin / Squirrel（Actor 于 2026-09-12 23:16 收尾）。Cora / Citeseer 各 5 seed 完整（Citeseer seed 3 曾因稠密 `eigvalsh` 未收敛，已重跑）。

**不能**把划分 0 单次数字写成 Table 1。剩余全量：`bash repro/run_sgpc_full.sh`（默认 dry-run）。

## 协议开关（默认 = 官方原样）

```bash
python main.py DATA_ID [--seed N] [--split 0-9] [--spec dense|lobpcg|off] [--max_epochs 2000]
```

补丁：`repro/patches/sgpc-protocol.patch`。无额外参数时应走官方路径。Pubmed 必须 `--spec lobpcg` 或 `off`。

## 环境

复用 `dtgb`（Python 3.10、torch 2.2.1+cu121、PyG 2.8、torch_sparse）。官方未声明版本。

## 数据

官方把数据根目录写死为 `/tmp/<Name>`。先镜像预下载，再由入口脚本做符号链接：

```bash
conda activate dtgb
python repro/download_sgpc_data.py          # 全部 9 个
# python repro/download_sgpc_data.py 0 6    # 只下 Cora / Cornell
```

数据落在 `repro/sgpc/data/<Name>/`。`run_sgpc.sh` 会执行 `/tmp/<Name> -> 该目录`。

| id | 数据集 |
|----|--------|
| 0 | Cora |
| 1 | Citeseer |
| 2 | Pubmed（稠密 `eigvalsh`，N=19717，先不要跑） |
| 3 | Chameleon |
| 4 | Squirrel |
| 5 | Actor |
| 6 | Cornell |
| 7 | Texas |
| 8 | Wisconsin |

## 运行

在工作区根目录：

```bash
# 单数据集（Cornell = 6）
bash repro/run_sgpc.sh official 6

# 多个，顺序跑
bash repro/run_sgpc_batch.sh official 0 1 5 6 7 8

# 异配 10 划分（固定 seed 0）
bash repro/run_sgpc_splits.sh webkb_s0 6 7 8

# 剩余全量（默认只打印）
bash repro/run_sgpc_full.sh
# FULL=1 bash repro/run_sgpc_full.sh

# 解析日志：同时给出 val 选模 test 与官方 oracle Best Test
python scripts/parse_sgpc_log.py results/sgpc/runs/*.log --csv results/sgpc/official_summary.csv
python scripts/summarize_sgpc_splits.py results/sgpc/runs/*webkb_s0*.log
```

入口会：激活 `dtgb`、检查预下载、建 `/tmp` 链接、走 85% 资源上限、把提交哈希与 stdout 写入 `results/sgpc/runs/<时间戳>_<label>_<Name>_pid*.log`。

## 对表时必须同时报两个数字

官方训练循环用 test 精度取 max 作为 `Best Test`（oracle）。常规协议应取最高 val 时刻的 test。解析脚本两种都给。论文 Table 1（%）：

| Cora | Citeseer | Pubmed | Actor | Chameleon | Squirrel | Cornell | Texas | Wisconsin |
|------|----------|--------|-------|-----------|----------|---------|-------|-----------|
| 83.0 ± 0.55 | 72.6 ± 0.21 | 79.9 ± 0.06 | 38.1 ± 0.52 | 53.3 ± 1.29 | 36.0 ± 0.30 | 81.0 ± 2.33 | 83.2 ± 1.82 | 81.1 ± 2.60 |

已跑结果见 `results/sgpc/official_summary.csv` 与过程日志步骤 6。
