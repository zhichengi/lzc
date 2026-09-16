# ScaDyG issue 草稿（**决定不发出**）

> 2026-09-16：**决定不发出**。保留本文作为 checkpoint bug 的证据记录。
> 若日后要发，目标仓库为 `BITNEO/ScaDyG`；提交前需先用 GitHub API 复核默认分支 SHA。

仓库：https://github.com/BITNEO/ScaDyG  
对照提交：`28ca94a06771c46073b650de3daa95e0939342ba`  
本地补丁：`repro/scadyg-checkpoint-fix.patch`  
**范围：只报确定的 checkpoint bug。不要把评测协议（每源一条正边、全节点负采样）写进 issue。**

发出前请再读一遍措辞，并确认该提交仍是默认分支 HEAD。

---

## Title

Checkpoint only saves `Predict_layer`; `model_transformer` is not restored at test time

## Body

Hi, thanks for releasing the code.

I tried to reproduce the MOOC link-prediction result (paper MRR 0.931 ± 0.009) at commit `28ca94a06771c46073b650de3daa95e0939342ba`, RTX 3090, seed 2023, default 100 epochs.

**Symptom.** Validation MRR per snapshot is already ~0.91–0.94 around epoch 6, but after early stopping (epoch 21, patience 10) the reported **test MRR is 0.025** (AP 0.40, AUC 0.019). Training itself looks healthy.

**Cause.** `train_scalable_tgn` jointly optimizes `model` (`Predict_layer`) and `model_transformer`, but the best checkpoint only deep-copies `model.state_dict()`:

```python
if val_ap > best_param['best_acc']:
    best_param = {'best_acc': val_ap, 'best_state': deepcopy(model.state_dict())}
# ...
model.load_state_dict(best_param['best_state'])
model.eval()
# model_transformer is never saved, loaded, or set to eval()
```

Test therefore pairs the best prediction head with the *last* epoch of the Transformer (here epoch 21), not the epoch that was selected by validation AP.

**Minimal fix** (keeps AP model selection and the rest of the training loop unchanged):

```python
if val_ap > best_param['best_acc']:
    best_param = {
        'best_acc': val_ap,
        'best_state': deepcopy(model.state_dict()),
        'best_transformer_state': deepcopy(model_transformer.state_dict()),
    }
# after the training loop:
model.load_state_dict(best_param['best_state'])
model_transformer.load_state_dict(best_param['best_transformer_state'])
model.eval()
model_transformer.eval()
```

**After this change only**, the same seed 2023 run (same early-stop epoch 21) gives **test MRR 0.9278**, within the paper's reported interval. Training/validation curves match the unpatched run; only the restored test-time modules change.

A patch against the commit above is in the comment / attached if useful.

Happy to provide logs or a one-epoch vs full-run comparison if that helps.
