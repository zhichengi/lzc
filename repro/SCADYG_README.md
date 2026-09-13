# ScaDyG 复现

论文：*ScaDyG: A New Paradigm for Large-Scale Dynamic Graph Learning*
（IEEE TNNLS 2026）。

- 官方仓库：`repro/scadyg/`
- 固定提交：`28ca94a06771c46073b650de3daa95e0939342ba`
- 过程日志：[SCADYG_REPRO_LOG.md](SCADYG_REPRO_LOG.md)
- 复现报告（初稿）：[SCADYG_REPORT.md](SCADYG_REPORT.md)
- checkpoint issue 草稿（未发出）：[scadyg_issue_draft.md](scadyg_issue_draft.md)
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

默认 1 epoch 回归：official MRR 0.6247271678，与最初基线逐位一致。消融与 BitcoinAlpha 尚未做。报告初稿见 [SCADYG_REPORT.md](SCADYG_REPORT.md)。结构化数字：`results/scadyg/multiseed_summary.csv`。
