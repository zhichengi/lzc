"""进程级 GPU 显存上限：不超过整卡的 85%。

由 scripts/capped_env.sh 把本目录加入 PYTHONPATH 后，CPython 会自动 import。
"""
try:
    import torch

    if torch.cuda.is_available():
        torch.cuda.set_per_process_memory_fraction(0.85, 0)
except Exception:
    pass
