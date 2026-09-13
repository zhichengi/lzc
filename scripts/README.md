# scripts/

工作区级脚本：环境安装、资源上限、日志解析、官方仓预处理。各论文的训练入口在 `repro/run_<name>.sh`，不放这里。

## 环境安装

| 脚本 | 作用 |
|------|------|
| `setup_env.sh` | 在已激活的环境（预期 `dtgb`）里装 torch 2.2.1+cu121 / PyG 2.8 / DGL 2.2.1。不要 `pip install -r requirements.txt` 来装 CUDA 轮子 |
| `setup_gctd_conda.sh` | 新建官方钉扎环境 `gctd`（Python 3.11、torch 2.1.2），不改 `dtgb` |
| `setup_gctd_env.sh` | 只向当前环境补 GCTD 缺的包（`repro/requirements-gctd.txt`） |
| `setup_puma_conda.sh` | 需要时从 dtgb 克隆 `puma`，不改 dtgb |
| `setup_gfm_uv.sh` | 只打印 FairEval 的 uv 步骤，不自动 sync |
| `setup_stem_gnn_conda.sh` | 拒绝官方巨型 environment.yml |
| `clone_official_repo.sh` | ghfast 浅克隆到 `repro/<name>/` 并核 SHA |
| `inspect_official_repo.py` | 扫描官方仓入口与依赖（只读） |
| `repro_wrap.sh` | 单次运行的公共外层（限额+日志） |
| `write_prep_scaffold.py` | 按篇写出 README/日志/入口（再手工改审计） |

IGNN 环境是手工建的 `/home/lab_user/tools/miniconda3/envs/ignn`，没有对应 setup 脚本。`run_example.sh` 跑的是根目录空壳 `main.py`，与四条复现线无关。

## 资源上限（85%）

无 root，不能 `nvidia-smi -pl`。用户态限额：

| 脚本 | 作用 |
|------|------|
| `capped_env.sh` | `source` 后设置 CPU 线程、MPS 85%、`PYTHONPATH`（从而加载 `sitecustomize.py`） |
| `run_capped.sh` | 在 `systemd-run --user` 的 CPUQuota / MemoryMax 里执行命令，并拉起 GPU 占空比 |
| `gpu_util_governor.sh` | 对训练 PID 做 SIGSTOP/SIGCONT，把 `nvidia-smi` GPU-Util 压到约 85% |
| `sitecustomize.py` | 进程启动时 `torch.cuda.set_per_process_memory_fraction(0.85)` |

`repro/run_sgpc.sh` 与 `repro/run_ignn.sh` 已 `source capped_env.sh`。采样写入 `results/logs/resource_cap_monitor.csv`（该目录默认 gitignore）。

临时关闭占空比：`GPU_GOV=0 bash scripts/run_capped.sh ...`。

## 解析与协议

| 脚本 | 作用 |
|------|------|
| `parse_sgpc_log.py` | 从 SGPC stdout 提取 val 选模 test 与 oracle Best Test |
| `analyze_scadyg_logs.py` | 汇总 ScaDyG 多 seed 日志 |
| `build_scadyg_mooc_protocol.py` | 生成 MOOC full-item 评测清单 `results/scadyg/protocols/mooc_full_item_v1.npz`；`run_scadyg.sh` 在缺失时会自动调用 |
