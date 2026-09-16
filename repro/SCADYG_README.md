# ScaDyG 复现

论文：*ScaDyG: A New Paradigm for Large-Scale Dynamic Graph Learning*
（IEEE TNNLS 2026）。

- 官方仓库：`repro/scadyg/`
- 固定提交：`28ca94a06771c46073b650de3daa95e0939342ba`
- 过程日志：[SCADYG_REPRO_LOG.md](SCADYG_REPRO_LOG.md)
- 复现报告（初稿）：[SCADYG_REPORT.md](SCADYG_REPORT.md)
- 组件消融汇总：[`results/scadyg/ablation_summary.csv`](../results/scadyg/ablation_summary.csv)（逐 run：[`ablation_runs.csv`](../results/scadyg/ablation_runs.csv)）
- 消融入口：`bash repro/run_scadyg_ablation.sh`（4 组件 × seeds 0–4）
- checkpoint issue 草稿（2026-09-16 决定不发出）：[scadyg_issue_draft.md](scadyg_issue_draft.md)
- 实验日志：`results/scadyg/runs/`
- 读书笔记：`paper/notes/43_scadyg.md`
- 本地论文：`papers/gnn-frontier-2025-2026/11-journals-tnnls-jmlr/43_ScaDyG_TNNLS2026.pdf`

## 环境

ScaDyG 使用独立 conda 环境，不修改 `dtgb` 和 `gctd`：

```bash
bash scripts/setup_scadyg_conda.sh
```

官方 `requirements.txt` 是包含大量无关包的完整环境导出，且 torch、PyG、DGL
版本组合不一致。本复现以已验证的 `dtgb` CUDA 栈为基础，只安装入口所需的
最小补充依赖，详见 `repro/requirements-scadyg.txt`。

## 运行

在工作区根目录执行：

```bash
# 1 epoch 管线测试
bash repro/run_scadyg.sh mooc --epochs 1 --seed 2023

# 官方默认：100 epoch
bash repro/run_scadyg.sh mooc --seed 2023

# 与论文主指标一致的 MRR 选模对照
bash repro/run_scadyg.sh mooc --seed 2023 --selection_metric mrr

# 同时输出 official 与 filtered full-item MRR
bash repro/run_scadyg.sh mooc --seed 2023 --eval_protocol both --selection_metric mrr

# canonical seeds 0–4；首个参数也可改为 ap
bash repro/run_scadyg_multiseed.sh mrr
```

入口会固定使用单卡机器的 `cuda:0`，自动创建官方源码需要的 `weights/`，并将
提交哈希、环境版本、完整命令和标准输出保存到独立时间戳日志。

## 当前边界

第一次对表保持官方模型、负采样、AP 选模和 MRR 评估实现不变。审计发现的
随机种子、选模和检查点问题已记录，修复结果作为明确标注的“论文协议修正版”
对照保留，不与官方基线混合。

当前已保留四层结果（canonical seeds 0–4）：

| 设定 | MRR |
|------|-----|
| 官方源码原样 | ~0.025（checkpoint 只存预测层） |
| 只修 checkpoint，AP 选模 | 0.915 ± 0.009 |
| checkpoint + MRR 选模（官方评测） | **0.922 ± 0.014**（论文 0.931 ± 0.009） |
| 同一 checkpoint，严格 item 排名 | **0.204 ± 0.004** |
| 合法二部图训练负采样 + 严格评测 | 0.203 ± 0.004（无改进） |

组件消融（R-SCADYG-2，seeds 0–4，`--ablate none` 即完整模型）：

| 组件 | official MRR | Δ vs 论文 |
|------|--------------|-----------|
| `none`（完整） | **0.9225 ± 0.0142** | −0.0085（1σ 内）|
| `hyper` | 0.8032 ± 0.0412 | −0.1278 |
| `time` | 0.8277 ± 0.0773 | −0.1033 |
| `topo` | **0.0099 ± 0.0000** | −0.9211（塌成随机）|

默认 1 epoch 回归：official MRR 0.6247271678，与最初基线逐位一致。**BitcoinAlpha 第二数据集已完成**：canonical seeds 0–4 的 official MRR 为 **0.719470 ± 0.006932**。消融已完成（见 `results/scadyg/ablation_summary.csv`）。报告初稿见 [SCADYG_REPORT.md](SCADYG_REPORT.md)。结构化数字：`results/scadyg/multiseed_summary.csv`。

## BitcoinAlpha

BitcoinAlpha 的原始数据来自 SNAP，下载、哈希记录、去注释和快照预处理由以下入口完成：

```bash
bash repro/download_scadyg_bitcoinalpha.sh
```

默认使用 723000 秒切片，并按原始预处理脚本的默认行为补充反向边。生成目录为
`repro/scadyg/dataset/bitcoinalpha/`。如需改变切片宽度，可设置
`SCADYG_SNAPSHOT_SECONDS`；如需保留有向边，可直接调用预处理脚本并加上
`--no-reverse-edges`：

```bash
conda run -n scadyg python repro/scadyg/process_raw_data/process_bitcoin.py \
	--input repro/scadyg/dataset_raw/bitcoinalpha/bitcoinalpha.csv \
	--output-root repro/scadyg/dataset \
	--snapshot-seconds 723000 \
	--no-reverse-edges
```

生成数据后，先做 1 epoch 管线检查：

```bash
bash repro/run_scadyg.sh bitcoinalpha --epochs 1 --seed 2023
```

正式多 seed 使用：

```bash
bash repro/run_scadyg_multiseed.sh mrr bitcoinalpha 0 1 2 3 4
```

结构化数字：`results/scadyg/bitcoinalpha_multiseed_summary.csv`。
