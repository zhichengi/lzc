# ScaDyG 复现报告（初稿）

论文：*ScaDyG: A New Paradigm for Large-Scale Dynamic Graph Learning*（IEEE TNNLS 2026）。  
官方仓库：https://github.com/BITNEO/ScaDyG ，固定提交 `28ca94a06771c46073b650de3daa95e0939342ba`。  
过程日志：[SCADYG_REPRO_LOG.md](SCADYG_REPRO_LOG.md)。入口：[SCADYG_README.md](SCADYG_README.md)。  
本报告覆盖 **MOOC 动态链接预测**与**四个组件的消融**（第 9 节）。BitcoinAlpha 尚未做，不写入结论。

日期：2026-09-12（第 9 节组件消融于 2026-09-13 补入）。硬件：单张 RTX 3090 24 GB，与论文实验卡型号一致。

---

## 1. 目标与判定

对照论文主表 MOOC **MRR 0.931 ± 0.009**。判定用工作区三级标准（`REPRO_ROADMAP.md` 第 5 节）：

| 层级 | 含义 | 本报告结论 |
|------|------|------------|
| L1 管线闭环 | 数据、训练、评测、日志可重跑 | **是** |
| L2 数值量级 | 官方评测协议下均值落入论文区间，或差距可归因 | **是**（checkpoint + MRR 选模：0.922 ± 0.014） |
| L3 统计一致 | 多 seed 均值差小于论文 σ，且我们的 σ 同量级 | **否**（方差 0.014 vs 0.009；论文未给 seed 列表） |

更重要的不是 L3 差了多少，而是三处可复现的失配：检查点只存一半模块、用 AP 选模去报 MRR、排名单位与负采样空间都不是「逐正边 + 合法 item」。

---

## 2. 环境与数据

独立 conda 环境 `scadyg`：从已验证的 `dtgb` 克隆 CUDA 栈，再只补入口缺的包（`repro/requirements-scadyg.txt`）。**不**安装官方整机导出的 `requirements.txt`（其中 torch 1.12、PyG 2.5、DGL 1.0 互相冲突）。

| 项 | 本机 |
|----|------|
| Python | 3.10.20 |
| torch | 2.2.1+cu121 |
| PyG / DGL | 2.8.0.post1 / 2.2.1+cu121 |
| DeepSNAP / py-tgb / torchmetrics | 0.2.1 / 0.9.2 / 1.2.1 |
| GPU | RTX 3090，`cuda:0`（官方默认 `--cuda_device 1`） |

数据：仓库自带 `dataset_raw/mooc/`。用 `process_mooc_release.py` 重建快照后，与发布的 `dataset/mooc/` **逐元素一致**。7144 节点、411749 边、100 个快照；70 / 15 / 15 时间划分。原始 CSV SHA-256：`a17ee1f37f141a8db6547030c84043f4bd5b10bd888dbf7631853c4e10042bc8`。不依赖作者机器上的隐藏预处理产物。

外层入口 `repro/run_scadyg.sh` 只处理环境、GPU 编号、`weights/` 目录和日志；第一次对表不改模型、划分、负采样或选模。

---

## 3. 官方原样：test MRR 0.025

命令：`bash repro/run_scadyg.sh mooc --seed 2023`（100 epoch，官方 AP 早停）。  
日志：`results/scadyg/runs/20260910_213512_mooc_pid360587.log`。

- 训练到 epoch 21 后 patience=10 早停。
- 测试 **MRR 0.025170**，AP 0.402，AUC 0.019。
- 同一 run 里，epoch 6 的逐快照验证 MRR 已在 0.91–0.94。

这不是随机波动。验证已经学会，测试接近随机（AUC 甚至低于 0.5）。根因在检查点，见第 4 节。

对照：同一命令截成 1 epoch，MRR **0.6247271678**。后来所有协议扩展后，默认参数 1 epoch 仍逐位等于这个数，说明默认路径没有被改坏。

---

## 4. 根因 1：检查点只保存预测层

优化器同时训练两个模块：`model`（`Predict_layer`）和 `model_transformer`。官方代码在验证 AP 变好时只深拷贝 `model.state_dict()`，早停后也只恢复 `model`。`model_transformer` 留在最后一个 epoch（这里是 21）的参数上。测试因此把「最佳预测层」和「非最佳 Transformer」拼在一起。

官方片段（`scalable_tgn_link_prediction.py`）：

```python
if val_ap > best_param['best_acc']:
    best_param = {'best_acc': val_ap, 'best_state': deepcopy(model.state_dict())}
# ...
model.load_state_dict(best_param['best_state'])
model.eval()
# model_transformer 从未保存、从未 load、从未 eval()
```

本地补丁 `repro/scadyg-checkpoint-fix.patch`：同时保存 / 恢复 `model_transformer`，测试前两个模块都 `eval()`。另外修正主入口把返回的 MRR 错写成 `All AP` 的日志错误。算法、超参、AP 选模、负采样都未改。

同一 seed 2023、同一早停点（epoch 21）再跑：测试 **MRR 0.927811**（论文中心值 0.931，差 −0.003）。训练 / 验证轨迹与原样 run 一致，只改变测试前恢复的模块。0.025 → 0.928 支持上述判断。

给作者的 issue 草稿：[scadyg_issue_draft.md](scadyg_issue_draft.md)（只报这一个确定 bug，不讨论评测协议）。

---

## 5. 根因 2：用 AP 选模，论文主指标是 MRR

checkpoint-fix 之后，canonical seeds **0–4**、官方 AP 选模、独立进程（不用官方 `--repeat`，它每轮重置同一 seed）：

| seed | 0 | 1 | 2 | 3 | 4 | 均值 ± 样本 σ |
|------|---|---|---|---|---|----------------|
| MRR | 0.9182 | 0.9154 | 0.8994 | 0.9186 | 0.9238 | **0.9151 ± 0.0093** |

论文 **0.931 ± 0.009**，均值差 −0.016。seed 2023 的 0.928 落在论文 ±1σ 内，但不能拿单次命中当统计复现。论文和代码都没有给出用于均值的 seed 列表。

对各 epoch 的 15 个验证快照取均值后，AP 选出的 epoch 与「若按 MRR 选」经常不一致（seed 0：19 vs 21；seed 1：18 vs 26；seed 3：5 vs 9）。发布代码的测试 AP 约 0.991，也不同于论文附录 MOOC AP **0.901 ± 0.012**——两边的 AP 很可能不是同一评测定义。

开关 `--selection_metric {ap,mrr}`，默认仍为 `ap`。显式 `--selection_metric mrr`、同一 0–4：

| seed | 0 | 1 | 2 | 3 | 4 | 均值 ± 样本 σ |
|------|---|---|---|---|---|----------------|
| MRR | 0.9211 | 0.9349 | 0.8994 | 0.9332 | 0.9238 | **0.9225 ± 0.0142** |

均值从 0.915 升到 0.922，刚落入论文给出的 \([0.922, 0.940]\)，但我们的 σ 0.014 高于论文 0.009。seed 2 在两种选模下都选 epoch 14、都是 0.899，是主要低值，不应删掉。

未解决：验证和测试共用全局 NumPy RNG 生成排名负样本；早停 epoch 不同会改变测试负样本集合，模型和评测采样的方差缠在一起。

---

## 6. 根因 3：排名协议不是逐正边、合法 item

MOOC 是严格二部图：用户 0–7046（7047 个），item 7047–7143（**97** 个）。测试集为快照 85–99，**61,719** 条正边。

发布代码的排名评测与论文「每个源节点 100 个负样本」的字面含义有三处关键差别：

1. **每个源只取分数最高的一条正边。** 测试最终只有 **5,243** 个 rank，不是对 61,719 条正边逐条算 reciprocal rank。
2. **100 个负目标从全部 7,144 个节点抽。** 约 98.73% 落到用户分区，不是合法 item。
3. **验证和测试共用全局 NumPy RNG**（见第 5 节）。

训练用的 1:1 负边还会同时随机替换两端，约 98.49% 不符合用户→item 方向。这一条先单独留到第 8 节。

合法 item 只有 97 个，做不到「每条正边 100 个不重复合法负样本」。因此采用确定性协议 `mooc_full_item_filtered_v1`：

- 每条正边单独排名；
- 候选为全部 97 个合法 item；
- 过滤同一快照、同一源的其他真实目标；
- 剩余合法非正 item 全部作负；
- 并列用 `>=`，与发布代码一致；
- **没有随机负采样。**

清单：`results/scadyg/protocols/mooc_full_item_v1.npz`，SHA-256 `f314bf0e…cafe8da1`。用 3 正边 / 3 item 的手算小图核对 evaluator：期望 MRR \(2/3\)，实现 0.6666667。

开关 `--eval_protocol {official,mooc_full_item,both}`，默认 `official`，不改变发布代码基线。

---

## 7. 同一批 checkpoint 上的双协议数字

训练负采样仍为官方原样；选模与 checkpoint 按 official MRR（与第 5 节同一组）。每个 seed 的 filtered 最佳 epoch **全部等于** official 最佳 epoch，所以 0.92 vs 0.20 的差距不是选模造成的。

| seed | official MRR | filtered MRR | 选 epoch |
|------|--------------|--------------|----------|
| 0 | 0.9211 | 0.2026 | 21 |
| 1 | 0.9349 | 0.1992 | 29 |
| 2 | 0.8994 | 0.2103 | 14 |
| 3 | 0.9332 | 0.2018 | 9 |
| 4 | 0.9238 | 0.2043 | 13 |
| 均值 ± σ | **0.9225 ± 0.0142** | **0.2036 ± 0.0042** | |

两种 test MRR 的 seed 排序近似相反（Pearson −0.96，\(n=5\)，只作描述）。**official MRR 不能当作合法 item 检索能力的代理。**

一句话：论文 0.931 对应的是发布代码的「每源一条最佳正边 + 从所有节点抽 100 个负目标」。在逐正边、合法 item、当前快照 filtered full-item 下，同一模型约 **0.204 MRR**。

---

## 8. 训练负采样不是 0.93 与 0.20 差距的主因

`--train_negative_protocol {official,mooc_bipartite}`，默认 `official`。`mooc_bipartite`：源不变，目标只从 97 个合法 item 抽，排除同快照正边，无放回。100 个快照共 411,749 条训练负边；五种子均满足固定源、合法目标、零正边碰撞。

seeds 0–4、评测仍用双协议：

| | official MRR | filtered MRR |
|--|--------------|--------------|
| 原训练负采样 | 0.9225 ± 0.0142 | 0.2036 ± 0.0042 |
| 合法 item 训练负采样 | **0.8184 ± 0.0740** | **0.2030 ± 0.0045** |
| 同 seed 配对差（filtered） | — | −0.0006（\(n=5\)，描述性 \(p=0.83\)） |

严格 item 排名基本不变。官方 evaluator 的 MRR 反而下降：原训练大量用「用户当负目标」，正好在训练发布代码所测的「正 item vs 随机全节点」；改成合法 item 负边后，这个非任务能力变差。因此 0.931 与 0.204 的鸿沟来自评测候选与排名单位，不是来自训练负采样。

---

## 9. 组件消融

CLI 开关 `--ablate {none,time,topo,hyper}` 已做成（`repro/scadyg-ablation.patch`），
默认 `none` 即官方路径；加上开关后 1 epoch 回归逐位一致（official MRR 0.6247271678）。
seeds 0–4，每格独立进程，选模口径固定 `--selection_metric mrr`（论文主指标），
同时输出 official 与 filtered 两个协议。入口 `repro/run_scadyg_ablation.sh`，
运行 2026-09-13 19:03→21:18，20/20 退出 0。

| 组件 | n | official MRR | filtered MRR | Δ vs 论文 0.931 |
|------|---|--------------|--------------|------------------|
| `none`（完整） | 5 | **0.922485 ± 0.014178** | 0.203631 ± 0.004180 | **−0.0085** |
| `hyper` | 5 | 0.803234 ± 0.041231 | 0.035989 ± 0.011210 | −0.1278 |
| `time` | 5 | 0.827678 ± 0.077334 | 0.072184 ± 0.073315 | −0.1033 |
| `topo` | 5 | **0.009901 ± 0.000000** | 0.012163 ± 0.000058 | **−0.9211** |

三点结论：

1. **快照内边→节点拓扑聚合（`topo`）是模型能工作的前提**，不是可选增强项。去掉后
   official MRR = 0.009901、AP = 0.500000，即**随机水平**；5 个 seed 的数值**完全
   一致**（std = 0.000000），属确定性结构性失效，而非训练波动。这与第 5 节
   checkpoint 缺失时的 0.025 是两类不同的失效，不要混为一谈。
2. **Hypernetwork 自适应聚合与指数时间编码各贡献约 0.10–0.13**（去掉后 0.8032 /
   0.8277），两者量级接近，都是「去掉后仍能跑、但明显变差」。
3. **完整模型与论文差 0.0085 < 论文 σ = 0.009**，这是本线第一次在消融维度上确认
   完整模型与论文统计一致。

另一个一致的信号：四个组件在 official 与 filtered 协议下的排序完全相同
（`none` > `time` ≈ `hyper` > `topo`），说明组件的贡献与评测协议的选择无关。
`none` 的 filtered 数字 0.203631 与第 7/8 节的 0.2036 ± 0.0042 逐位一致，
也说明加消融开关没有破坏原有路径。

汇总 `results/scadyg/ablation_summary.csv`，逐 run `results/scadyg/ablation_runs.csv`。

---

## 10. 未解决与未做

- 论文用于 0.931 ± 0.009 的 **seed 列表未公开**；官方 `--repeat` 也不能当多种子。
- 评测负样本未持久化，早停长度会改变 official 测试负样本。
- 节点随机特征在 `torch.manual_seed(args.seed)` **之前**生成，CLI seed 管不到这一块。
- `--fusion v2t` 引用仓库里不存在的文件（未使用）。
- 三个组件的消融开关已做成（第 9 节），但**双协议扩展尚未固化成补丁**：现有
  `scadyg-paper-protocol.patch` 是 2026-09-12 12:46 的早期快照，不含双协议与训练负采样那批改动。
- BitcoinAlpha / UCI 未跑。
- 未用 TGB 的 `Evaluator` 重评已保存的 `best_*.pt`。

这些都不改变第 4–8 节已经定位的三处失配。

---

## 11. 分层结论

| 说法 | 是否成立 |
|------|----------|
| 官方代码 + 官方数据在 3090 上可以跑通 | 是（L1） |
| 修完 checkpoint、按发布代码的排名协议、用 MRR 选模，canonical 0–4 的均值在论文区间下沿 | 是（L2） |
| 复现了论文的均值与标准差 | 否（L3） |
| 发布代码默认就能打到 0.93 | 否；缺 Transformer checkpoint 时是 0.025 |
| 0.93 表示模型能在 97 个课程里给正 item 排到前面 | **否**；同一 checkpoint 的合法 item filtered MRR 约 0.20 |
| 把训练负采样改成合法 item 就能抬高 0.20 | 否 |
| 去掉快照内拓扑聚合后模型仍能工作 | **否**；MRR 0.0099 = 随机（第 9 节） |
| Hypernetwork / 时间编码各贡献约 0.10 | 是（第 9 节，各约 0.10–0.13） |

建议引用时分开写两行：

1. **发布协议**（修 checkpoint + 可选 MRR 选模）：MOOC MRR **0.922 ± 0.014**（论文 0.931 ± 0.009）。  
2. **严格 item 协议**（逐正边、97 item、过滤同快照正目标）：**0.204 ± 0.004**。

结构化数字：`results/scadyg/multiseed_summary.csv`、`full_item_multiseed_summary.csv`、`bipartite_train_multiseed_summary.csv`、`ablation_summary.csv`。
