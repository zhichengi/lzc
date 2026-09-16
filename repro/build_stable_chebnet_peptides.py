"""Rebuild LRGB Peptides-func raw splits for PyG's LRGBDataset.

Context: PyG's ``LRGBDataset`` downloads ``peptidesfunc.zip`` from Dropbox and
expects ``raw/{train,val,test}.pt`` to be lists of ``(x, edge_attr,
edge_index, y)`` tuples. Dropbox is unreachable from this machine.

This script reconstructs those raw files from two reachable mirrors:

1. ``LRGB/peptides-functional`` on HuggingFace -> ``geometric_data_processed.pt``
   is the *processed* output of the original LRGB loader (collated ``Data`` +
   ``slices``), in the original CSV row order.
2. ``scikit-fingerprints/LRGB_Peptides-func`` on HuggingFace -> the stratified
   random split indices (10,873 / 2,331 / 2,331), indexing that same CSV.

Graph order is verified by comparing all 15,535 label vectors against the CSV,
so the split indices apply directly to the processed graphs.

Output is written to ``<out-root>/peptides-func/raw/{train,val,test}.pt``; the
stale ``processed/`` files are removed so PyG re-processes from raw.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from typing import Dict, List

import torch
from torch_geometric.data import Data


def get_graph(data: Data, slices: Dict[str, torch.Tensor], index: int) -> Data:
    """Rebuild one graph from collated ``data`` + ``slices``.

    Mirrors ``InMemoryDataset.__getitem__``: slice each attribute along its own
    concatenation dimension (dim 0 for ``x``/``y``/``edge_attr``, dim 1 for
    ``edge_index``).
    """
    graph = data.__class__()
    if hasattr(data, "__num_nodes__"):
        graph.num_nodes = int(data.__num_nodes__[index])
    for key in data.keys():
        item, segments = data[key], slices[key]
        selection = [slice(None)] * item.dim()
        cat_dim = data.__cat_dim__(key, item)
        cat_dim = 0 if cat_dim is None else int(cat_dim)
        if cat_dim < 0:
            cat_dim += item.dim()
        selection[cat_dim] = slice(int(segments[index]), int(segments[index + 1]))
        graph[key] = item[tuple(selection)]
    return graph


def unbatch(processed_path: str, indices: List[int]) -> List[Data]:
    data, slices = torch.load(processed_path, weights_only=False)
    return [get_graph(data, slices, index) for index in indices]


def load_split_indices(path: str) -> Dict[str, List[int]]:
    """Load the stratified split indices (CSV row order)."""
    with open(path, "r") as handle:
        raw = json.load(handle)
    mapping = {"train": "train", "val": "valid", "test": "test"}
    return {out_key: [int(i) for i in raw[in_key]]
            for out_key, in_key in mapping.items()}


def to_raw_tuple(graph: Data) -> tuple:
    y = graph.y
    if y.dim() == 1:
        y = y.view(1, -1)
    return (graph.x, graph.edge_attr, graph.edge_index, y)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed", required=True,
                        help="geometric_data_processed.pt from LRGB/peptides-functional")
    parser.add_argument("--splits", required=True,
                        help="lrgb_splits_peptides_func.json from scikit-fingerprints")
    parser.add_argument("--out-root", required=True,
                        help="directory that will contain peptides-func/")
    args = parser.parse_args()

    dataset_dir = os.path.join(args.out_root, "peptides-func")
    raw_dir = os.path.join(dataset_dir, "raw")
    processed_dir = os.path.join(dataset_dir, "processed")
    os.makedirs(raw_dir, exist_ok=True)

    splits = load_split_indices(args.splits)
    total = sum(len(v) for v in splits.values())
    print(f"[build] split sizes: " +
          ", ".join(f"{k}={len(v)}" for k, v in splits.items()) + f" (total={total})")

    all_indices = [i for values in splits.values() for i in values]
    if sorted(all_indices) != list(range(total)):
        raise SystemExit("[build] split indices do not partition 0..N-1")

    for split_name in ("train", "val", "test"):
        indices = splits[split_name]
        graphs = unbatch(args.processed, indices)
        payload = [to_raw_tuple(g) for g in graphs]

        node_counts = sum(g.x.shape[0] for g in graphs)
        edge_counts = sum(g.edge_index.shape[1] for g in graphs)
        feature_dims = {g.x.shape[1] for g in graphs}
        edge_dims = {g.edge_attr.shape[1] for g in graphs}
        label_dims = {tuple(g.y.shape) for g in graphs}

        out_path = os.path.join(raw_dir, f"{split_name}.pt")
        torch.save(payload, out_path)
        print(f"[build] {split_name}: graphs={len(payload)} nodes={node_counts} "
              f"edges={edge_counts} x_dim={feature_dims} "
              f"edge_dim={edge_dims} y_shape={label_dims} -> {out_path}")

    if os.path.isdir(processed_dir):
        shutil.rmtree(processed_dir)
        print(f"[build] removed stale {processed_dir}")

    print("[build] done")


if __name__ == "__main__":
    main()
