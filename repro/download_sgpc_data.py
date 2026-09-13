#!/usr/bin/env python
"""通过镜像预下载 SGPC 官方 main.py 使用的 9 个 PyG 数据集。

官方代码把数据根目录写死在 /tmp/<Name>；本脚本把同样的目录结构放到
repro/sgpc/data/<Name>，由 repro/run_sgpc.sh 用符号链接接到 /tmp，
使官方代码可以原样运行。

做法：把 PyG 内部的 download_url / fs.cp 对 GitHub 的请求改写到 ghfast.top，
其余逻辑完全交给 PyG 自己的 Dataset 类，保证 raw 文件名和目录与官方一致。

用法（在 dtgb 环境）：
    python repro/download_sgpc_data.py            # 全部 9 个
    python repro/download_sgpc_data.py 0 3 5      # 只下 data_id 为 0/3/5 的
"""
import hashlib
import os
import sys

import torch_geometric.data.download as tg_download
import torch_geometric.io.fs as tg_fs
from torch_geometric import datasets as D

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.join(HERE, "sgpc", "data")
MIRROR = "https://ghfast.top/"
GITHUB_PREFIXES = ("https://github.com/", "https://raw.githubusercontent.com/")


def mirror(url: str) -> str:
    if url.startswith(GITHUB_PREFIXES) and not url.startswith(MIRROR):
        return MIRROR + url
    return url


_orig_download_url = tg_download.download_url
_orig_cp = tg_fs.cp


def download_url(url, folder, *args, **kwargs):
    return _orig_download_url(mirror(url), folder, *args, **kwargs)


def cp(path1, path2, *args, **kwargs):
    return _orig_cp(mirror(path1), path2, *args, **kwargs)


# Planetoid 走 fs.cp（模块内 `from torch_geometric.io import fs`，改 fs.cp 属性即可生效）；
# 其余三类模块内 `from torch_geometric.data import download_url`，需逐模块覆盖名字。
tg_fs.cp = cp
tg_download.download_url = download_url
for mod in (D.wikipedia_network, D.actor, D.webkb):
    mod.download_url = download_url

# 与官方 main.py 的 data_id 一一对应，root 名字也保持一致
SPECS = {
    0: ("Cora", lambda r: D.Planetoid(root=r, name="Cora")),
    1: ("Citeseer", lambda r: D.Planetoid(root=r, name="Citeseer")),
    2: ("Pubmed", lambda r: D.Planetoid(root=r, name="Pubmed")),
    3: ("Chameleon", lambda r: D.WikipediaNetwork(root=r, name="chameleon")),
    4: ("Squirrel", lambda r: D.WikipediaNetwork(root=r, name="squirrel")),
    5: ("Actor", lambda r: D.Actor(root=r)),
    6: ("Cornell", lambda r: D.WebKB(root=r, name="Cornell")),
    7: ("Texas", lambda r: D.WebKB(root=r, name="Texas")),
    8: ("Wisconsin", lambda r: D.WebKB(root=r, name="Wisconsin")),
}


def sha256_of_dir(path: str) -> str:
    h = hashlib.sha256()
    for dirpath, _, files in sorted(os.walk(path)):
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            h.update(os.path.relpath(p, path).encode())
            with open(p, "rb") as fh:
                h.update(hashlib.sha256(fh.read()).digest())
    return h.hexdigest()


def main(ids):
    os.makedirs(DATA_ROOT, exist_ok=True)
    for i in ids:
        name, build = SPECS[i]
        root = os.path.join(DATA_ROOT, name)
        ds = build(root)
        data = ds[0]
        raw_dir = ds.raw_dir
        print(
            f"[{i}] {name}: nodes={data.num_nodes} edges={data.num_edges} "
            f"feats={data.num_node_features} classes={ds.num_classes} "
            f"train_mask_dim={data.train_mask.dim()} raw_dir={os.path.relpath(raw_dir, HERE)} "
            f"raw_sha256={sha256_of_dir(raw_dir)}"
        )


if __name__ == "__main__":
    sel = [int(a) for a in sys.argv[1:]] or list(SPECS)
    main(sel)
