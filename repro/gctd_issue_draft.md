# GCTD issue 草稿（先不提交）

仓库：https://github.com/nicolasrsantos/gctd  
对照提交：本地克隆当时 HEAD `785cfc9`（*Revise README with project details and usage instructions*）。发出前用 GitHub API 再核一次默认分支 SHA。  
**目的：报告默认超参下合成图必为完全图，并请求 Table 2 的完整超参。不要把我们后加的 topk / 配额补丁说成官方行为。**

---

## Title

Default `lr_rec=0.001` makes `to_edge_index` (threshold 0.05) a complete graph on Cora 1.3%

## Body

Hi, thanks for the GCTD release.

I am reproducing Table 2, Cora 1.3% (paper **81.4 ± 1.6**). Hardware: RTX 3090. I first ran the published defaults (`lr_rec=0.001`, `to_edge_index` threshold 0.05, seed 42, `rec_epochs=200`, `gnn_epochs=600`).

**Symptom.** Condensation finishes (22 epochs, rec error ~1e-3). The GCN train accuracy stays at **33.3%** for 600 epochs. Test accuracy is **30.2%**, which matches Cora's global majority class (class 3, 30.2%), not a slightly-weaker condensed graph.

**Cause.** After averaging the core slices, every entry of `A^S` is already above the hard-coded threshold:

| quantity (Cora, 35 supernodes, seed 42, default `lr_rec`) | value |
|---|---|
| `A^S`.min | **0.057** |
| `A^S`.mean / max | 0.358 / 0.672 |
| edges after `new_adj >= 0.05` | **1225 = 35 × 35** (density 1.0) |

```python
# src/models/gctd.py, published `to_edge_index`
new_adj = torch.mean(slices, dim=0, dtype=torch.float)
edge_index = new_adj >= 0.05
```

A 2-layer GCN on this complete graph collapses node representations; the classifier predicts the majority class. A no-graph logistic regression on the same supernode features still reaches ~49% on the original test set, so the features are not empty — the dense graph is.

Raising `lr_rec` to the upper end of `wandb_example.yml` (0.1) is enough for seed 42 to drop some core values near 0.05, and test accuracy goes to ~74.5% with the same 0.05 threshold. That setting is **seed-unstable** (other seeds yield 0 edges or ~4 training supernodes). Aligning the conda stack to the README (Python 3.11, torch 2.1.2, pyg 2.6.1) does **not** recover 81.4% (10-run ~61% under a scale-invariant sparsifier we added locally).

**Request.** Could you share the **exact Table 2 hyperparameters** for Cora 1.3% (and ideally Citeseer / Pubmed), or export the wandb Bayesian sweep that produced 81.4 ± 1.6? In particular: `lr_rec`, `R`, `add_ratio`, `lr_gnn`, whether `weighted` / `drop_ratio` were non-default, and how the 0.05 threshold was meant to interact with the learned core scale.

Happy to send the diagnostic script and logs. I did not change the published condensation/GCN formulas for the 30.2% run above.
