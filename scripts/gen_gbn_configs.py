#!/usr/bin/env python
"""按论文 Table 8 生成 GBN 的 NC 配置 json（含 `layer_wise`）。

背景：`repro/gbn/main.py` 的 argparse **没有** `layer_wise`，但
`node_classification.py:load_model` 会读 `configs.layer_wise`。官方因此把该字段
放在预置 json 里（只给了 `configs/NC/CS.json`）。若某个数据集没有 json，
main.py 会用 CLI 值另存一份 json —— 里面没有 `layer_wise`，随后
`AttributeError: 'Namespace' object has no attribute 'layer_wise'`。

本脚本不写进官方克隆，而是生成到 `results/gbn/configs/`（入库），
由 `repro/run_gbn_table.sh` 在运行时拷进 `repro/gbn/configs/NC/`。

超参来源：论文 *Deeper with Riemannian Geometry*（NeurIPS 2025）Table 8。
  Dataset          n_layers  hid_dim  dropout  norm   lr     w_decay
  Texas               5       512     0.3     ln    1e-4      0
  Wisconsin           5       512     0.7     ln    1e-3      0
  Amazon-Ratings      5       512     0.15    bn    3e-4      0
  Roman-Empire        5       512     0.15    ln    3e-4      0
  Coauthor-CS         3       512     0.2     ln    3e-5      0
  AmazonComputers     3       512     0.2     ln    3e-5      0
  WikiCS              3       512     0.2     ln    3e-5      0
（Cora 不在论文表中，作为额外汇总项，沿用同配 3 层那组。）

其余字段取官方 `configs/NC/CS.json` 的值：hid_dim=embed_dim=512、GELU、
tau=1.0、layer_wise=true、add_self_loop=false、weight_decay_nc=0、
epochs_nc=2000、val_every=5、patience_nc=15、exp_iters=10。

用法:
    python scripts/gen_gbn_configs.py                    # 写到 results/gbn/configs/
    python scripts/gen_gbn_configs.py --out-dir DIR
"""
import argparse
import json
from pathlib import Path

# 论文 Table 8；Cora 为额外补充（沿用同配 3 层设置）
TABLE8 = {
    "CS":             {"n_layers": 3, "dropout": 0.20, "norm": "ln", "lr_nc": 3e-5},
    "WikiCS":         {"n_layers": 3, "dropout": 0.20, "norm": "ln", "lr_nc": 3e-5},
    "computers":      {"n_layers": 3, "dropout": 0.20, "norm": "ln", "lr_nc": 3e-5},
    "Cora":           {"n_layers": 3, "dropout": 0.20, "norm": "ln", "lr_nc": 3e-5},
    "Roman-empire":   {"n_layers": 5, "dropout": 0.15, "norm": "ln", "lr_nc": 3e-4},
    "Amazon-ratings": {"n_layers": 5, "dropout": 0.15, "norm": "bn", "lr_nc": 3e-4},
    "Texas":          {"n_layers": 5, "dropout": 0.30, "norm": "ln", "lr_nc": 1e-4},
    "Wisconsin":      {"n_layers": 5, "dropout": 0.70, "norm": "ln", "lr_nc": 1e-3},
}

BASE = {
    "task": "NC",
    "root_path": "./datasets",
    "val_every": 5,
    "exp_iters": 10,
    "log_dir": "./logs/",
    "result_dir": "./results/",
    "checkpoints": "./checkpoints/",
    "add_self_loop": False,
    "hid_dim": 512,
    "embed_dim": 512,
    "act": "gelu",
    "input_act": "gelu",
    "bias": True,
    "tau": 1.0,
    "layer_wise": True,
    "weight_decay_nc": 0,
    "epochs_nc": 2000,
    "patience_nc": 15,
    "use_gpu": True,
    "gpu": 0,
    "devices": "0",
}


def make(name, hp, exp_iters=None, epochs_nc=None, ablate=None,
         gamma_const=None, rate_const=None):
    cfg = dict(BASE)
    cfg.update({
        "dataset": name,
        "task_model_path": f"NC_{name}_model.pt",
        **hp,
    })
    if exp_iters is not None:
        cfg["exp_iters"] = exp_iters
    if epochs_nc is not None:
        cfg["epochs_nc"] = epochs_nc
    if ablate is not None:
        cfg["ablate"] = ablate
    if gamma_const is not None:
        cfg["ablate_gamma_const"] = gamma_const
    if rate_const is not None:
        cfg["ablate_rate_const"] = rate_const
    return cfg


# 论文 Table 4 的消融变体；'none' 即完整 GBN。
# 语义（论文 7.2 节 Ablation Study）：
#   gamma_all0      γ_i = 0      去掉外部输入
#   beta_all0       β_i = 0      去掉边界交互
#   gamma_beta_all0 γ_i, β_i = 0 论文说此时退化为 GCN
#   gamma0_beta0    γ, β 换成固定常数（**论文未给出常数取值**，本仓库默认 1.0）
ABLATIONS = ["none", "gamma0_beta0", "gamma_all0", "beta_all0", "gamma_beta_all0"]
# 论文 Table 4 覆盖的数据集
ABLATION_DATASETS = ["CS", "WikiCS", "Texas", "Amazon-ratings"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="results/gbn/configs")
    ap.add_argument("--smoke", action="store_true",
                    help="另出一份短 epoch 的烟雾配置到 <out>/smoke/")
    ap.add_argument("--ablation", action="store_true",
                    help="另出消融配置到 <out>/ablate/<mode>/（论文 Table 4）")
    ap.add_argument("--ablation-datasets", default=",".join(ABLATION_DATASETS))
    ap.add_argument("--epochs", type=int, default=None,
                    help="覆盖 epochs_nc（消融可用较小值做烟雾）")
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, hp in TABLE8.items():
        path = out / f"{name}.json"
        path.write_text(json.dumps(make(name, hp), indent=4) + "\n", encoding="utf-8")
        print(f"wrote {path}")
    if args.smoke:
        sm = out / "smoke"
        sm.mkdir(parents=True, exist_ok=True)
        for name, hp in TABLE8.items():
            # 烟雾只减 epoch，**不动 exp_iters**：官方 `node_classification.py`
            # 用 `mask[:, split]`，要求 2-D 掩码；CS/WikiCS/computers/Cora 走
            # `RandomNodeSplit`，当 num_splits=1 时掩码是 1-D，会 IndexError。
            # WebKB / Heterophilous 用原生 [N, 10] 掩码，不受影响。
            path = sm / f"{name}.json"
            path.write_text(
                json.dumps(make(name, hp, epochs_nc=2), indent=4) + "\n",
                encoding="utf-8",
            )
            print(f"wrote {path}")
    if args.ablation:
        ds_list = [d for d in args.ablation_datasets.split(",") if d]
        for mode in ABLATIONS:
            d_abl = out / "ablate" / mode
            d_abl.mkdir(parents=True, exist_ok=True)
            for name in ds_list:
                hp = TABLE8[name]
                path = d_abl / f"{name}.json"
                path.write_text(
                    json.dumps(
                        make(name, hp, ablate=mode, epochs_nc=args.epochs),
                        indent=4,
                    ) + "\n",
                    encoding="utf-8",
                )
                print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
