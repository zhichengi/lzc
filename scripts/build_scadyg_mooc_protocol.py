#!/usr/bin/env python3
"""Build a deterministic full-item evaluation manifest for ScaDyG MOOC."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


PROTOCOL = "mooc_full_item_filtered_v1"


def canonical_edge_hash(snapshots: list[np.ndarray]) -> str:
    digest = hashlib.sha256()
    for snapshot_id, edge_index in enumerate(snapshots):
        array = np.ascontiguousarray(edge_index.astype(np.int64, copy=False))
        digest.update(snapshot_id.to_bytes(4, byteorder="little"))
        digest.update(np.asarray(array.shape, dtype=np.int64).tobytes())
        digest.update(array.tobytes())
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--edge-index-dir",
        type=Path,
        required=True,
        help="directory containing numbered edge_index .npy snapshots",
    )
    parser.add_argument("--output", type=Path, required=True, help="output .npz path")
    args = parser.parse_args()

    snapshot_paths = sorted(
        args.edge_index_dir.glob("*.npy"), key=lambda path: int(path.stem)
    )
    if not snapshot_paths:
        raise FileNotFoundError(f"no .npy snapshots found in {args.edge_index_dir}")
    expected_ids = list(range(len(snapshot_paths)))
    actual_ids = [int(path.stem) for path in snapshot_paths]
    if actual_ids != expected_ids:
        raise ValueError(
            f"snapshot IDs must be contiguous from zero: got {actual_ids[:3]}..."
        )

    snapshots = [np.load(path, allow_pickle=False) for path in snapshot_paths]
    for snapshot_id, edge_index in enumerate(snapshots):
        if edge_index.ndim != 2 or edge_index.shape[0] != 2:
            raise ValueError(
                f"snapshot {snapshot_id} has invalid shape {edge_index.shape}"
            )

    all_sources = np.unique(np.concatenate([edge_index[0] for edge_index in snapshots]))
    all_destinations = np.unique(
        np.concatenate([edge_index[1] for edge_index in snapshots])
    )
    overlap = np.intersect1d(all_sources, all_destinations)
    if overlap.size:
        raise ValueError(
            f"MOOC is expected to be bipartite, but {overlap.size} node IDs overlap"
        )

    snapshot_count = len(snapshots)
    train_end = int(np.ceil(snapshot_count * 0.70))
    validation_end = train_end + int(np.ceil(snapshot_count * 0.15))
    edge_counts = np.asarray(
        [edge_index.shape[1] for edge_index in snapshots], dtype=np.int64
    )
    edge_index_sha256 = canonical_edge_hash(snapshots)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output,
        protocol=np.asarray(PROTOCOL),
        dataset=np.asarray("mooc"),
        snapshot_count=np.asarray(snapshot_count, dtype=np.int64),
        train_snapshot_ids=np.arange(train_end, dtype=np.int64),
        validation_snapshot_ids=np.arange(
            train_end, validation_end, dtype=np.int64
        ),
        test_snapshot_ids=np.arange(
            validation_end, snapshot_count, dtype=np.int64
        ),
        valid_source_nodes=all_sources.astype(np.int64, copy=False),
        valid_destination_nodes=all_destinations.astype(np.int64, copy=False),
        edge_counts=edge_counts,
        edge_index_sha256=np.asarray(edge_index_sha256),
    )

    metadata = {
        "protocol": PROTOCOL,
        "dataset": "mooc",
        "snapshot_count": snapshot_count,
        "split": {
            "train": [0, train_end - 1],
            "validation": [train_end, validation_end - 1],
            "test": [validation_end, snapshot_count - 1],
        },
        "source_node_count": int(all_sources.size),
        "source_node_range": [int(all_sources.min()), int(all_sources.max())],
        "destination_node_count": int(all_destinations.size),
        "destination_node_range": [
            int(all_destinations.min()),
            int(all_destinations.max()),
        ],
        "positive_edge_count": int(edge_counts.sum()),
        "edge_index_sha256": edge_index_sha256,
        "filter": "other positive destinations for the same source in the snapshot",
        "ranking_unit": "one rank per positive edge",
        "candidate_policy": "all valid destination nodes; no random sampling",
    }
    metadata_path = args.output.with_suffix(".json")
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    manifest_sha256 = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(json.dumps({**metadata, "manifest_sha256": manifest_sha256}, indent=2))
    print(f"manifest={args.output}")
    print(f"metadata={metadata_path}")


if __name__ == "__main__":
    main()
