# GBN 上游问题草稿（**决定不发出**）

> 2026-09-16：**决定不发出**。保留本文作为 Table 3/4 差距与失配的证据记录。
> 若日后要发，目标仓库为 `ZhenhHuang/GBN`（作者仓库）；提交前需先用 GitHub API
> 复核默认分支 SHA。

仓库：https://github.com/ZhenhHuang/GBN
提交：`72ad3692916ecc60f2c78d5bd01a55d7c6297a4f`
论文：*Deeper with Riemannian Geometry: Overcoming Oversmoothing and Oversquashing for Graph Foundation Models*（NeurIPS 2025）

本文件只整理**有确定依据**的问题，供后续决定是否发出。复现细节见
[GBN_REPRO_LOG.md](GBN_REPRO_LOG.md)。**已决定不发出**（见文首标注）。

---

## 1. `gamma0_beta0` 的常数取值未公开，Table 4 这一行无法复现

**现象**：论文 Table 4 的 `γ0, β0` 行应只比 GBN 略低（CS −1.64、WikiCS −0.85、
Texas −1.84、Ratings −0.46）。我们把可学系数换成固定常数 1.0 后，四格全部大幅偏低：

| 数据集 | 论文 γ0,β0 | 我们（取 1.0） | 差 |
|--------|-----------|----------------|-----|
| CS | 94.14 ± 0.26 | 90.37 ± 0.30 | −3.77 |
| WikiCS | 85.36 ± 0.45 | 78.65 ± 1.21 | −6.71 |
| Texas | 83.17 ± 4.32 | 63.78 ± 5.57 | −19.39 |
| Amazon-ratings | 53.05 ± 0.78 | 42.66 ± 2.11 | −10.39 |

**请求**：论文 7.2 节只写"replace the learnable boundary condition coefficients with
fixed constants, termed as γ0, β0"，请补充这两个常数的具体数值（或指出它们是标量还是
向量、作用在哪一层）。

---

## 2. `β` 的作用位置：`βi = 0` 在我们的实现里几乎不改变结果

**现象**：论文中 `βi = 0` 明确掉 2.0–4.5 个点；我们把
`BoundaryConvLayer.rate`（乘在 `out_x` 上的系数）置零后，CS / WikiCS 几乎不动：

| 数据集 | GBN（我们） | βi=0（我们） | 我们变化 | 论文变化 |
|--------|-------------|--------------|----------|----------|
| CS | 95.80 | 95.72 | −0.08 | −2.01 |
| WikiCS | 84.91 | 85.01 | +0.10 | −4.50 |
| Texas | 82.16 | 83.51 | +1.35 | −2.23 |
| Amazon-ratings | 51.95 | 50.23 | −1.72 | −2.82 |

**推测**：β 可能还参与 `ind_bd`（边界指示量）或 `p_deg` 的构造，而不只是 `out_x` 的
系数。若如此，`βi = 0` 应当同时改变这些量。

**请求**：`modules/layers.py` 的 `BoundaryConvLayer.forward` 里，`rate` 与
`ind_bd` / `p_deg` 分别对应论文记号里的哪一项？β 是只对应 `rate` 吗？

---

## 3. Appendix E Table 8 只给了 7 个超参

Table 8 给了 `n_layers` / `hid_dim` / activation / dropout / norm / `lr` / `w_decay`，
但以下需要从代码默认值推断，论文未说明：

- `tau`（模型里 `F.logsigmoid(ind_layer(x0)/tau)`，代码默认 1.0）
- `add_self_loop`（代码默认 `False`，但 `BoundaryGCN` 的签名默认是 `True`，CLI 里没有）
- `val_every`（我们用官方 `configs/NC/CS.json` 的 5，直接影响早停时机）
- `embed_dim`（我们用与 `hid_dim` 相同的 512）
- 是否固定随机种子 / 划分的具体生成方式（`main.py` 顶部写死 `set_seed(3047)`，
  我们用 `RandomNodeSplit` 生成 10 个划分）

**请求**：补齐这些取值，尤其是 `val_every` 与 `tau`。

---

## 4. `layer_wise` 不在 argparse 里（可用性建议）

`main.py` 的 argparse 没有 `layer_wise`，但 `node_classification.py:load_model` 读
`configs.layer_wise`。官方只预置了 `configs/NC/CS.json`，因此对任何其它数据集，首次运行
会生成一份**不含** `layer_wise` 的 json，紧接着报：

```
AttributeError: 'Namespace' object has no attribute 'layer_wise'
```

**建议**：把 `layer_wise` 加进 argparse（或给 `getattr` 一个默认值）。

---

## 备注

- 以上 1、2 两条是本轮消融对比中发现的**具体失配**，都指向"论文文字与代码/公开材料之间的
  缺口"，不是数值噪声。
- 第 3 条是主表偏差的可疑来源之一（另有硬件差异：论文 RTX 4090，我们 RTX 3090）。
