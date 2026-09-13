# IGNN custom split 准备单（10× 48%/32%/20%）

服务器占用期间**只准备、不训练**。GPU 空闲后按本文件或包装脚本执行：

```bash
bash repro/run_ignn_custom_cignn.sh                          # 预检 + 打印命令
IGNN_EXECUTE=1 IGNN_SMOKE_ONLY=1 bash repro/run_ignn_custom_cignn.sh
IGNN_EXECUTE=1 bash repro/run_ignn_custom_cignn.sh            # 烟雾 + 三个 10-run
```
过程记录追加到 [`IGNN_REPRO_LOG.md`](IGNN_REPRO_LOG.md)。默认不训练。

## 协议

- 论文主协议：仓库固定 10 组随机划分，训练 / 验证 / 测试 = 48% / 32% / 20%。
- 入口：`scripts/01-best-cIGNN.sh` 第 2–20 行（c-IGNN，`--public False --repeat 10`）。
- 对照表：`repro/ignn/results/table_our.csv`（作者 V100 环境）。
- 本机：RTX 3090，Python 3.8.16，PyTorch 2.1.2+cu121。README 已声明同参跨卡会有偏差；chameleon 官方示例是 V100 `50.79±4.92` vs 3090 `47.53±3.36`。
- **不搜参、不跑 30 个基线、不跑 arxiv/products/pokec。**

## 首轮三数据集（GPU 空闲后按此顺序）

| 顺序 | 数据集 | source | 官方 c-IGNN（our split） | 数据文件 | 划分文件 SHA-256 |
|------|--------|--------|--------------------------|----------|------------------|
| 1 | actor | pyg | 38.51±0.94 | `data/actor/` 已在本地 | `9668e2f89750f49567b99671d250c1bc9300574298ce6efc910dd76dbb7e8478` |
| 2 | chameleon | critical | 50.79±4.92（V100；3090 可能约 47.5） | `chameleon_filtered_directed.npz` | `2174cc40152f1c5d78b4022d80df652c914d5390f402d20ffd114705799c9b2b` |
| 3 | squirrel | critical | 45.71±2.13 | `squirrel_filtered_directed.npz` | `e6220e175e748158ce3fd4816e80bbe5d8c75ea09b860ce577ce47e13ee1a222` |

选这三组的原因：划分文件与执行路径一致；数据已在本地；actor 可与已完成的 public 结果对照；chameleon / squirrel 是真正的 48/32/20 协议，不再误用 `graph_datasets` 丢掉的 NPZ mask。

## 已核实的事实

- 10 个中等数据集的 `*-48-32-splitsx10.npy` 均存在，每组 10 折，train/val/test 无交集，覆盖全部节点，比例为 48/32/20（整数取整误差 ≤0.02 个百分点）。
- Actor 的 PyG public mask 与 custom npy **尺寸相同但节点不同**（第 0 折训练交集 1713 / 3648）。因此 custom 数字不应与 public 的 `37.43±0.97` 直接比。
- Chameleon / Squirrel 的 NPZ 里确有 10 组 public mask，但与仓库 npy **不是同一套**。此前 `--public True` 因加载器丢 mask，实际读的是 npy。custom 命令会**故意**读这套 npy，协议才正确；超参仍须用 `01-best-cIGNN.sh`，不能复用 public 脚本。
- 烟雾测试残留的 `chameleon_critical-48-32-splitsx1.npy` 已删除，避免 `repeat=1` 时静默生成非官方划分。
- 官方提交仍为 `7a1bb0adb3ccb78e193276e181cbf8d2090ed61f`，工作区干净。

## 数据哈希

```
chameleon_filtered_directed.npz  5a2d40701407188f1661d37a326484b49cc15251e0dedaa7bd380873dac80f21
squirrel_filtered_directed.npz   0526e53252f0b052124f7390829c32e923d432acaf64206191a1144a07b39620
roman_empire.npz                 a58ba741d123bf892fe5c872138d07463d75a2e9012360b8dd78ac2d4766d428
amazon_ratings.npz               4c3a3e3b9d9f6cba0fede4625a00aad8c5721c1a36ed771367f446763241c7dd
```

尚未下载、本轮不做：flickr / blogcatalog（`source=cola`）、photo（`source=pyg`）。

## GPU 空闲后的命令

在工作区根目录执行。标签必须含 `custom`；烟雾测试标签必须含 `smoke`。

```bash
# 0. 再核一次划分指纹（必须与上表一致）
sha256sum repro/ignn/data/random_splits/fixed_splits/actor_pyg-48-32-splitsx10.npy \
          repro/ignn/data/random_splits/fixed_splits/chameleon_critical-48-32-splitsx10.npy \
          repro/ignn/data/random_splits/fixed_splits/squirrel_critical-48-32-splitsx10.npy

# 1. Actor 烟雾 → 正式
bash repro/run_ignn.sh smoke_actor_c_custom_2ep_r1 --gpu_id 0 --seed 42 --dataset actor --source pyg --model ignn --n_epochs 2 --agg_type gcn_incep --IN IN-SN --h_feats 512 --lr 0.001 --l2_coef 0.0 --n_hops 1 --n_layers 1 --early_stop 100 --RN concat --norm_type ln --act_type relu --preln False --fast False --pre_dropout 0.0 --hid_dropout 0.8 --clf_dropout 0.9 --eval_interval 1 --eval_start 0 --public False --repeat 1

bash repro/run_ignn.sh official_actor_c_custom_r10 --gpu_id 0 --seed 42 --dataset actor --source pyg --model ignn --n_epochs 3000 --agg_type gcn_incep --IN IN-SN --h_feats 512 --lr 0.001 --l2_coef 0.0 --n_hops 1 --n_layers 1 --early_stop 100 --RN concat --norm_type ln --act_type relu --preln False --fast False --pre_dropout 0.0 --hid_dropout 0.8 --clf_dropout 0.9 --eval_interval 1 --eval_start 0 --public False --repeat 10

# 2. Chameleon 烟雾 → 正式
bash repro/run_ignn.sh smoke_chameleon_c_custom_2ep_r1 --gpu_id 0 --seed 42 --dataset chameleon --source critical --model ignn --n_epochs 2 --agg_type gcn_incep --IN IN-SN --h_feats 64 --lr 0.001 --l2_coef 0.0 --n_hops 1 --n_layers 5 --early_stop 150 --RN concat --norm_type none --act_type none --preln True --fast False --pre_dropout 0.8 --hid_dropout 0.3 --clf_dropout 0.3 --eval_interval 1 --eval_start 0 --public False --repeat 1

bash repro/run_ignn.sh official_chameleon_c_custom_r10 --gpu_id 0 --seed 42 --dataset chameleon --source critical --model ignn --n_epochs 3000 --agg_type gcn_incep --IN IN-SN --h_feats 64 --lr 0.001 --l2_coef 0.0 --n_hops 1 --n_layers 5 --early_stop 150 --RN concat --norm_type none --act_type none --preln True --fast False --pre_dropout 0.8 --hid_dropout 0.3 --clf_dropout 0.3 --eval_interval 1 --eval_start 0 --public False --repeat 10

# 3. Squirrel 烟雾 → 正式
bash repro/run_ignn.sh smoke_squirrel_c_custom_2ep_r1 --gpu_id 0 --seed 42 --dataset squirrel --source critical --model ignn --n_epochs 2 --agg_type gcn_incep --IN IN-SN --h_feats 128 --lr 0.005 --l2_coef 0.0 --n_hops 1 --n_layers 3 --early_stop 200 --RN none --norm_type none --act_type relu --preln False --fast False --pre_dropout 0.8 --hid_dropout 0.2 --clf_dropout 0.8 --eval_interval 1 --eval_start 0 --public False --repeat 1

bash repro/run_ignn.sh official_squirrel_c_custom_r10 --gpu_id 0 --seed 42 --dataset squirrel --source critical --model ignn --n_epochs 3000 --agg_type gcn_incep --IN IN-SN --h_feats 128 --lr 0.005 --l2_coef 0.0 --n_hops 1 --n_layers 3 --early_stop 200 --RN none --norm_type none --act_type relu --preln False --fast False --pre_dropout 0.8 --hid_dropout 0.2 --clf_dropout 0.8 --eval_interval 1 --eval_start 0 --public False --repeat 10
```

烟雾测试日志里必须出现 `random splits train:val:test =48:32:20`，且**不能**出现 `No fixed splits found`。若生成了新的 `splitsx1.npy`，立即停止并删除该文件。

## 判定

| 层级 | 通过条件 |
|------|----------|
| L1 | 退出码 0；日志确认读的是 `splitsx10.npy`；划分指纹未变 |
| L2 | actor / squirrel 均值落入官方 ±σ；chameleon 允许落到 README 的 3090 示例附近 |
| L3 | 均值差 < 官方 σ 且方差同量级；硬件差异必须写明 |

三组 c-IGNN 完成后再决定是否扩展 r-IGNN / a-IGNN。roman-empire custom 数据已在本地，但不是首轮。

## 停止条件

- 划分文件哈希变化，或运行中新生成 `splitsx*`。
- 日志显示 public mask，或比例不是 48/32/20。
- 需要改超参才能接近表格：记录后停止，不搜参。
