# 04 MF_GIA 预处理 / 复现入口

论文：*Modality-Free Graph In-context Alignment*（ICLR 2026）。论文库编号 04。学习模块：`LEARNING_PLAN.md` M6。

- 官方仓库：`repro/mf_gia/`（https://github.com/JhuoW/MF-GIA）
- 固定提交：`9b2946d13af0372323b5e3f3105d822757a87cd9`（分支 `master`，与 `git ls-remote HEAD` 一致）
- 过程日志：[MF_GIA_REPRO_LOG.md](MF_GIA_REPRO_LOG.md)
- 本地论文：`papers/gnn-frontier-2025-2026/01-graph-foundation-models/04_MF-GIA_ICLR2026.pdf`
- 读书笔记：`paper/notes/04_mf_gia.md`
- 运行产物：`results/mf_gia/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（2026-09-12）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `gfm`；conda create -n mf_gia python=3.12 -y  # 见 README，暂不执行 |
| 数据 | 按 README 组织 datasets/；OFA 原始文件来自 https://github.com/LechengKong/OneForAll |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_mf_gia_full.sh`（默认 dry-run） |

对照目标：ICL 节点分类：Cora k-shot。预训练 8000 epoch，优先用仓库 checkpoint。

## 烟雾（短）

```bash
# 仓库无 datasets/（ofa/pyg 文本图），ICL 无法启动。ckpt 在 generated_files/ 里也没用。
echo 'blocked: missing datasets/'
```

不要在预处理阶段跑 pretrain.py（8000 epoch）。不要手搓数据树冒充官方 OFA。

## 全量（默认不跑）

```bash
bash repro/run_mf_gia_full.sh          # 只打印命令
FULL=1 bash repro/run_mf_gia_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
