# 29 SGPC（AAAI 2026）

*Sheaf Graph Neural Networks via PAC-Bayes Spectral Optimization*。Choi, Choi, Ko, Kim, Kim。
arXiv 2508.00357；DOI 10.1609/aaai.v40i25.39193。复现日志：`repro/SGPC_REPRO_LOG.md`。

## 一句话

针对异配图上的过平滑与泛化差，把每条边配一个由最优传输权重决定的 sheaf 限制映射，
在 sheaf 拉普拉斯上做隐式扩散（CG 求解）+ 多项式频率混合，再用 PAC-Bayes 界（边一致性的
β 后验 KL）和谱间隙作正则；9 个基准上异配集提升明显（Actor 38.1、Squirrel 36.0、Wisconsin 81.1），
同配集与 SOTA 持平。

## 方法拆解（论文 → `main.py`）

| 论文组件 | 代码位置 | 实际做法 |
|----------|----------|----------|
| Wasserstein–Entropic Sheaf Lifting | `sinkhorn_simple` / `jko_refine` / `W_sheaf` | 边代价 \(C_{ij} = \|W(h_i - h_j)\|^2\)；权重 \(w = 0.7\,e^{-C/\varepsilon} + 0.3\,e^{\log e^{-C/\varepsilon} - C/\varepsilon}\)，两处都 clamp 到 [1e-3, 1]。没有 Sinkhorn 迭代归一化 |
| Sheaf 拉普拉斯 | `build_sheaf_laplacian` | 限制映射 \(R_{ij} = w_{ij}\,W h_i\)，边权取 \(\mathrm{mean}(R_{ij}^2)\)；实际是**标量加权图拉普拉斯**，不是矩阵值 sheaf |
| SVR（隐式扩散） | `conjugate_gradient` | 解 \((I + \Delta t L) H = h\)，CG 10–20 步 |
| AFM（自适应频率混合） | `afm_branch` | 归一化 \(\tilde L\) 的切比雪夫多项式 \(T_0..T_3\)，softmax 权重 `gamma` |
| 融合 | `forward` | \(h + \sigma(\alpha_{svr}) H_{svr} + \sigma(\alpha_{afm}) H_{afm}\)，α 初值 −4（Chameleon −8） |
| 分类头 | `GATConv`×2（同配）/ MLP（异配） | 同配用 GAT，异配用 MLP |
| PAC-Bayes β–Dirichlet 校准 | `estimate_edge_posterior` / `beta_kl` | 边两端预测分布点积作"一致性"，Beta(1+agree, 1+1−agree) 对 Beta(1,1) 的 KL；损失 \(\sqrt{(\bar{KL} + \log(2/\delta)) / 2n}\)，\(\delta = 0.1\) |
| 谱间隙优化 | `spectral_gap_from_sparse` / `heterophily_penalty` | \(\lambda_2\) 用稠密 `eigvalsh`（detach，不反传）；异配惩罚 = 类间一致性矩阵的 Frobenius 范数 / \(\lambda_2\) |
| 正则开始时机 | `pacbayes_epoch = 300` | 前 300 epoch 只有 NLL |

## 实验协议

| 项 | 论文 | 代码 |
|----|------|------|
| 划分 | 每类 20 个随机训练节点，其余 val/test | PyG 自带：Planetoid public；异配集 geom-gcn 60/20/20 第 0 组 |
| 重复 | 未写 | 无循环、无 seed |
| 选模 | 未写 | 打印 `Best Test`（test 上取 max）；val 只用于早停 |
| 优化 | Adam 1e-3，wd 5e-4 | 一致；另有 ReduceLROnPlateau(0.5, 50) |
| ∆t | 0.02 / 0.5 | 0.02 / 0.15 |
| 内层步 K | 5 | 无 |
| 硬件 | 未写 | — |

## 论文写的 vs 代码做的（复现关注点）

1. 划分协议不同 → 论文 ± 不可按同一协议复现；我们跑 10 组 geom-gcn 划分作替代。
2. `Best Test` 是 oracle → 必须同时报 val 选模数字。
3. sheaf 退化为标量权 → 方法的"sheaf"成分在实现里很弱，可作为一个分析点。
4. ∆t、K 与论文不一致 → 先按代码跑，再单独试 ∆t = 0.5。

## 依赖的基础知识（LEARNING_PLAN 模块）

- M1：sheaf 拉普拉斯（Hansen & Ghrist；Bodnar NSD 第 2–3 节）、切比雪夫多项式滤波、
  PAC-Bayes 界的 McAllester 形式（Alquier 第 1–2 章）、Sinkhorn（Peyré & Cuturi 第 4 章）。
- M0：CG 解线性系统、归一化拉普拉斯谱的范围 [0, 2]。

## 复现结论（步骤 7，未冻结）

| 层级 | 是否达到 | 说明 |
|------|----------|------|
| L1 | 是 | 9/9 闭环；Pubmed 用 `--spec lobpcg` |
| L2 | 部分 | Cora 5-seed oracle 82.58 vs 83.0；Chameleon 10 划分 oracle 52.83 vs 53.3；Cornell oracle 80.54 vs 81.0。Texas oracle 偏高；Wisconsin 明显偏高。val 选模系统性低于 oracle |
| L3 | 否 | 异配是 geom-gcn 10 划分，不是论文「每类 20 个随机训练节点」；同配是 public split 的 init seed；我们的 σ 大于论文 |

协议开关默认关，补丁 `repro/patches/sgpc-protocol.patch`。Citeseer seed 3 上稠密 `eigvalsh` 曾 `LinAlgError`，dense 路径已加失败回退。Actor / Squirrel 10 划分未跑。数字见 `results/SUMMARY.md` 与 `repro/SGPC_REPRO_LOG.md`。

## 可以延伸的点

- 把 `build_sheaf_laplacian` 换成真正的 \(d \times d\) 限制映射（NSD 风格），看异配集是否再提升。
- 异配 ∆t=0.5（论文）vs 0.15（代码），尤其 Wisconsin。
- 与 IGNN 在同一 critical 划分下对比（两者都在 Actor / Chameleon / Squirrel 上报数）。
