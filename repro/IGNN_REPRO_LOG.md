# IGNN 复现日志

## 目标与范围

复现 NeurIPS 2025 论文 *Making Classic GNNs Strong Baselines Across Varying Homophily* 的官方 IGNN 代码。首轮只验证三个严格 public-split 小数据集，不重新搜索超参数或运行 30 个基线。

- 官方仓库：`galogm/IGNN`
- 固定提交：`7a1bb0adb3ccb78e193276e181cbf8d2090ed61f`
- public 入口：`scripts/00-best-racIGNN-public.sh`
- 官方汇总：`results/table_pub.csv`

服务器直连 `github.com:443` 克隆超时；通过只读镜像克隆后，已使用 GitHub API 返回的 `master` SHA 逐字核验提交一致。

## 独立环境

采用官方 RTX 3090 Setting 2：

- Conda：`/home/lab_user/tools/miniconda3/envs/ignn`
- Python 3.8.16
- PyTorch 2.1.2+cu121
- PyG 2.4.0
- DGL 2.0.0+cu121
- `graph_datasets` 1.1.1
- `the_utils` 1.0.2
- `ogb` 1.3.6
- NVIDIA GeForce RTX 3090 24 GiB，驱动 595.84

DGL wheel 依赖系统 CUDA 动态库，已从 NVIDIA `cuda-12.1.1` 固定标签在独立环境中补装 runtime。核心包导入成功，`pip check` 无冲突。

官方结果表使用 V100、Python 3.9.15、PyTorch 2.0.1、CUDA 11.7。README 明确说明相同超参数在 V100 与 RTX 3090 上可能产生明显差异，因此本轮判断代码/协议是否闭环，并记录数值偏差，不要求逐位一致。

## 追加式日志

所有运行通过 `repro/run_ignn.sh` 执行。每次运行在 `results/ignn/runs/<UTC时间>_<标签>/` 中保存：

- 完整命令；
- 官方源码提交与状态；
- Python、CUDA、GPU 和核心依赖版本；
- 标准输出、起止时间与退出码。

每次运行使用独立目录，不覆盖历史。

## Actor

烟雾测试：

- 目录：`results/ignn/runs/20260912T054833Z_smoke_actor_c_public_2ep_r1/`
- 仅将官方命令缩为 2 epoch、1 split。
- 7,600 节点、30,019 条原始边、932 维特征、5 类。
- 10 个 public mask 被正确识别，首个划分为 48%/32%/20%。
- 退出码 0；2 epoch 测试准确率 25.13%，不用于论文比较。

正式运行：

- 目录：`results/ignn/runs/20260912T054919Z_official_actor_c_public_r10/`
- 官方 c-IGNN 命令原样运行，3000 epoch 上限、10 个公开划分、early stopping 200。
- 本次：`37.43±0.97`
- 官方：`38.01±1.11`
- 差值：`-0.58` 个百分点
- 退出码 0

结论：Actor public split 成功复现。

## Roman-empire 协议审计

首次烟雾测试因 `graph_datasets` 直连 GitHub 下载数据超时而失败，失败日志保存在：

`results/ignn/runs/20260912T055051Z_smoke_roman_empire_c_public_2ep_r1/`

随后经 GitHub API 从上游固定提交 `a431395` 下载 `roman_empire.npz`：

- Git blob SHA：`1f9bae5e95b28e529015269e98acb237b65d8d3b`
- SHA-256：`a58ba741d123bf892fe5c872138d07463d75a2e9012360b8dd78ac2d4766d428`
- 文件包含 10 组 `train_masks`、`val_masks`、`test_masks`。

烟雾重试成功，日志位于：

`results/ignn/runs/20260912T055347Z_smoke_roman_empire_c_public_2ep_r1_retry/`

但 `graph_datasets 1.1.1` 的 `datasets/critical.py` 只读取特征、标签和边，没有返回 NPZ 内公开 mask。因此 `get_splits(..., public=True)` 检测不到公开 mask，会回退到仓库固定的 48%/32%/20% custom split。

该问题同样影响 `source=critical` 的 Chameleon、Squirrel 和 Amazon-ratings。它们不能被严格称为 public-split 结果，本轮不将其纳入三个严格 public 数据集。

## PubMed

烟雾测试：

- 目录：`results/ignn/runs/20260912T055455Z_smoke_pubmed_c_public_2ep_r1/`
- 标准 Planetoid mask：60 个训练、500 个验证、1,000 个测试节点。
- 退出码 0。

正式运行：

- 目录：`results/ignn/runs/20260912T055529Z_official_pubmed_c_public_r3/`
- 同一个公开划分连续运行 3 次随机初始化。
- 本次：`79.63±0.26`
- 官方：`80.03±0.37`
- 差值：`-0.40` 个百分点
- 退出码 0

结论：PubMed public split 成功复现。

## WikiCS

烟雾测试：

- 目录：`results/ignn/runs/20260912T055720Z_smoke_wikics_c_public_2ep_r1/`
- 20 个公开划分被正确识别。
- 首个划分 train/val/test 占全图 4.96%/15.12%/49.97%。
- 退出码 0。

正式运行：

- 目录：`results/ignn/runs/20260912T055747Z_official_wikics_c_public_r20/`
- 官方命令完整运行 20 个公开划分。
- 本次：`80.46±0.41`
- 官方：`80.55±0.43`
- 差值：`-0.09` 个百分点
- 退出码 0

结论：WikiCS public split 成功复现。

## 首轮结论

三个真实 public-split 数据集均成功：

- Actor：`37.43±0.97`，差 `-0.58` 个百分点；
- PubMed：`79.63±0.26`，差 `-0.40` 个百分点；
- WikiCS：`80.46±0.41`，差 `-0.09` 个百分点。

最大均值偏差为 0.58 个百分点。官方模型、训练、验证集选模、测试评测和确定性 RNG 序列能够闭环。

## 可追溯性与随机性边界

- `scripts/make_tab_pub.py` 依赖未入库的 `results/public.csv`；仓库仅保留 `table_pub.csv` 与 `table_our.csv`，所以无法从作者逐运行记录重建汇总表。
- `pyproject.toml` 声明 PyG 2.6.1，而生产安装脚本使用 `requirements.txt` 的 PyG 2.4.0。本次遵循生产安装脚本。
- `set_seed(42)` 只在进程入口调用一次，split 循环内不重置。各 split 使用连续推进的确定性 RNG 序列，不是每个 split 独立重新播种。
- products 和 pokec 的 best/搜参脚本还存在 epoch、eval_start、public、repeat 参数不一致；完成单独协议审计前不运行大图实验。

下一阶段建议转向仓库固定的 10× 48%/32%/20% custom split，并优先验证 c-IGNN 的 Actor、Chameleon、Squirrel。
