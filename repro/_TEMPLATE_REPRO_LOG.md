# <NAME> 复现日志

论文：*<完整标题>*，<会议 年份>。论文库编号 <NN>。  
官方代码：<URL>  
本地论文：`papers/gnn-frontier-2025-2026/<目录>/<文件名>.pdf`  
读书笔记：`paper/notes/<NN>_<name>.md`  
学习模块：`LEARNING_PLAN.md` M?

约定：

- 日志按时间追加，不改写既有结论。
- 官方仓库放 `repro/<name>/`；运行产物放 `results/<name>/runs/`。
- 先保留官方算法与评测实现，只在外层处理环境、GPU 编号、相对路径和日志。
- 每次运行记录官方提交哈希、环境版本、完整命令和独立文本日志。
- 复现目标（论文主表中要对照的格）：<数据集> <指标> **<数值 ± std>**（<n> 次）。

---

## <YYYY-MM-DD> 步骤 1：源码固定

- 官方默认分支提交：`<sha>`
- 克隆方式：<镜像 URL>；与 GitHub API 返回 SHA 比对：一致 / 不一致
- 仓库提交数：<n>（只有 1 个提交时要注意作者后续推送）

## <YYYY-MM-DD> 步骤 2：环境

- conda 环境：`<env>`（复用 / 新建）；脚本 `scripts/setup_<name>_conda.sh`
- Python / torch / CUDA / PyG / DGL：
- `pip check`：
- 官方声明环境与本地差异：

## <YYYY-MM-DD> 步骤 3：数据核验

- 数据集与来源 URL：
- 下载方式（镜像）：`repro/download_<name>.sh`
- SHA-256：
- 是否可重建并比对：

## <YYYY-MM-DD> 步骤 4：代码审计（只记录不改）

1. cwd / 绝对路径依赖：
2. GPU 编号写死：
3. wandb / 外部服务：
4. seed 设置位置与覆盖范围：
5. 选模指标 vs 论文主指标：
6. checkpoint 覆盖的模块：
7. 负采样 / 数据划分与论文文字是否一致：
8. README 与实现不一致处：
9. `--repeat` 语义：

## <YYYY-MM-DD> 步骤 5：烟雾测试

- 命令：
- 日志：`results/<name>/runs/<...>`
- 退出码：
- 只验证链路，不与论文比较。

## <YYYY-MM-DD> 步骤 6：官方原样

- 命令：
- 日志：
- 结果：**<数值>**；论文 **<数值 ± std>**；差值：
- 无论多离谱，原样记录。

## <YYYY-MM-DD> 步骤 7：定位失配

- 失配类型：超参未公开 / 代码 bug / 硬件与环境 / 协议与论文文字不一致
- 诊断脚本：`repro/diagnose_<name>_*.py`
- 证据：

## <YYYY-MM-DD> 步骤 8：修正版

| 开关 | 默认 | 含义 | 论文依据 |
|------|------|------|----------|

- 补丁：`repro/<name>-<fix>.patch`，SHA-256：
- 默认 1 epoch 回归：与步骤 5 逐位一致 / 不一致

## <YYYY-MM-DD> 步骤 9：多 seed

- seeds：0–4 / 0–9，独立进程，脚本 `repro/run_<name>_multiseed.sh`
- 结果表：`results/<name>/<variant>_multiseed_summary.csv`
- 均值 ± 样本标准差：**<...>**；论文 **<...>**

## <YYYY-MM-DD> 步骤 10：分层结论

| 层级 | 是否达到 | 说明 |
|------|----------|------|
| L1 管线闭环 | | |
| L2 数值量级 | | |
| L3 统计一致 | | |

## <YYYY-MM-DD> 步骤 11：冻结

- 剩余假设：
- 停止理由：
- 给作者的 issue 草稿：`repro/<name>_issue_draft.md`（若有确定 bug）
- `results/SUMMARY.md` 已更新；`paper/notes/<NN>_<name>.md` 已定稿
- git 提交：`repro(<name>): freeze, L? reached`
