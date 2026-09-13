# 复现工作区

四条已开线 + 队列论文的预处理都在本目录。各篇互相独立，总索引 [`PREP_STATUS.md`](PREP_STATUS.md)。
顶层数字见 [`../results/SUMMARY.md`](../results/SUMMARY.md)。
流程与判定见 [`../REPRO_ROADMAP.md`](../REPRO_ROADMAP.md)；学习计划见 [`../LEARNING_PLAN.md`](../LEARNING_PLAN.md)；
已开线收尾见 [`CLOSEOUT_PLAN.md`](CLOSEOUT_PLAN.md)。新开一篇时复制 [`_TEMPLATE_REPRO_LOG.md`](_TEMPLATE_REPRO_LOG.md)。

| 编号 | 论文 | 怎么跑 | 过程日志 | 官方克隆 | conda |
|------|------|--------|----------|----------|-------|
| 11 | IGNN | [IGNN_README.md](IGNN_README.md) | [IGNN_REPRO_LOG.md](IGNN_REPRO_LOG.md)；custom：[IGNN_CUSTOM_SPLIT.md](IGNN_CUSTOM_SPLIT.md) | `ignn/` | `ignn` |
| 43 | ScaDyG | [SCADYG_README.md](SCADYG_README.md) / [SCADYG_REPORT.md](SCADYG_REPORT.md) | [SCADYG_REPRO_LOG.md](SCADYG_REPRO_LOG.md) | `scadyg/` | `scadyg` |
| 40 | GCTD | [GCTD_README.md](GCTD_README.md) | [REPRO_LOG.md](REPRO_LOG.md)（历史文件名，未改成 `GCTD_REPRO_LOG.md`） | `gctd/` | `gctd`（对照用 `dtgb`） |
| 29 | SGPC | [SGPC_README.md](SGPC_README.md) | [SGPC_REPRO_LOG.md](SGPC_REPRO_LOG.md) | `sgpc/` | `dtgb` |
| 09–22 等 | 队列预处理 | [PREP_STATUS.md](PREP_STATUS.md) | 各 `<NAME>_REPRO_LOG.md` | 各 `<name>/` | 见表 |

约定：

- 官方仓库放 `repro/<name>/`，自带 `.git`，**不加入根仓库**。
- 对官方代码的改动以 `repro/<name>-*.patch` 为准；GCTD 的 `gctd-repro.patch` 已补齐并验证（`CLOSEOUT_PLAN.md` R-WS-1）。
- 运行产物放 `results/<name>/runs/`；每次运行独立日志，不覆盖。
- 先保留官方算法与评测，只在外层处理环境、GPU、镜像下载和日志。
- 长任务走 `scripts/run_capped.sh` / `scripts/capped_env.sh`（85% 上限）。

## 目录

```
repro/
├── README.md                      # 本文件
├── CLOSEOUT_PLAN.md               # 已开线收尾
├── _TEMPLATE_REPRO_LOG.md
├── GCTD_README.md / REPRO_LOG.md / run_gctd.sh / diagnose_cora.py
├── SCADYG_README.md / SCADYG_REPRO_LOG.md / run_scadyg*.sh / scadyg-*.patch
├── IGNN_README.md / IGNN_REPRO_LOG.md / IGNN_CUSTOM_SPLIT.md / run_ignn*.sh
├── SGPC_README.md / SGPC_REPRO_LOG.md / run_sgpc*.sh / download_sgpc_data.py
├── download_planetoid.sh / download_critical.sh
└── gctd/ scadyg/ ignn/ sgpc/ gcond/   # 官方克隆，不入根 git
```
