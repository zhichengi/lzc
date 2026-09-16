import os
from typing import List, Union

# This preprocessing script follows the Bitcoin Alpha setup used in
# "ROLAND: Graph Learning Framework for Dynamic Graphs".

import argparse
import deepsnap
import numpy as np
import pandas as pd
import torch
from deepsnap.graph import Graph
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder


def save_snapshot(dataset, dataset_name, output_root):
    dataset_dir = os.path.join(output_root, dataset_name)

    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        os.makedirs(os.path.join(dataset_dir, 'edge_feature'))
        os.makedirs(os.path.join(dataset_dir, 'edge_index'))
        os.makedirs(os.path.join(dataset_dir, 'edge_time'))
        os.makedirs(os.path.join(dataset_dir, 'node_feature'))

    for index, graph in enumerate(dataset):
        np.save(os.path.join(dataset_dir, 'edge_feature', f'{index}.npy'), graph.edge_feature.numpy())
        np.save(os.path.join(dataset_dir, 'edge_index', f'{index}.npy'), graph.edge_index.numpy())
        np.save(os.path.join(dataset_dir, 'edge_time', f'{index}.npy'), graph.edge_time.numpy())
        np.save(os.path.join(dataset_dir, 'node_feature', f'{index}.npy'), graph.node_feature.numpy())


def load_single_dataset(dataset_dir: str, add_reverse_edges: bool) -> Graph:
    dataframe = pd.read_csv(dataset_dir, sep=',', header=None, index_col=None)
    dataframe.columns = ['SOURCE', 'TARGET', 'RATING', 'TIME']
    num_nodes = len(pd.unique(dataframe[['SOURCE', 'TARGET']].to_numpy().ravel()))
    dataframe['TIME'] = dataframe['TIME'].astype(int).astype(float)
    assert not np.any(pd.isna(dataframe).values)

    time_scaler = MinMaxScaler((0, 2))
    dataframe['TimestampScaled'] = time_scaler.fit_transform(
        dataframe['TIME'].values.reshape(-1, 1)
    )
    edge_feature = torch.Tensor(dataframe[['RATING', 'TimestampScaled']].values)

    node_indices = np.sort(pd.unique(dataframe[['SOURCE', 'TARGET']].to_numpy().ravel()))
    encoder = OrdinalEncoder(categories=[node_indices, node_indices])
    edge_index = torch.LongTensor(
        encoder.fit_transform(dataframe[['SOURCE', 'TARGET']].values).transpose()
    )
    node_feature = torch.ones(num_nodes, 1).float()
    edge_time = torch.FloatTensor(dataframe['TIME'].values)

    if add_reverse_edges:
        edge_feature = torch.cat((edge_feature, edge_feature.clone()), dim=0)
        reversed_index = torch.stack([edge_index[1], edge_index[0]]).clone()
        edge_index = torch.cat((edge_index, reversed_index), dim=1)
        edge_time = torch.cat((edge_time, edge_time.clone()))

    return Graph(
        node_feature=node_feature,
        edge_feature=edge_feature,
        edge_index=edge_index,
        edge_time=edge_time,
        directed=True,
    )


def split_by_seconds(graph, frequency_seconds: int) -> List[Graph]:
    split_criterion = graph.edge_time // frequency_seconds
    groups = torch.sort(torch.unique(split_criterion))[0]
    snapshots = []
    for group in groups:
        period_members = split_criterion == group
        snapshots.append(Graph(
            node_feature=graph.node_feature,
            edge_feature=graph.edge_feature[period_members, :],
            edge_index=graph.edge_index[:, period_members],
            edge_time=graph.edge_time[period_members],
            directed=graph.directed,
        ))
    return snapshots


def load_generic(
    dataset_path: str,
    snapshot_seconds: int,
    add_reverse_edges: bool,
    layers_mp: int,
) -> List[Graph]:
    graph = load_single_dataset(dataset_path, add_reverse_edges)
    snapshots = split_by_seconds(graph, snapshot_seconds)
    num_nodes = int(graph.edge_index.max()) + 1

    for snapshot in snapshots:
        snapshot.node_states = [0 for _ in range(layers_mp)]
        snapshot.node_cells = [0 for _ in range(layers_mp)]
        snapshot.node_degree_existing = torch.zeros(num_nodes)

    previous_end = -1
    for snapshot in snapshots:
        start = torch.min(snapshot.edge_time)
        end = torch.max(snapshot.edge_time)
        assert previous_end < start <= end
        previous_end = end
    return snapshots


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='BitcoinAlpha CSV path')
    parser.add_argument('--output-root', default='dataset', help='generated dataset root')
    parser.add_argument('--snapshot-seconds', type=int, default=723000)
    parser.add_argument('--no-reverse-edges', action='store_true')
    parser.add_argument('--layers-mp', type=int, default=2)
    args = parser.parse_args()

    snapshots = load_generic(
        args.input,
        args.snapshot_seconds,
        add_reverse_edges=not args.no_reverse_edges,
        layers_mp=args.layers_mp,
    )
    save_snapshot(snapshots, 'bitcoinalpha', args.output_root)
    print(f'generated {len(snapshots)} snapshots in {os.path.join(args.output_root, "bitcoinalpha")}')
