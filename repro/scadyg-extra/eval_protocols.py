"""Deterministic ranking protocols kept separate from the released evaluator."""

from __future__ import annotations

import torch


@torch.no_grad()
def report_filtered_bipartite_eval(model, graph, x, valid_destination_nodes):
    """Rank every positive edge against all valid non-positive destinations.

    Other positive destinations of the same source in the current snapshot are
    filtered out. The metric is deterministic and does not consume an RNG.
    """
    x = x.detach()
    edge_index = graph.edge_label_index[:, graph.edge_label == 1].to("cpu").long()
    if edge_index.numel() == 0:
        raise ValueError("filtered evaluation requires at least one positive edge")

    valid_destination_nodes = torch.as_tensor(
        valid_destination_nodes, dtype=torch.long, device="cpu"
    )
    if valid_destination_nodes.ndim != 1 or valid_destination_nodes.numel() == 0:
        raise ValueError("valid_destination_nodes must be a non-empty vector")
    if torch.unique(valid_destination_nodes).numel() != valid_destination_nodes.numel():
        raise ValueError("valid_destination_nodes contains duplicates")
    valid_destination_nodes = torch.sort(valid_destination_nodes).values

    source_nodes, source_inverse = torch.unique(
        edge_index[0], sorted=True, return_inverse=True
    )
    candidate_edge_index = torch.stack(
        [
            source_nodes.repeat_interleave(valid_destination_nodes.numel()),
            valid_destination_nodes.repeat(source_nodes.numel()),
        ],
        dim=0,
    )

    model.eval()
    positive_scores = (
        model(edge_index.to(x.device), x, mode="train").detach().cpu().reshape(-1)
    )
    candidate_scores = (
        model(candidate_edge_index.to(x.device), x, mode="train")
        .detach()
        .cpu()
        .reshape(source_nodes.numel(), valid_destination_nodes.numel())
    )

    destination_lookup = torch.full(
        (graph.num_nodes(),), -1, dtype=torch.long, device="cpu"
    )
    destination_lookup[valid_destination_nodes] = torch.arange(
        valid_destination_nodes.numel(), dtype=torch.long
    )
    positive_destination_columns = destination_lookup[edge_index[1]]
    if torch.any(positive_destination_columns < 0):
        invalid = torch.unique(edge_index[1][positive_destination_columns < 0])
        raise ValueError(
            "positive destinations missing from protocol manifest: "
            f"{invalid.tolist()}"
        )

    positive_mask = torch.zeros(
        (source_nodes.numel(), valid_destination_nodes.numel()), dtype=torch.bool
    )
    positive_mask[source_inverse, positive_destination_columns] = True
    negative_mask = ~positive_mask

    positive_scores_from_grid = candidate_scores[
        source_inverse, positive_destination_columns
    ]
    if not torch.allclose(positive_scores, positive_scores_from_grid):
        raise RuntimeError(
            "positive scores do not align with the full destination score grid"
        )

    negative_scores_by_positive = candidate_scores[source_inverse]
    valid_negatives_by_positive = negative_mask[source_inverse]
    ranks = (
        (
            (negative_scores_by_positive >= positive_scores.unsqueeze(1))
            & valid_negatives_by_positive
        )
        .sum(dim=1)
        .float()
        + 1
    )
    reciprocal_ranks = ranks.reciprocal()
    negative_counts = valid_negatives_by_positive.sum(dim=1)

    return {
        "mrr": float(reciprocal_ranks.mean()),
        "recall_at_1": float((ranks <= 1).float().mean()),
        "recall_at_3": float((ranks <= 3).float().mean()),
        "recall_at_10": float((ranks <= 10).float().mean()),
        "positive_count": int(edge_index.shape[1]),
        "source_count": int(source_nodes.numel()),
        "mean_negative_count": float(negative_counts.float().mean()),
        "min_negative_count": int(negative_counts.min()),
        "max_negative_count": int(negative_counts.max()),
    }
