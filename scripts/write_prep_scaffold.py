#!/usr/bin/env python
"""根据登记表写出每篇论文独立的 README / 日志 / notes / 入口脚本。不改官方克隆。"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-12"

# HEAD SHA 来自本次 ghfast 浅克隆，已与 git ls-remote HEAD 一致。
PAPERS = [
    dict(
        id="09", name="gbn", env="dtgb", module="M1",
        title="Deeper with Riemannian Geometry: Overcoming Oversmoothing and Oversquashing for Graph Foundation Models",
        venue="NeurIPS 2025", github="https://github.com/ZhenhHuang/GBN",
        slug="ZhenhHuang/GBN", sha="72ad3692916ecc60f2c78d5bd01a55d7c6297a4f", branch="main",
        pdf="papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/09_Riemannian_GBN_NeurIPS2025.pdf",
        target="节点分类（WikiCS / Texas 等）与深层 GCN 对照；仓库预置 configs/NC/CS.json",
        cwd="repro/gbn",
        audit=[
            "cwd 依赖：`./datasets` `./configs/{task}/{dataset}.json`；JSON 存在时会覆盖 CLI。",
            "seed 写死 `set_seed(3047)`，`exp_iters` 默认 10。",
            "官方 requirements 钉 torch 2.0.0+cu118；本机先试 `dtgb`。",
            "无 wandb。GPU `--gpu` 默认 0。",
            "NC 预置配置只有 CS；Cora/Texas 首次运行会**写入**新 json，烟雾后必须删掉以免污染全量。",
        ],
        data="PyG：WebKB / Planetoid / Coauthor / WikiCS / Heterophilous。优先符号链接已有 `repro/sgpc/data/`。Coauthor CS 需另下。",
        smoke="bash repro/run_gbn.sh smoke_texas -- --task NC --dataset Texas --epochs_nc 2 --exp_iters 1 --patience_nc 1 --hid_dim 64 --embed_dim 64",
        smoke_note="烟雾用 Texas 并在运行后删除 configs/NC/Texas.json（若原本不存在）。不要改 CS.json。",
        full="\n".join([
            "bash repro/run_gbn.sh official_cs -- --task NC --dataset CS",
            "bash repro/run_gbn.sh official_texas -- --task NC --dataset Texas",
            "# Transfer 任务：python main.py --task Transfer --dataset line",
        ]),
        setup="# 复用 dtgb。若 BoundaryGCN / torch-scatter 报错再新建 gbn。\necho 'reuse dtgb'",
        extra_setup="",
    ),
    dict(
        id="10", name="stable_chebnet", env="dtgb", module="M1,M5",
        title="Return of ChebNet: Understanding and Improving an Overlooked GNN on Long-Range Tasks",
        venue="NeurIPS 2025 Spotlight", github="https://github.com/ahariri13/Stable-ChebNet",
        slug="ahariri13/Stable-ChebNet", sha="7d7a7e2696119891d277fd3fa2b32fdda454b814", branch="main",
        pdf="papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/10_Stable-ChebNet_NeurIPS2025.pdf",
        target="Peptides-func / Peptides-struct（LRGB）；Barbell 与 GraphProp 为合成/属性任务",
        cwd="repro/stable_chebnet",
        audit=[
            "无统一 requirements.txt；依赖 PyG + OGB。GraphProp 入口强制 `import ray`。",
            "Barbell 默认 wandb，且 README 用 sbatch。",
            "Peptides 脚本把超参写在 py 文件里，无 CLI epoch。",
            "主表应对 LRGB，不要用 Barbell 数字对论文主表。",
        ],
        data="Peptides 走 PyG LRGB；不要直连 GitHub，先镜像或本地下好再离线加载。",
        smoke="echo 'ChebNet 训练烟雾需 LRGB 数据与可能的 ray；预处理阶段只做 import 检查，见 run_stable_chebnet.sh'",
        smoke_note="预处理不做全 epoch。数据就绪后：cd Peptides/Stable && python ChebStable_peptide.py（先备份脚本再把 epoch 改为 2）。",
        full="\n".join([
            "cd repro/stable_chebnet/Peptides/Stable",
            "python ChebStable_peptide.py",
            "python ChebStable_Struc.py",
        ]),
        setup="echo 'reuse dtgb; pip install ogb if missing'",
        extra_setup="",
    ),
    dict(
        id="31", name="puma", env="puma", module="M2",
        title="PUMA: Efficient Continual Graph Learning with Graph Condensation",
        venue="TKDE 2025", github="https://github.com/superallen13/PUMA",
        slug="superallen13/PUMA", sha="9e4e87f53db0da6aacad4a0a9d08f1c2970413d0", branch="master",
        pdf="papers/gnn-frontier-2025-2026/08-ccf-journals/31_PUMA_TKDE2025.pdf",
        target="Table 2 class-IL：CoraFull / arxiv / reddit / products，指标 AP / mAP / AF",
        cwd="repro/puma",
        audit=[
            "官方环境 Python 3.8 + torch 1.13.0 + pyg 2.2.0 + ogb 1.3.6。",
            "table2.sh 对四个数据集循环，budget 写死；`--repeat 5`。",
            "wandb 默认关。`--device cuda:0`。",
            "CoraFull / Reddit 走 PyG；arxiv/products 走 OGB。",
            "全量 table2 小时级；烟雾用 `--cgl-method bare --cls-epoch 1 --repeat 1 --dataset-name corafull`。",
        ],
        data="CoraFull 由 PyG 下载；OGB 需镜像。数据根 `--data-dir ./data`。",
        smoke="bash repro/run_puma.sh smoke_bare_corafull -- --dataset-name corafull --cgl-method bare --cls-epoch 1 --repeat 1 --evaluate",
        smoke_note="新建 conda `puma` 之前，可先在 dtgb 试 bare 1 epoch。失败则按 setup_puma_conda.sh 建环境，不要往 dtgb 装 torch 1.13。",
        full="bash repro/puma/scripts/table2.sh   # 须在 repro/puma 下，且 FULL=1",
        setup="bash scripts/setup_puma_conda.sh",
        extra_setup="puma",
    ),
    dict(
        id="15", name="scalegnn", env="dtgb", module="M3",
        title="ScaleGNN: Towards Scalable Graph Neural Networks via Adaptive High-order Neighboring Feature Fusion",
        venue="WWW 2026", github="https://github.com/lx970414/ScaleGNN",
        slug="lx970414/ScaleGNN", sha="4825c7ed2ccb8a7a4c47edce4afefb1e771389aa", branch="main",
        pdf="papers/gnn-frontier-2025-2026/03-scalable-bigdata-gnn/15_ScaleGNN_WWW2026.pdf",
        target="Cora/Citeseer/Pubmed 小图；主表 ogbn-arxiv（约 1 小时 / 10 seed）。papers100M 仅 memmap 路径。",
        cwd="repro/scalegnn",
        audit=[
            "官方验证环境是 Python 3.12 + torch 2.11+cu128；本机先用 dtgb（2.2.1+cu121）。",
            "`config_cora.yaml` 默认 `device: cpu` 且 `selection_metric: test`（用 test 选模）。",
            "烟雾不要改官方 yaml：复制到 results/scalegnn/ 再改 epochs。",
            "ogbn-arxiv 走 `ogb_precompute_train.py`；papers100M 走 memmap，不要一次载入全图。",
        ],
        data="小图 Planetoid 符号链接 `repro/sgpc/data/Cora` → `repro/scalegnn/data/Cora`。arxiv 用 OGB `./data`。",
        smoke="bash repro/run_scalegnn.sh smoke_cora -- python main.py --config /home/lab_user/project/lzc/results/scalegnn/smoke_cora.yaml",
        smoke_note="smoke yaml 由预处理写入 results/scalegnn/smoke_cora.yaml（epochs=2, device=cuda）。",
        full="\n".join([
            "python main.py --config config_cora.yaml",
            "python ogb_precompute_train.py --config config_arxiv.yaml",
        ]),
        setup="echo reuse dtgb; python -c 'import yaml,ogb'",
        extra_setup="",
    ),
    dict(
        id="44", name="labeling_trick", env="dtgb", module="M5",
        title="Improving Graph Neural Networks on Multi-node Tasks with the Labeling Trick",
        venue="JMLR 2025", github="https://github.com/GraphPKU/LabelingTrick",
        slug="GraphPKU/LabelingTrick", sha="17b71959c854c5379e1b042100321661c7d1d55e", branch="main",
        pdf="papers/gnn-frontier-2025-2026/11-journals-tnnls-jmlr/44_LabelingTrick_JMLR2025.pdf",
        target="LinkPred 子目录：Cora/CiteSeer/PubMed 无向链接预测 AUROC；`--test` 为 10 seed 正式协议",
        cwd="repro/labeling_trick/LinkPred",
        audit=[
            "四个子仓库互不共享入口。主线用 LinkPred。",
            "无 `--test` 时跑 Optuna 200 trial + sqlite，不要当正式数字。",
            "`--test` 仍是 10 个 seed、每 seed 最多 2000 step，不是烟雾。",
            "需要 optuna、torch_scatter；device 写死 cuda。",
            "Planetoid 根目录 `./data`（相对 LinkPred）。",
        ],
        data="`repro/labeling_trick/LinkPred/data/` 链到已有 Planetoid。",
        smoke="bash repro/run_labeling_trick.sh smoke_import -- python -c \"from Dataset import load_dataset; d=load_dataset('Cora'); print('nodes', d.num_nodes, 'edges', d.edge_index.size(1))\"",
        smoke_note="官方无短 epoch CLI。训练烟雾不要用 --test（那是 10 seed 全量）。全量：python main.py --dataset Cora --test",
        full="python main.py --dataset Cora --test",
        setup="echo reuse dtgb; python -c 'import optuna, torch_scatter'",
        extra_setup="",
    ),
    dict(
        id="13", name="mavn", env="dtgb", module="M5",
        title="Learn When and Where to Connect: Adaptive Virtual Nodes for Dynamic Message Passing on Graphs",
        venue="KDD 2026", github="https://github.com/bdi-lab/MAVN",
        slug="bdi-lab/MAVN", sha="3773c40a753a08528aa73c641c4f991ba4cfd4e5", branch="main",
        pdf="papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/13_MAVN_KDD2026.pdf",
        target="Peptides-func AP（seed 0–3）；PascalVOC-SP；minesweeper / tolokers 10 split。附录 PDF：Setup_MAVN_KDD2026.pdf",
        cwd="repro/mavn/code",
        audit=[
            "官方 Python 3.9.19 + torch 2.0.1+cu117。requirements 很短，其余在 PDF。",
            "两个入口：train.py（TunedGNN 风格）与 train_v2.py（heterophily 风格）。",
            "Peptides 要改 val.pt→valid.pt；数据放 ./datasets/。",
            "命令极长，必须原样复制 README，只改 --num_epoch 做烟雾。",
            "许可证 CC BY-NC-SA 4.0。",
        ],
        data="Peptides/Pascal 来自 Dropbox/PyG LRGB；minesweeper/tolokers 用 ghfast 拉 yandex npz。脚本 repro/download_mavn_data.sh",
        smoke="echo '先 bash repro/download_mavn_data.sh minesweeper，再把 README 的 minesweeper 命令 --num_epoch 改为 2'",
        smoke_note="烟雾数据集优先 minesweeper（比 Peptides 小）。不要在没数据时启动 train.py。",
        full="见 README Peptides-func 四 seed 命令；在 code/ 下执行。",
        setup="echo reuse dtgb first",
        extra_setup="",
    ),
    dict(
        id="08", name="fair_eval_gfm", env="gfm", module="M6",
        title="A Fair Evaluation of Graph Foundation Models for Node Property Prediction",
        venue="ICML 2026 Workshop", github="https://github.com/yandex-research/gnn-fair-evaluation",
        slug="yandex-research/gnn-fair-evaluation", sha="0a388f087773258e8f2559d801129dfe87adb3bc", branch="main",
        pdf="papers/gnn-frontier-2025-2026/01-graph-foundation-models/08_FairEval_GFM_ICML2026Workshop.pdf",
        target="GraphLand 上的 GNN 基线；GFM 数字来自各官方仓。本仓库只用 uv 复现 GNN 部分。",
        cwd="repro/fair_eval_gfm",
        audit=[
            "强制 Python 3.12.9 + uv；torch==2.4.0、dgl==2.4.0，不能塞进 dtgb。",
            "数据 GraphLand：Zenodo 16895532，需 symlink `data/`。",
            "仓库已含实验报告；重跑必须 `--force`。",
            "GFM 方法不在本仓，链到 AnyGraph / GraphPFN / EquivarianceEverywhere 等。",
        ],
        data="https://zenodo.org/records/16895532 下载解压后 `ln -s <path> repro/fair_eval_gfm/data`",
        smoke="echo '需 uv + GraphLand。环境好后: uv run bin/go.py exp/critical/gcn/tolokers-2/evaluation.toml --n_seeds 1 --ensemble_size 0 --force'",
        smoke_note="预处理不装 uv 环境、不下 Zenodo（体积大）。setup_gfm_conda.sh 只记录步骤。",
        full="uv run bin/go.py exp/cgasb/gcn/tolokers-2/evaluation.toml --n_seeds 5",
        setup="bash scripts/setup_gfm_uv.sh",
        extra_setup="gfm",
    ),
    dict(
        id="01", name="equivariance", env="gfm", module="M6",
        title="Equivariance Everywhere All At Once: A Recipe for Graph Foundation Models",
        venue="NeurIPS 2025", github="https://github.com/benfinkelshtein/EquivarianceEverywhere",
        slug="benfinkelshtein/EquivarianceEverywhere", sha="1dfe3870fd8a0de7e15db6958289661b2cabdc37", branch="main",
        pdf="papers/gnn-frontier-2025-2026/01-graph-foundation-models/01_EquivarianceEverywhere_NeurIPS2025.pdf",
        target="trainset1：Cora 训练、其余图测试。与 04 二选一做全量。",
        cwd="repro/equivariance",
        audit=[
            "官方 Python 3.10 + torch 2.3.0+cu118 + pyg 2.5.3；另要 neptune、triton。",
            "必须在仓库根目录启动 main.py。",
            "README 让装 neptune；代码里需确认是否硬依赖（全量前审计 experiment.py）。",
            "best config 的 max_epochs 达 2000。烟雾必须显式 --max_epochs 2。",
        ],
        data="脚本内下载多图节点分类基准；全量前应预下载并离线。",
        smoke="bash repro/run_equivariance.sh smoke_gat -- python -u main.py --is_train --gnn_type GAT --lr 0.001 --lp_ratio 0.3 --max_epochs 2",
        smoke_note="与 04 都预处理；全量只开一篇。neptune 若强制登录，先定位再跑。",
        full="python -u main.py --is_train --train_test_setup trainset1 --gnn_type MEAN_GNN --hidden_dim 16 --num_layers 2 --lp_ratio 0.4 --max_epochs 2000 --lr 0.01",
        setup="bash scripts/setup_gfm_uv.sh  # 或独立 conda equivariance",
        extra_setup="",
    ),
    dict(
        id="04", name="mf_gia", env="gfm", module="M6",
        title="Modality-Free Graph In-context Alignment",
        venue="ICLR 2026", github="https://github.com/JhuoW/MF-GIA",
        slug="JhuoW/MF-GIA", sha="9b2946d13af0372323b5e3f3105d822757a87cd9", branch="master",
        pdf="papers/gnn-frontier-2025-2026/01-graph-foundation-models/04_MF-GIA_ICLR2026.pdf",
        target="ICL 节点分类：Cora k-shot。预训练 8000 epoch，优先用仓库 checkpoint。",
        cwd="repro/mf_gia",
        audit=[
            "官方 conda python 3.12.2；torch 2.6.0+cu124，与 dtgb 不兼容。",
            "数据目录结构严格（OFA / pyg SingleTextGraph）。缺文件会在预训练才爆。",
            "configs 里 gpu 默认可能是 1；本机只有 0。",
            "wandb 监控；num_workers 可能触发 too many open files。",
            "generated_files/checkpoints 若在克隆中，全量应先评测 checkpoint 而非重训。",
        ],
        data="按 README 组织 datasets/；OFA 原始文件来自 https://github.com/LechengKong/OneForAll",
        smoke="echo '确认 generated_files/checkpoints 后：python run_ICL_node.py --dataset cora --k_shot 1 --model_path <ckpt>'",
        smoke_note="不要在预处理阶段跑 pretrain.py（8000 epoch）。",
        full="python run_ICL_node.py --dataset cora --k_shot 1",
        setup="conda create -n mf_gia python=3.12 -y  # 见 README，暂不执行",
        extra_setup="",
    ),
    dict(
        id="23", name="graphrp", env="dtgb", module="M7",
        title="Defending against Model Extraction for GNNs with Model Reprogramming",
        venue="KDD 2026", github="https://github.com/overwenyan/GraphRP-KDD2026",
        slug="overwenyan/GraphRP-KDD2026", sha="38b00ecd2cc404461cec176051fd62efd01acd9c", branch="main",
        pdf="papers/gnn-frontier-2025-2026/05-data-mining-security/23_GraphRP_KDD2026.pdf",
        target="MUTAG / ENZYMES 等图分类上的 clone acc ↓ 与 benign acc ↑。与 41 二选一全量。",
        cwd="repro/graphrp",
        audit=[
            "克隆后**只有 README.md**。README 描述的 train_defense.py / models / configs 均不存在。",
            "无法烟雾、无法全量，直到作者推送源码。",
            "记录 blocker，不要手写一份“按论文实现”冒充官方。",
        ],
        data="TU 数据集（MUTAG 等），代码到位后由 PyG TUDataset 加载。",
        smoke="echo 'BLOCKED: 仓库无源码'",
        smoke_note="预处理结论：源码未发布。全量脚本会拒绝执行。",
        full="echo BLOCKED no source",
        setup="echo blocked",
        extra_setup="blocked",
    ),
    dict(
        id="41", name="unlearning_inv", env="dtgb", module="M7",
        title="Unlearning Inversion Attacks for Graph Neural Networks",
        venue="WSDM 2026", github="https://github.com/QwQ2000/WSDM26-Graph-Unlearning-Inversion",
        slug="QwQ2000/WSDM26-Graph-Unlearning-Inversion", sha="3bfc1f17e82a3a9fad9b1cc3ef28281a1323ea16", branch="main",
        pdf="papers/gnn-frontier-2025-2026/10-wsdm/41_UnlearningInversion_WSDM2026.pdf",
        target="Cora 上 Inversion + GIF；README 示例 num_runs=5。与 23 二选一全量。",
        cwd="repro/unlearning_inv",
        audit=[
            "官方声明 python 3.6 + torch 1.9；先试 dtgb。",
            "`--cuda` 默认 **2**，本机必须传 `--cuda 0`。",
            "改编自 GIF-torch。可能需要 METIS。",
            "烟雾：`--num_epochs 2 --num_runs 1`。",
        ],
        data="Planetoid Cora，PyG 默认路径。可复用已有下载。",
        smoke="bash repro/run_unlearning_inv.sh smoke_cora -- python main.py --dataset_name cora --target_model GCN --exp Inversion --method GIF --unlearn_ratio 0.05 --attack_method trend_steal --num_runs 1 --num_epochs 2 --cuda 0 --is_gen_unlearn_request True --is_gen_unlearned_probs True",
        smoke_note="若 METIS/分区失败，记入日志，不要改算法。",
        full="python main.py --dataset_name cora --target_model=GCN --exp Inversion --method GIF --unlearn_ratio 0.05 --attack_method=trend_steal --num_runs=5 --cuda 0 --is_gen_unlearn_request=True --is_gen_unlearned_probs=True",
        setup="echo reuse dtgb",
        extra_setup="",
    ),
    dict(
        id="12", name="stem_gnn", env="stem_gnn", module="M7",
        title="Generalizing GNNs with Tokenized Mixture of Experts",
        venue="KDD 2026", github="https://github.com/GXG-CS/STEM-GNN",
        slug="GXG-CS/STEM-GNN", sha="8995878ca0df9f1fcaedca49d3a45a44ec8403c2", branch="main",
        pdf="papers/gnn-frontier-2025-2026/02-gnn-architecture-theory/12_STEM-GNN_KDD2026.pdf",
        target="先 finetune Cora 节点任务；预训练 `pretrain.py --pretrain_dataset all` 很重，有 ckpt 则跳过",
        cwd="repro/stem_gnn",
        audit=[
            "environment.yml 是整机导出（CUDA 11.6、graph-tool、transformers、deepspeed），**禁止 conda env create -f 原文件**。",
            "入口在子目录 STEM-GNN/。`--use_params` 读 config/*.yaml。",
            "数据放 STEM-GNN/data，权重 STEM-GNN/ckpts。",
            "setup 脚本只装最小依赖，不复现官方巨型 yml。",
        ],
        data="Cora 等放 `repro/stem_gnn/STEM-GNN/data/`。",
        smoke="echo '环境未建。建好后: python STEM-GNN/finetune.py --use_params --finetune_dataset cora --gpu 0'（仍可能要预训练 ckpt）",
        smoke_note="预处理不创建 stem_gnn conda。",
        full="python STEM-GNN/finetune.py --use_params --finetune_dataset cora --gpu 0",
        setup="bash scripts/setup_stem_gnn_conda.sh",
        extra_setup="stem",
    ),
    dict(
        id="22", name="core_graphrag", env="dtgb", module="M8",
        title="Core-based Hierarchies for Efficient GraphRAG",
        venue="KDD 2026", github="https://github.com/erdemUB/KDD26",
        slug="erdemUB/KDD26", sha="37a81bc38b0c5b5836c51d73d1f795a5b438407e", branch="master",
        pdf="papers/gnn-frontier-2025-2026/04-graphrag-llm/22_CoreGraphRAG_KDD2026.pdf",
        target="只做 k-core 层次 / RkH·M2hC·MRC vs Leiden 的算法可复现性；LLM 查询不做",
        cwd="repro/core_graphrag",
        audit=[
            "基于 Microsoft GraphRAG v2.7.0 评测框架；index/query 需要 API key。",
            "本计划只复现社区构造算法侧。单元测试在 tests/unit 与 tests/smoke。",
            "安装 `pip install -e ./graphrag` 可能与 dtgb 冲突，全量前再决定是否新建 env。",
            "community 算法名：RkH / M2hC / MRC。",
        ],
        data="Kevin Scott podcast 等来自 GraphRAG benchmarking datasets；算法烟雾不需要语料。",
        smoke="bash repro/run_core_graphrag.sh smoke_unit -- python -m pytest tests/unit -q --maxfail=3",
        smoke_note="pytest 若缺依赖，记 blocker，不要为了测试去装整个 GraphRAG+OpenAI。",
        full="echo '算法全量：在无 API 条件下对比 Leiden vs RkH 的社区划分可复现性（见笔记）；query 等预算'",
        setup="echo optional pip install pytest in dtgb",
        extra_setup="",
    ),
]


README_TMPL = """# {id} {name_upper} 预处理 / 复现入口

论文：*{title}*（{venue}）。论文库编号 {id}。学习模块：`LEARNING_PLAN.md` {module}。

- 官方仓库：`repro/{name}/`（{github}）
- 固定提交：`{sha}`（分支 `{branch}`，与 `git ls-remote HEAD` 一致）
- 过程日志：[{name_upper}_REPRO_LOG.md]({name_upper}_REPRO_LOG.md)
- 本地论文：`{pdf}`
- 读书笔记：`paper/notes/{id}_{name}.md`
- 运行产物：`results/{name}/runs/`

**本文件只服务这一篇。不要和其它论文共用命令、数据目录或 conda 环境改动。**

## 预处理状态（{today}）

| 项 | 状态 |
|----|------|
| 源码固定 | 已克隆，SHA 见上 |
| 环境 | 计划 `{env}`；{setup_one} |
| 数据 | {data} |
| 代码审计 | 见日志步骤 4（只记录，未改官方代码） |
| 烟雾 | 命令见下；数字不对论文 |
| 全量 | `FULL=1 bash repro/run_{name}_full.sh`（默认 dry-run） |

对照目标：{target}

## 烟雾（短）

```bash
{smoke}
```

{smoke_note}

## 全量（默认不跑）

```bash
bash repro/run_{name}_full.sh          # 只打印命令
FULL=1 bash repro/run_{name}_full.sh   # 真正训练
```

## 不要做的事

- 不要把这篇的日志写进其它论文的 `*_REPRO_LOG.md`。
- 不要在官方克隆里扫参；修正必须是默认关闭的开关 + `.patch`。
- 同一时刻只占一张 GPU；先看 `nvidia-smi`。
"""

LOG_TMPL = """# {name_upper} 复现日志

论文：*{title}*，{venue}。论文库编号 {id}。
官方代码：{github}
本地论文：`{pdf}`
读书笔记：`paper/notes/{id}_{name}.md`
学习模块：`LEARNING_PLAN.md` {module}

约定：日志只追加。官方仓库 `repro/{name}/`。产物 `results/{name}/runs/`。外层只处理环境、GPU、镜像与日志。

复现目标：{target}

---

## {today} 步骤 1：源码固定

- 官方默认分支提交：`{sha}`
- 克隆：`bash scripts/clone_official_repo.sh {name} {slug}`（`ghfast.top`）
- 与 `git ls-remote HEAD`：一致
- 浅克隆，后续作者推送会改变结果；全量前再核一次 SHA

## {today} 步骤 2：环境

- 计划 conda：`{env}`
- 安装：`{setup}`
- 预处理阶段**未**为每篇新建环境（避免 13 套 CUDA 轮子互相覆盖）。烟雾优先试 `dtgb`；失败再执行 setup。
- 官方声明与本机差异：见步骤 4。

## {today} 步骤 3：数据核验

- {data}
- 下载脚本：见 `repro/download_{name}.sh`（若有）或本篇 README
- SHA-256：待实际下载后补

## {today} 步骤 4：代码审计（只记录不改）

{audit}

## {today} 步骤 5：烟雾测试

- 计划命令：

```
{smoke}
```

- {smoke_note}
- 退出码 / 日志：见本条目后续追加（执行后填写）

## 步骤 6–11

未开始。启动全量前：`FULL=1 bash repro/run_{name}_full.sh`，然后按 `_TEMPLATE_REPRO_LOG.md` 追加步骤 6。
"""

NOTES_TMPL = """# {id} {name_upper}（{venue}）

## 一句话
{title}

## 方法拆解
- 待精读论文第 3 节与官方入口后填写 → 代码位置 `repro/{name}/`

## 实验协议
对照目标：{target}

## 论文写的 vs 代码做的
| 项 | 论文 | 代码 | 影响 |
|----|------|------|------|
| （审计摘要） | 见 `repro/{name_upper}_REPRO_LOG.md` 步骤 4 |  |  |

## 依赖的基础知识（对应 LEARNING_PLAN 模块）
- {module}

## 复现结论（冻结时填写）
预处理完成；L1/L2/L3 待全量。

## 可以延伸的点
- （全量后再写）
"""


def write_run_sh(p: dict) -> str:
    blocked = p.get("extra_setup") == "blocked"
    body_block = ""
    if blocked:
        body_block = """
echo "[run] 仓库无源码，拒绝启动。" >&2
exit 3
"""
    return f"""#!/usr/bin/env bash
# {p['id']} {p['name']} 单次运行入口（独立于其它论文）。
# 用法: bash repro/run_{p['name']}.sh LABEL -- CMD...
set -euo pipefail
ROOT="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/.." && pwd)"
if [[ $# -lt 1 ]]; then
  echo "用法: $0 LABEL -- command..." >&2
  exit 2
fi
LABEL="$1"; shift
[[ "${{1:-}}" == "--" ]] && shift
{body_block}
if [[ $# -lt 1 ]]; then
  echo "缺少命令。示例见 repro/{p['name'].upper()}_README.md" >&2
  exit 2
fi
exec bash "${{ROOT}}/scripts/repro_wrap.sh" \\
  --paper {p['name']} --env {p['env']} --repo repro/{p['name']} --cwd {p['cwd']} --label "${{LABEL}}" -- "$@"
"""


def write_full_sh(p: dict) -> str:
    return f"""#!/usr/bin/env bash
# {p['id']} {p['name']} 全量启动。默认 dry-run。
set -euo pipefail
ROOT="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/.." && pwd)"
cd "${{ROOT}}"
echo "[full] paper={p['name']} id={p['id']} FULL=${{FULL:-0}}"
echo "[full] 对照：{p['target']}"
if [[ "${{FULL:-0}}" != "1" ]]; then
  echo "[full] DRY-RUN。确认 GPU 空闲且只跑这一篇后："
  echo "       FULL=1 bash repro/run_{p['name']}_full.sh"
  echo "[full] 计划命令："
  cat <<'EOF'
{p['full']}
EOF
  exit 0
fi
echo "[full] 开始执行。日志走 run_{p['name']}.sh / 官方脚本。"
# 下面按论文自己的工作目录执行；失败立即停，避免和下一篇搅在一起。
cd "${{ROOT}}/{p['cwd']}"
cat <<'EOF'
{p['full']}
EOF
echo "[full] 请按 README 逐条调用 run_{p['name']}.sh，不要在本脚本里静默开训（防止误跑）。" >&2
exit 2
"""


def write_download_stub(p: dict) -> str:
    return f"""#!/usr/bin/env bash
# {p['id']} {p['name']} 数据准备（独立目录）。GitHub 走 ghfast.top。
set -euo pipefail
ROOT="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/.." && pwd)"
echo "[data] paper={p['name']}"
echo "{p['data']}"
echo "实现按 README 补齐；不要写到其它论文的 data/ 目录。"
"""


def main():
    gitignore_names = []
    rows = []
    for p in PAPERS:
        p = dict(p)
        p["today"] = TODAY
        p["name_upper"] = p["name"].upper()
        p["setup_one"] = p["setup"].split("\n")[0]
        p["audit"] = "\n".join(f"{i}. {x}" for i, x in enumerate(p["audit"], 1))
        (ROOT / "results" / p["name"] / "runs").mkdir(parents=True, exist_ok=True)
        (ROOT / "results" / p["name"] / "runs" / ".gitkeep").write_text("")
        (ROOT / f"repro/{p['name_upper']}_README.md").write_text(README_TMPL.format(**p), encoding="utf-8")
        (ROOT / f"repro/{p['name_upper']}_REPRO_LOG.md").write_text(LOG_TMPL.format(**p), encoding="utf-8")
        (ROOT / f"paper/notes/{p['id']}_{p['name']}.md").write_text(NOTES_TMPL.format(**p), encoding="utf-8")
        run_path = ROOT / f"repro/run_{p['name']}.sh"
        run_path.write_text(write_run_sh(p), encoding="utf-8")
        run_path.chmod(0o755)
        full_path = ROOT / f"repro/run_{p['name']}_full.sh"
        full_path.write_text(write_full_sh(p), encoding="utf-8")
        full_path.chmod(0o755)
        dl = ROOT / f"repro/download_{p['name']}.sh"
        if not dl.exists():
            dl.write_text(write_download_stub(p), encoding="utf-8")
            dl.chmod(0o755)
        gitignore_names.append(f"repro/{p['name']}/")
        rows.append(p)
    print(f"wrote {len(rows)} papers")
    print("gitignore:")
    for n in gitignore_names:
        print(n)


if __name__ == "__main__":
    main()
