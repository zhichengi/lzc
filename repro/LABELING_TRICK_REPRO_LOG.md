# LABELING_TRICK 复现日志

论文：*Improving Graph Neural Networks on Multi-node Tasks with the Labeling Trick*，JMLR 2025。论文库编号 44。
官方代码：https://github.com/GraphPKU/LabelingTrick
本地论文：`papers/gnn-frontier-2025-2026/11-journals-tnnls-jmlr/44_LabelingTrick_JMLR2025.pdf`
读书笔记：`paper/notes/44_labeling_trick.md`
学习模块：`LEARNING_PLAN.md` M5

约定：日志只追加。官方仓库 `repro/labeling_trick/`。产物 `results/labeling_trick/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：LinkPred 子目录：Cora/CiteSeer/PubMed 无向链接预测 AUROC；`--test` 为 10 seed 正式协议

---

## 2026-09-12 步骤 1：源码固定

- 官方默认分支提交：`17b71959c854c5379e1b042100321661c7d1d55e`
- 克隆：`bash scripts/clone_official_repo.sh labeling_trick GraphPKU/LabelingTrick`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## 2026-09-12 步骤 2：环境

- 计划 conda：`dtgb`
- 安装：`echo reuse dtgb; python -c 'import optuna, torch_scatter'`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## 2026-09-12 步骤 3：数据核验

- `repro/labeling_trick/LinkPred/data/` 链到已有 Planetoid。
- 下载脚本：见 `repro/download_labeling_trick.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## 2026-09-12 步骤 4：代码审计（只记录不改）

1. 四个子仓库互不共享入口。主线用 LinkPred。
2. 无 `--test` 时跑 Optuna 200 trial + sqlite，不要当正式数字。
3. `--test` 仍是 10 个 seed、每 seed 最多 2000 step，不是烟雾。
4. 需要 optuna、torch_scatter；device 写死 cuda。
5. Planetoid 根目录 `./data`（相对 LinkPred）。

## 2026-09-12 步骤 5：烟雾测试

- 计划命令：

```
bash repro/run_labeling_trick.sh smoke_import -- python -c "from Dataset import load_dataset; d=load_dataset('Cora'); print('nodes', d.num_nodes, 'edges', d.edge_index.size(1))"
```

- 官方无短 epoch CLI。训练烟雾不要用 --test（那是 10 seed 全量）。全量：python main.py --dataset Cora --test
- 退出码 0。日志 `results/labeling_trick/runs/20260912_175350_smoke_import_pid84939.log`。`load_dataset('Cora')` → 2708 节点 / 10556 边。训练烟雾未做（官方 `--test` 是 10 seed）。

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_labeling_trick_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
