# SCALEGNN 复现日志

论文：*ScaleGNN: Towards Scalable Graph Neural Networks via Adaptive High-order Neighboring Feature Fusion*，WWW 2026。论文库编号 15。
官方代码：https://github.com/lx970414/ScaleGNN
本地论文：`papers/gnn-frontier-2025-2026/03-scalable-bigdata-gnn/15_ScaleGNN_WWW2026.pdf`
读书笔记：`paper/notes/15_scalegnn.md`
学习模块：`LEARNING_PLAN.md` M3

约定：日志只追加。官方仓库 `repro/scalegnn/`。产物 `results/scalegnn/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：Cora/Citeseer/Pubmed 小图；主表 ogbn-arxiv（约 1 小时 / 10 seed）。papers100M 仅 memmap 路径。

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`4825c7ed2ccb8a7a4c47edce4afefb1e771389aa`
- 克隆：`bash scripts/clone_official_repo.sh scalegnn lx970414/ScaleGNN`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`dtgb`
- 安装：`echo reuse dtgb; python -c 'import yaml,ogb'`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- 小图 Planetoid 符号链接 `repro/sgpc/data/Cora` → `repro/scalegnn/data/Cora`。arxiv 用 OGB `./data`。
- 下载脚本：见 `repro/download_scalegnn.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 官方验证环境是 Python 3.12 + torch 2.11+cu128；本机先用 dtgb（2.2.1+cu121）。
2. `config_cora.yaml` 默认 `device: cpu` 且 `selection_metric: test`（用 test 选模）。
3. 烟雾不要改官方 yaml：复制到 results/scalegnn/ 再改 epochs。
4. ogbn-arxiv 走 `ogb_precompute_train.py`；papers100M 走 memmap，不要一次载入全图。

## 2026-09-12 步骤 5：烟雾测试

- 计划命令：

```
bash repro/run_scalegnn.sh smoke_cora -- python main.py --config /home/lab_user/project/lzc/results/scalegnn/smoke_cora.yaml
```

- smoke yaml 由预处理写入 results/scalegnn/smoke_cora.yaml（epochs=2, device=cuda）。
- 退出码 0。日志 `results/scalegnn/runs/20260912_175350_smoke_cora_pid84975.log`。Cora 2 epoch Val 0.316 / Test 0.319（不对论文）。配置在 `results/scalegnn/smoke_cora.yaml`，未改官方 yaml。权重写在 `results/scalegnn/smoke_save/`。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_scalegnn_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
