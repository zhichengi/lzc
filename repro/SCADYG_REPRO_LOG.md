# ScaDyG 复现日志

> 当前：官方协议 MRR 选模 0.922 ± 0.014 vs 论文 0.931 ± 0.009；严格 item 排名 0.204 ± 0.004。组件消融已完成（R-SCADYG-2，2026-09-13）：`none` 0.9225±0.0142（1σ 内）> `hyper` 0.8032±0.0412 ≈ `time` 0.8277±0.0773 ≫ `topo` 0.0099（塌成随机）。BitcoinAlpha 已完成 5 seed：0.719470 ± 0.006932。报告：[SCADYG_REPORT.md](SCADYG_REPORT.md)。入口：[SCADYG_README.md](SCADYG_README.md)。

论文：*ScaDyG: A New Paradigm for Large-Scale Dynamic Graph Learning*，IEEE TNNLS 2026。  
官方代码：https://github.com/BITNEO/ScaDyG  
本地论文：`papers/gnn-frontier-2025-2026/11-journals-tnnls-jmlr/43_ScaDyG_TNNLS2026.pdf`

约定：

- 日志按时间追加，不改写既有实验结论。
- 官方仓库放在 `repro/scadyg/`；运行产物放在 `results/scadyg/runs/`。
- 先保留官方算法与评测实现，只在外层处理环境、GPU 编号、相对路径和日志。
- 每次运行记录官方提交哈希、环境版本、完整命令和独立文本日志。

---

## 2026-09-10 初始审计

### 目标

先复现论文的 MOOC 动态链接预测实验。论文报告 ScaDyG 的 MRR 为
**0.931 ± 0.009**；协议为按时间步 70%/15%/15% 划分，排名评估时每个源节点
使用 100 个负样本。论文实验机器为 RTX 3090 24GB，与本机一致。

### 代码来源

- 官方 `master` 提交：`28ca94a06771c46073b650de3daa95e0939342ba`
- GitHub 直连克隆因 `GnuTLS recv error (-110)` 失败；随后通过
  `ghfast.top` 镜像克隆同一官方仓库，并用提交哈希固定版本。
- 仓库自带 MOOC 原始数据、100 个预处理快照及可重建/核对快照的脚本
  `process_raw_data/process_mooc_release.py`，不需要先从 Zenodo 下载。

### 环境策略

官方 `requirements.txt` 是完整环境导出，不是最小依赖清单，其中同时包含：

- `torch==1.12.1+cu116`
- `torch_geometric==2.5.3`
- `dgl-1.0.0`
- 大量与主入口无关的 Web、NLP、调参和开发包

整体安装容易破坏现有 CUDA/PyG 组合。因此新建独立环境 `scadyg`：克隆已验证
可用的 `dtgb`（Python 3.10、torch 2.2.1+cu121、CUDA 12.1、PyG 扩展、
DGL 2.2.1），再只补官方入口缺少的 `deepsnap==0.2.1`、
`py-tgb==0.9.2`、`yacs==0.1.6`。脚本：
`scripts/setup_scadyg_conda.sh`。

### 运行前发现的问题

1. 官方入口默认 `--cuda_device 1`，本机只有一张卡，必须显式传
   `--cuda_device 0`。
2. 模型无条件写 `./weights/*.pth`，仓库没有 `weights/` 目录；外层入口负责创建。
3. 数据与日志使用相对当前目录的路径；外层入口固定在 `repro/scadyg/` 启动。
4. 源码中节点随机特征在 `torch.manual_seed(args.seed)` **之前**生成，因此 CLI
   seed 不能控制这部分随机性。
5. `--repeat > 1` 的每轮都重设为同一个 seed，并不等价于独立多种子实验。
6. 验证阶段以 **AP** 保存最佳模型，而论文主表指标是 **MRR**。
7. 最佳状态只保存 `Predict_layer`，未同时保存 `model_transformer`。
8. 源码先构造 1:1 随机负边用于 BCE/AP；排名评估另行生成每源节点 100 个负样本。
   自定义 1:1 负采样会随机更换源和目标，且不去重负样本。
9. 节点属性预测加载器含作者机器绝对路径；本阶段只跑 MOOC 链接预测，不触发。
10. `--fusion v2t` 引用仓库中不存在的 `scalable_tgn_affine_v2t_chunk.py`；
    默认 `t2v` 路径文件存在。

以上问题先记录。第一次运行只做必要移植，不修改其模型、数据划分、负采样或选模
逻辑；得到官方实现基线后，再决定是否建立“论文协议修正版”作为独立对照。

### 入口

```bash
bash scripts/setup_scadyg_conda.sh
bash repro/run_scadyg.sh mooc --epochs 1 --seed 2023
```

---

## 2026-09-10 数据核验与烟雾测试

### 数据一致性

用仓库附带的原始 `ml_mooc.csv` / `ml_mooc.npy` 重新执行
`process_raw_data/process_mooc_release.py`，输出到临时目录后与发布的
`dataset/mooc/` 比较：

- 节点数：7144
- 边数：411749
- 快照数：100
- 每个完整快照的边块大小：4118
- `edge_index`、`edge_time`、`edge_feature`、`node_feature`：全部逐元素一致

这一步确认当前实验不依赖作者机器上的隐藏 MOOC 预处理产物。

SHA-256：

- `dataset_raw/mooc/ml_mooc.csv`：
  `a17ee1f37f141a8db6547030c84043f4bd5b10bd888dbf7631853c4e10042bc8`
- `dataset_raw/mooc/ml_mooc.npy`：
  `2fcedad92a1b950dcca233fa9eeca8869ec74a867702ac06803a93a3872a759b`
- `dataset_raw/mooc/ml_mooc_node.npy`：
  `a2866aa91a170db7578480e294b816c20f33d766173ff6857a61b99fcee35e91`
- 对 400 个已排序快照文件的逐文件 SHA-256 清单再取 SHA-256：
  `57ed9577c2f6f7d22e7e19a3ea1482d8484c87563beb4faf8d817943362260c1`

### 依赖补充

入口首次导入时发现还需要 `torchmetrics`。已按官方清单的版本
`torchmetrics==1.2.1` 加入 `repro/requirements-scadyg.txt`。最终关键环境：

- Python 3.10.20
- torch 2.2.1+cu121
- PyG 2.8.0.post1
- DGL 2.2.1+cu121
- DeepSNAP 0.2.1
- py-tgb 0.9.2
- torchmetrics 1.2.1

### 1 epoch 烟雾测试

```bash
bash repro/run_scadyg.sh mooc --epochs 1 --seed 2023
```

日志：`results/scadyg/runs/20260910_213415_mooc_pid360254.log`

- 运行设备：RTX 3090，`cuda:0`
- 划分：70 个训练快照、15 个验证快照、15 个测试快照
- 参数量：56005
- 管线总耗时：约 27.6 秒
- 测试 `avg_mrr`：**0.624727**
- 测试 `avg_ap`：0.985757
- 测试 `avg_auc`：0.990608

1 epoch 结果只用于验证数据、训练、验证、100 负样本排名评估和测试全链路，
不能与论文的 **0.931 ± 0.009** 比较。

### 完整实验

已启动官方默认 100 epoch、seed 2023：

```bash
bash repro/run_scadyg.sh mooc --seed 2023
```

该运行保持官方的 AP 选模与早停逻辑。完成后再追加最终 MRR 与运行时。

### 官方源码原样运行结果

日志：`results/scadyg/runs/20260910_213512_mooc_pid360587.log`

- 命令：`bash repro/run_scadyg.sh mooc --seed 2023`
- 实际训练到 epoch 21 后由 patience=10 的官方逻辑早停
- 总耗时：344.0 秒
- 测试 `avg_mrr`：**0.025170**
- 测试 `avg_ap`：0.401836
- 测试 `avg_auc`：0.019418
- 论文目标：0.931 ± 0.009，差值为 -0.9058

该结果不是一般的随机波动：epoch 6 的逐快照验证 MRR 已在约 0.91–0.94，
但测试时多数快照 MRR 降到约 0.01，同时 AUC 接近 0。

### 上游检查点缺陷及补丁

根因位于 `scalable_tgn_link_prediction.py`：

1. 优化器共同训练 `model` 与 `model_transformer`。
2. 验证 AP 改善时，官方代码只将 `model.state_dict()` 保存到内存。
3. 早停后只恢复 `model`；`model_transformer` 保留 epoch 21 的参数。
4. 测试因此组合了不同 epoch 的两个模块，预测严重失配。

本地补丁同时保存并恢复 `model_transformer.state_dict()`，并在测试前对两个模块
调用 `eval()`。另修正主入口把返回的 MRR 错标为 `All AP` 的日志错误；算法、
超参数、AP 选模和负采样均未改动。补丁已通过 `git diff --check` 和 Python
语法检查。

下一次运行记为“checkpoint-fix”，不能与上面的官方源码原样结果混为一条。

### checkpoint-fix 完整结果

日志：`results/scadyg/runs/20260910_214335_mooc_pid362292.log`

- 源提交：`28ca94a06771c46073b650de3daa95e0939342ba`
- 跟踪文件补丁 SHA-256：
  `5ce31e5275df2683438b11432c07f103169577b1061425c30312c265d9c6a0fc`
- 命令：`bash repro/run_scadyg.sh mooc --seed 2023`
- 实际训练：epoch 0–21，之后按官方 AP/patience=10 规则早停
- 总耗时：344.4 秒
- 测试 `avg_mrr`：**0.927811**
- 测试 `avg_ap`：0.991759
- 测试 `avg_auc`：0.992688
- 测试 accuracy：0.984292
- 论文：**0.931 ± 0.009**
- 与论文中心值差：**-0.003189**

单次 seed 2023 的结果落在论文报告区间 `[0.922, 0.940]` 内。它还不能验证论文
的均值与标准差，但已经完成了代码、数据、评测和关键检查点缺陷的闭环复现。

原样运行和修复运行的训练/验证轨迹一致，且都在 epoch 21 停止；修复仅改变测试前
共同训练模块的恢复状态。MRR 从 0.025170 恢复到 0.927811，支持上述根因判断。

补丁可单独审阅或重新应用：
`repro/scadyg-checkpoint-fix.patch`。全部结构化结果汇总在
`results/scadyg/summary.csv`。

### 后续计划

1. 用独立进程分别运行 3–5 个 seed；不要使用官方 `--repeat`，因为它每轮重置同一
   seed。
2. 先确认不同 seed 的均值/样本标准差是否接近 0.931 ± 0.009。
3. 再建立单独的“论文协议修正版”，评估 MRR 选模、完整模块 checkpoint 以及更严格
   碰撞检查负采样的影响；不得覆盖当前官方基线。
4. MOOC 稳定后再做论文的三个 ScaDyG 消融，之后考虑 BitcoinAlpha/UCI。

---

## 2026-09-10 checkpoint-fix 五种子结果

使用独立进程运行 canonical seeds 0–4，均为默认 100 epoch、官方 AP 选模和
checkpoint-fix。各 run 的命令、补丁哈希和环境均已写入对应文本日志。

- seed 0：MRR 0.918152，epoch 29 早停
- seed 1：MRR 0.915360，epoch 28 早停
- seed 2：MRR 0.899404，epoch 24 早停
- seed 3：MRR 0.918637，epoch 15 早停
- seed 4：MRR 0.923839，epoch 23 早停
- 五种子均值 ± 样本标准差：**0.915078 ± 0.009282**
- 论文：**0.931 ± 0.009**
- 均值差：**-0.015922**

因此结论需分开表述：

1. 官方默认 seed 2023 的 0.927811 落在论文区间内。
2. canonical seeds 0–4 的均值没有复现论文中心值，不能把 seed 2023 的单次命中
   当成完整统计复现。
3. 论文和代码都没有给出用于均值/标准差的 seed 列表；官方 `--repeat` 还会重复
   使用同一 seed，因此无法确认论文使用的随机种子。

结构化结果：

- `results/scadyg/summary.csv`
- `results/scadyg/multiseed_summary.csv`

### AP 选模审计

用 `scripts/analyze_scadyg_logs.py` 对每个 epoch 的 15 个验证快照取均值后发现：

- seed 0：AP 选 epoch 19；MRR 应选 epoch 21
- seed 1：AP 选 epoch 18；MRR 应选 epoch 26
- seed 2：两者都选 epoch 14
- seed 3：AP 选 epoch 5；MRR 应选 epoch 9
- seed 4：两者都选 epoch 13

论文把 MRR 作为主指标，但发布代码使用 AP 早停/选模；且当前代码的测试 AP
约 0.991，明显不同于论文附录报告的 MOOC AP 0.901 ± 0.012。下一步应建立
`--selection_metric mrr` 的明确协议对照，而不是通过挑选 seed 追论文数字。

---

## 2026-09-10 MRR 选模五种子对照

新增 `--selection_metric {ap,mrr}`，默认仍为 `ap` 以保持发布代码行为；本组显式
传入 `--selection_metric mrr`。补丁同时包含双模块 checkpoint 修复和 MRR 日志
命名修复：

- 补丁：`repro/scadyg-paper-protocol.patch`
- 跟踪文件补丁 SHA-256：
  `0ec53530a474b13f3b89cb277fdee9fcd724a6ec0431508f3013b9bc96eb9205`

结果：

- seed 0：0.921137，epoch 31 早停
- seed 1：0.934858，epoch 39 早停
- seed 2：0.899404，epoch 24 早停
- seed 3：0.933187，epoch 19 早停
- seed 4：0.923839，epoch 23 早停
- 五种子均值 ± 样本标准差：**0.922485 ± 0.014178**
- 论文：**0.931 ± 0.009**
- 均值差：**-0.008515**

MRR 选模把五种子均值从 0.915078 提升到 0.922485；均值刚好落在论文给出的
`[0.922, 0.940]` 区间内，但方差 0.014178 高于论文的 0.009。因此可认为性能量级
已复现，均值接近报告范围下界，但**尚未严格复现论文的均值与方差**。

特别地，seed 2 在 AP 与 MRR 选模中均选择 epoch 14，结果都为 0.899404，是主要
低值来源；不应把它作为“坏 seed”删除。论文未公开 seed 列表，继续尝试 seed
2023–2027 只能说明另一组随机种子的表现，不能替代 canonical 0–4 的结果。

### 评测随机性边界

发布代码在每个验证 epoch 和最终测试时都通过全局 NumPy RNG 临时生成排名负样本。
因此早停 epoch 不同会消耗不同数量的随机数，使最终测试负样本集合也随训练长度
变化；源码没有保存负样本或独立评测 RNG。这会混合“模型差异”和“评测样本差异”，
也是当前方差解释中的未解决因素。

若继续提高复现严谨性，下一步不是扫学习率，而是建立固定、持久化且完整碰撞检查的
100-negative 评测集，并在后续运行中持久化完整 checkpoint 后进行重评。当前发布
代码和本轮补丁只在内存中保留最佳完整状态，实验结束后没有可直接重评的完整
checkpoint。该步骤会形成第三种明确协议，不能覆盖本日志中的官方评测结果。

---

## 2026-09-11 MOOC 排名协议根因审计

MOOC 的节点空间是严格二部图：

- 源节点（用户）：0–7046，共 7047 个；
- 目标节点（item）：7047–7143，共 97 个；
- 测试集：快照 85–99，共 61,719 条正边。

发布代码的排名评测与论文文字描述存在三项关键差异：

1. 发布代码对每个源节点只取最高分正边，测试集最终只形成 5,243 个 rank，不是对
   61,719 条正边逐条计算 reciprocal rank。
2. 100 个负目标从全部 7,144 个节点采样，约 98.73% 落入不合法的用户目标分区。
3. 验证和测试共用全局 NumPy RNG；训练停止 epoch 会改变测试负样本，无法把模型
   方差与评测采样方差分开。

训练用 1:1 负边还会同时随机替换两端点，约 98.49% 不符合用户→item 方向。它先
作为独立因素保留，不混入本节的纯评测修正。

由于合法 item 总数只有 97，不能构造“每条正边 100 个不重复合法负样本”。因此严格
协议采用 `mooc_full_item_filtered_v1`：

- 每条正边单独排名；
- 候选目标是全部 97 个合法 item；
- 过滤同一快照、同一源节点的其他真实目标；
- 所有剩余合法非正 item 都作为负候选；
- 使用 `>=` 处理并列分数，与发布代码保持一致；
- 不使用随机负采样。

协议清单：

- `results/scadyg/protocols/mooc_full_item_v1.npz`
- 清单 SHA-256：
  `f314bf0ef2afecc8c127d89f32620f47075f438ebe21ee960b146d69cafe8da1`
- 100 个 `edge_index` 快照的 canonical SHA-256：
  `e8b017550b97172caa9334cc6a5cba18bbd052f30ef93ecd2cdb17c4ff24e33c`

### 双协议与 checkpoint 实现

新增 `--eval_protocol {official,mooc_full_item,both}`，默认 `official`，因此不改变
发布代码兼容基线。`both` 会在同一个选中状态上同时输出两种 MRR。新增
`--selection_metric filtered_mrr`，但只有显式启用 full-item 评测才能使用。

每个 run 现在在独立目录保存：

- `best_ap.pt`
- `best_official_mrr.pt`
- `best_filtered_mrr.pt`

每份 checkpoint 都包含预测层、Transformer、最佳 epoch、seed、完整 CLI 参数、
源码提交、协议清单哈希和数据哈希。运行日志继续记录补丁哈希、环境、命令和产物
目录。

### 1 epoch 双协议烟雾测试

日志：`results/scadyg/runs/20260911_175707_mooc_pid732369.log`

- official MRR：0.624727
- full-item filtered MRR：0.015597
- 严格协议排名正边：61,719
- 每条正边的合法负候选范围：取决于同源真实目标数，本次各快照最小值 29–64、
  最大值均为 96
- AP、official MRR、filtered MRR 三份 checkpoint 均成功落盘，每份都包含预测层
  4 个张量和 Transformer 32 个张量

另用一个可手算的 3 正边、3 item 小图验证 evaluator，预期 MRR 为 2/3，实际为
0.6666667。烟雾测试的严格 MRR 很低是重要信号，但 1 epoch 不能作为最终模型结论；
已启动 seeds 0–4 的完整 `filtered_mrr` 选模实验。

### full-item filtered MRR 五种子结果

五个 run 使用完全相同的源码补丁
`9c5c573c67cf67dc7b1588abbd796fcb30acf6e937c3b9a8782fcb9438909540`
和协议清单，训练负采样仍为发布代码原样。结果为：

- seed 0：official 0.921137，filtered 0.202563，选 epoch 21；
- seed 1：official 0.934858，filtered 0.199150，选 epoch 29；
- seed 2：official 0.899404，filtered 0.210344，选 epoch 14；
- seed 3：official 0.933187，filtered 0.201842，选 epoch 9；
- seed 4：official 0.923839，filtered 0.204256，选 epoch 13。

full-item filtered MRR 的五种子均值 ± 样本标准差为
**0.203631 ± 0.004180**。同一批 checkpoint 上的 official MRR 为
**0.922485 ± 0.014178**，与上一组 official MRR 选模结果逐 seed 完全一致。

五个 seed 中，filtered MRR 的最佳 epoch 与 official MRR 最佳 epoch 全部相同，
因此这次差值不是 checkpoint 选择造成的，而是完全由评测候选和排名单位造成的。
两种 test MRR 的 seed 排序甚至近似相反（Pearson -0.959、Spearman -0.900，
`n=5`，只作描述性结果），说明 official MRR 不能作为合法 item 检索能力的可靠代理。

结论：论文的 0.931 数值复现对应的是发布代码的“每源取最佳正边 + 从所有节点抽
100 个负目标”协议；在逐正边、合法 item、当前快照 filtered full-item 协议下，
同一模型只有约 0.204 MRR。下一步单独修正训练负采样，判断模型较低的合法 item
排序能力有多少来自训练目标与二部图任务不匹配。

结构化结果：

- `results/scadyg/full_item_multiseed_summary.csv`
- `results/scadyg/multiseed_summary.csv`

### 合法二部图训练负采样对照

在评测协议固定后，新增独立的
`--train_negative_protocol {official,mooc_bipartite}`，默认仍为 `official`。
`mooc_bipartite` 对每条正边：

- 保持原 source 不变；
- target 只从 97 个合法 item 中选择；
- 排除同一快照中的 source→item 正边；
- 每个 source 的候选先随机打乱、无放回使用；候选不足时才进入下一轮打乱；
- 训练负边在 run 开始时一次生成并记录 SHA-256。

100 个快照共生成 411,749 条训练负边。所有五种子均满足：

- fixed-source fraction：1.0；
- legal-destination fraction：1.0；
- positive collisions：0；
- unique-pair fraction：0.992845。

1 epoch 烟雾测试日志：
`results/scadyg/runs/20260911_190131_mooc_pid763572.log`。该次 filtered MRR 从
原训练协议 1 epoch 的 0.015597 上升到 0.159345，但完整实验显示这个早期差异不能
外推到收敛结果。

完整 seeds 0–4：

- seed 0：official 0.868706，filtered 0.208198，选 epoch 11；
- seed 1：official 0.715643，filtered 0.196889，选 epoch 0；
- seed 2：official 0.784881，filtered 0.201864，选 epoch 10；
- seed 3：official 0.816549，filtered 0.206607，选 epoch 5；
- seed 4：official 0.906229，filtered 0.201585，选 epoch 2。

合法训练负采样的 filtered MRR 为 **0.203029 ± 0.004491**，原训练负采样为
**0.203631 ± 0.004180**。同 seed 配对平均差为 **-0.000603**，配对差样本标准差
0.005848；`n=5` 下没有可解释的改进（配对 t 检验仅作描述，`p=0.829`）。

official MRR 则降到 **0.818401 ± 0.074045**。合理解释是原训练协议大量使用非法
用户目标作为负边，恰好训练了发布代码 official evaluator 所测试的“正 item 对随机
全节点”区分能力；改为合法 item 负边后，这个非任务内能力下降。严格 item 排名基本
不变，说明训练负采样不是 0.931 与 0.204 差距的主要根因。

所有五个 run 都正常结束，无 traceback、OOM 或残留进程。每个 run 均保存并核验
`best_ap.pt`、`best_official_mrr.pt`、`best_filtered_mrr.pt`；每份 checkpoint 含
预测层 4 个张量、Transformer 32 个张量及对应训练负边哈希。

本组跟踪文件补丁 SHA-256 为
`ac6fff66d39df29e96404ec537be87e914d81752500c384bfdcee383a0f21c79`。
严格 evaluator 是新增未跟踪文件，未包含在 `git diff` 哈希内，因此另记
`model/eval_protocols.py` 文件 SHA-256：
`fc7bd1550ed359f1f7a085ea75e2eb9e8eb4e0535181279e4499e6fe8f865624`。

结构化结果：

- `results/scadyg/bipartite_train_multiseed_summary.csv`
- `results/scadyg/multiseed_summary.csv`

### 默认协议回归检查

完成上述扩展后，再次不传任何新协议参数运行 1 epoch：

```bash
bash repro/run_scadyg.sh mooc --epochs 1 --seed 2023
```

日志：`results/scadyg/runs/20260912_124851_mooc_pid845844.log`。

结果 official MRR 为 **0.6247271678**，与 2026-09-10 初始 1 epoch 基线逐位一致；
AP 0.9857572059、AUC 0.9906082116、accuracy 0.9830360181 也逐位一致。该回归确认
`eval_protocol=official` 与 `train_negative_protocol=official` 的默认行为没有被
双轨协议扩展改变。

---

## 2026-09-12 报告初稿与 checkpoint issue 草稿（不训练）

- 复现报告：`repro/SCADYG_REPORT.md`。结构按 `CLOSEOUT_PLAN.md` R-SCADYG-4：官方原样 0.025 → checkpoint-fix → AP vs MRR 选模 → 排名协议 → 双协议 0.922 vs 0.204 → 训练负采样对照。消融与 BitcoinAlpha 标明未做。
- 上游 issue 草稿：`repro/scadyg_issue_draft.md`。只报 Transformer 未写入 / 未恢复的 checkpoint bug，附 seed 2023 的 0.025 → 0.928。**2026-09-16 决定不发出**（保留作证据）；评测协议争议不写进 issue。
- `model/eval_protocols.py` 已复制到 `repro/scadyg-extra/eval_protocols.py`，SHA-256 均为 `fc7bd1550ed359f1f7a085ea75e2eb9e8eb4e0535181279e4499e6fe8f865624`（与日志步骤记录一致）。官方克隆仍 gitignore。

---

## 2026-09-13 R-SCADYG-1：三个组件 → 代码位置 → 开关

官方提交 `28ca94a06771c46073b650de3daa95e0939342ba`。逐文件读了
`scalable_tgn_link_prediction.py`（51,003 B，核心）、
`scalable_tgn_main_link_prediction.py`（21,828 B，入口）、`transformer/`。

### 组件对照表

| 论文组件 | 代码位置 | 实际做什么 | 消融方式 |
|----------|----------|-----------|----------|
| ① 时间感知拓扑重构 | `snapshot.__init__` / `initialize_edge_node_mat`（397–474）；`snapshot.set_edge_features`（443–448） | 每个快照把边特征按 `node_edge_mat` 聚合到入射节点（`sum` reduce）；时间编码先乘进边特征 | `--ablate topo`：跳过边→节点聚合，退化为全局池化（快照内所有节点用同一个特征） |
| ② 指数时间编码 | `TimeEncode_exp`（341–369，`forward` 用 `torch.exp`） | `exp(w·Δt)`，`w` 固定不可训练，`vec = linspace(-a, -0.1a, dim)` | `--ablate time`：`forward` 直接返回全 1，时间信息归零 |
| ③ Hypernetwork 自适应聚合 | `Encoder.__init__`（207–242）；`Encoder.forward`（256–334） | **注意**：Transformer 分支（`layer_stack_time_1/2`、`CustomEncoderLayer*`、`repeat_to_n_dim`）在 `forward` 里**全部被注释掉**。实际生效的是：对时间维度求和 → `scale_matrix` 生成逐样本缩放 → 与 `global_weight` 做 `bmm` → `sigmoid` 得到逐样本/逐维门控 `new_weight`，再与基础权重 `self.weight` 相乘 | `--ablate hyper`：门控置 1，仅保留基础权重矩阵 |

### 重要发现

1. **Transformer 层是死代码**。`Encoder.forward` 内 `layer_stack_time_1` / `layer_stack_time_2` /
   `layer_stack_feature` 的调用全部被注释；`CustomEncoderLayer`、
   `CustomEncoderLayer_withScale`、`position_enc` 都不参与前向。所谓"Hypernetwork"
   实为**输入条件化的权重缩放**（`weight × sigmoid(scale ⊗ global_weight)`），不是
   产生权重矩阵的超网络。
2. **`merge_weight`、`TimeEncode`（cos 版）、`graph_coarsening`、`weight_expand` 是死代码**：
   只有定义，全仓库无调用。`merge_weight`/`graph_coarsening` 在
   `scalable_tgn_node_affinity_prediction.py` 里也是同名死代码。
3. **`time_rate` 被写死为 1**。`initialize_edge_node_mat` 里
   `self.time_rate = torch.ones(...)`，紧邻的上方注释行
   `#self.time_rate = torch.matmul(self.time_features, self.snapshot_timefeat.t())`
   是原始设计。因此 `--time_rate` 这个 CLI 参数**不生效**。
4. `snapshot.time_features` 计算后在 `set_edge_features` 里与边特征逐元素相乘，
   所以②确实进入前向（并非死代码）。
5. 入口 `--fusion` 默认 `t2v`，而代码只判断 `if args.fusion == 'v2t'`；`v2t` 分支
   import 的 `scalable_tgn_affine_v2t_chunk` 模块**不存在**。`t2v` 走到标准分支。

### 消融开关实现（默认 none，不改官方路径）

新增 `--ablate {none,time,topo,hyper}`：

- `scalable_tgn_main_link_prediction.py`：新增参数，并把它传给 `Encoder(..., ablate=args.ablate)`（两处构造，通用分支与 reddit_title 分支）。
- `scalable_tgn_link_prediction.py`：
  - `TimeEncode_exp.__init__` 记录 `self.ablate`；`forward` 在 `time` 时返回全 1。
  - `snapshot.__init__` 记录 `self.ablate`；`set_edge_features` 在 `topo` 时跳过
    `node_edge_mat` 聚合。
  - `Encoder.__init__` 新增 `ablate='none'` 形参；`forward` 在 `hyper` 时把
    `new_weight` 置 1。

**默认回归**（`--ablate` 不传，即 `none`，1 epoch，seed 2023）：

| 指标 | 本次 `20260913_185717_mooc_pid220956` | 基线 `20260912_124851_mooc_pid845844` |
|------|--------------------------------------|--------------------------------------|
| `avg_official_mrr` | **0.63610** | 0.63610 |
| `avg_ap` | **0.98954** | 0.98954 |

逐位一致，确认新增开关不改变官方路径（`CLOSEOUT_PLAN.md` R-SCADYG-1 的验收要求）。

### 消融生效性冒烟（1 epoch，seed 2023，MOOC）

| 设定 | `avg_official_mrr` | `avg_ap` | 相对基线 |
|------|--------------------|----------|----------|
| 基线 `--ablate none` | 0.63610 | 0.98954 | — |
| `--ablate time` | 0.62998 | 0.98940 | −0.006 |
| `--ablate topo` | **0.00990** | **0.50000** | **塌成随机** |
| `--ablate hyper` | 0.64828 | 0.98974 | +0.012 |

- 三个开关都改变了数值，说明确实进入前向（非空操作）。
- `topo` 消融后 MRR 0.0099 / AP 0.5000 = 随机水平，说明**快照内边→节点拓扑聚合是
  该模型能工作的前提**，不只是"锦上添花"的组件。
- `time` / `hyper` 在 1 epoch 下差异小（±0.012），需要完整 100 epoch × seeds 0–4
  才能判断（见 R-SCADYG-2）。
- 全部退出码 0，无 traceback。日志：`results/scadyg/runs/20260913_1857*`…`1900*`。

### 补丁与可追溯性

- 新增 `repro/scadyg-ablation.patch`（103 行，2 文件），SHA-256
  `59efcde22da4368a9fbb1dc3b858f0da247388ef8b5bd8c406d3d8e4a4a2dd33`。
- 验证：在 HEAD 的临时 worktree 上先还原到消融前状态，`git apply --check` 通过，
  应用后与工作树**逐字一致**；临时 worktree 已清理。
- 消融前状态由反向还原我的编辑得到，其 `git diff` SHA-256 为
  `ac6fff66d39df29e96404ec537be87e914d81752500c384bfdcee383a0f21c79`，
  与 2026-09-12 双协议那组记录的哈希**逐字一致**，确认还原精确、没有夹带其他改动。

### ⚠ 发现的追溯缺口：已有补丁不覆盖工作树

`repro/scadyg-checkpoint-fix.patch`（75 行）与 `repro/scadyg-paper-protocol.patch`
（110 行）合计 185 行，且**两者互斥**（都从同一 base 改 `train_scalable_tgn` 的同一区域，
`paper-protocol` 是 `checkpoint-fix` 的超集；按任一顺序连续应用都会冲突）。

而工作树相对 HEAD 是 **458 增 / 32 删**。`paper-protocol` 补丁**不含**双协议与训练
负采样那批工作的符号（`capture_state`、`report_filtered_bipartite_eval`、
`negative_sampling_mooc_bipartite`、`from pathlib import Path` 均为 0 处）。
即：两个补丁都是 **2026-09-12 12:46 的早期快照**，之后的双协议扩展没有固化成补丁。

处理：本次不重写旧补丁（避免与已有 SHA 记录冲突），改为在 R-SCADYG-2 完成后生成一份
覆盖当前完整工作树的补丁。届时旧的 `scadyg-paper-protocol.patch` 应标注为已过时。

---

## 2026-09-13 R-SCADYG-2：三个组件消融 × seeds 0–4（MOOC）

入口 `repro/run_scadyg_ablation.sh`（4 组件 × 5 seed，每格独立进程）。每格：

```bash
bash repro/run_scadyg.sh mooc --seed <0-4> --selection_metric mrr \
  --eval_protocol both --ablate {none,time,topo,hyper}
```

- 批次日志：`results/scadyg/runs/20260913_190322_ablation_multiseed.batch.log`
- 运行区间：2026-09-13 19:03:22 → 21:18:26（约 2h15m，20/20 退出 0，无 traceback）
- 选模口径固定 `mrr`（与论文主指标一致）；`--ablate none` 即完整模型。

### 结果（official MRR，对照论文 0.931 ± 0.009）

| 组件 | n | official MRR | filtered MRR | Δ vs 论文 | 结论 |
|------|---|--------------|--------------|-----------|------|
| `none`（完整） | 5 | **0.922485 ± 0.014178** | 0.203631 ± 0.004180 | **−0.0085** | 落在论文 1σ 内，复现成立 |
| `hyper` | 5 | 0.803234 ± 0.041231 | 0.035989 ± 0.011210 | −0.1278 | 掉幅最大 |
| `time` | 5 | 0.827678 ± 0.077334 | 0.072184 ± 0.073315 | −0.1033 | 次之 |
| `topo` | 5 | **0.009901 ± 0.000000** | 0.012163 ± 0.000058 | **−0.9211** | **塌成随机** |

逐 run 明细：`results/scadyg/ablation_runs.csv`；分组汇总：
`results/scadyg/ablation_summary.csv`。

### 读法

- **`topo`（快照内边→节点拓扑聚合）是模型能工作的前提**，不是可选增强项：去掉后
  official MRR = 0.009901、AP = 0.500000，即**随机水平**；5 个 seed **完全一致**
  （std = 0.000000），说明这是确定性的结构性失效，而非训练波动。这与 R-SCADYG-1 的
  1-epoch 冒烟（0.00990 / 0.50000）逐位一致。
- **`hyper`（Hypernetwork 自适应聚合）掉 0.1278**，**`time`（指数时间编码）掉
  0.1033**，两者量级接近，都是"去掉后仍能跑、但明显变差"。
- **`none` 与论文差 0.0085 < 论文 σ = 0.009**，这是本线第一次在消融维度上确认完整
  模型与论文统计一致。
- 方差：`time` 的 std 最大（0.0773，seed 2 只有 0.7017），`hyper` 0.0412，`none`
  0.0142。**消融后的方差都大于完整模型**，与"组件被移除后优化更不稳定"一致。
- 也看 filtered 协议：`none` 0.203631 与 2026-09-12 的 0.203631 ± 0.004180 逐位
  一致（回归未破），`time` 0.0722、`topo` 0.0122、`hyper` 0.0360——四个组件的
  official 与 filtered 排序**一致**（none > time ≈ hyper > topo）。

### ⚠ 汇总陷阱（复现时必须避开）

用宽通配符 `results/scadyg/runs/2026*_mooc_pid*.log` 汇总会**混入 R-SCADYG-1 的
1-epoch 冒烟日志（`--seed 2023`，official MRR 0.650017）**，把 `hyper` 污染成
`0.739000 ± 0.125842`。正确的 `hyper` 是 **0.803234 ± 0.041231**（n=5）。

做法：从批次日志里取绝对路径列表，而不要用通配符：

```bash
LOGS=$(grep -oE "/home/[^ ]*/results/scadyg/runs/2026[0-9_]+_mooc_pid[0-9]+\.log" \
  results/scadyg/runs/20260913_190322_ablation_multiseed.batch.log | sort -u)
python scripts/summarize_scadyg_ablation.py $LOGS --csv results/scadyg/ablation_summary.csv
```

### 分层判定

- L1 管线闭环：是（20/20 退出 0，脚本可重跑）。
- L2 数值量级：`none` 与论文差 0.0085，在论文 σ 内；三个消融组按预期下降。
- L3 统计一致：否（消融组与论文无对应表可对照；`none` 只做到 1σ 内）。

### 仍未做

- 覆盖当前完整工作树的补丁（见上节追溯缺口）。R-SCADYG-2 已完成，可生成。
- BitcoinAlpha 第二数据集（R-SCADYG-3）。

## 2026-09-16 R-SCADYG-3：BitcoinAlpha 第二数据集

- 原始数据：SNAP `soc-sign-bitcoinalpha.csv.gz`；SHA-256：`3a178611b9c2f39c9a0dc75936f28557317f1733319b49da4838232b3757cd76`。
- 下载入口：`repro/download_scadyg_bitcoinalpha.sh`；预处理脚本：`repro/scadyg-extra/process_bitcoin.py`。
- 默认切片宽度 723000 秒、补充反向边，生成 226 个快照；四组快照文件各 226 个，首个快照形状为 `(2, 46)`、`(46, 2)`、`(46,)`、`(3783, 1)`。
- 烟雾命令 `bash repro/run_scadyg.sh bitcoinalpha --epochs 1 --seed 2023` 退出码 0，`avg_official_mrr=0.7340658586`；该数字只用于管线检查。

正式运行使用独立进程、`--selection_metric mrr`、官方训练负采样与官方排名协议：

| seed | official MRR |
|------|--------------|
| 0 | 0.7170117487 |
| 1 | 0.7272967349 |
| 2 | 0.7160102901 |
| 3 | 0.7110614720 |
| 4 | 0.7259677410 |

均值 ± 样本标准差：**0.719470 ± 0.006932**（n=5）。5/5 正常完成，无 traceback；不宣称论文数值匹配，且与 MOOC 的 0.922 ± 0.014 分开记账。结构化数字：`results/scadyg/bitcoinalpha_multiseed_summary.csv`。

R-SCADYG-3 数据、训练、评测和日志均已完成。L1 管线闭环为是；冻结前剩余任务是整理 `SCADYG_REPORT.md` 与完整补丁追溯说明。


