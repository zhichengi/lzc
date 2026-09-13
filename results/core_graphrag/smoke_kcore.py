#!/usr/bin/env python
"""Core GraphRAG 算法烟雾：RkH k-core 层次。不装 OpenAI / pytest / graspologic。
graspologic.partition.leiden 与 plotly 仅模块顶层 import，RkH 路径用 networkx.core_number。
"""
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "repro" / "core_graphrag"
sys.path.insert(0, str(ROOT))

g = types.ModuleType("graspologic")
gp = types.ModuleType("graspologic.partition")
gp.leiden = lambda *a, **k: {}
sys.modules["graspologic"] = g
sys.modules["graspologic.partition"] = gp
try:
    import plotly  # noqa: F401
except ImportError:
    sys.modules["plotly"] = types.ModuleType("plotly")
    sys.modules["plotly.graph_objects"] = types.ModuleType("plotly.graph_objects")

import networkx as nx
from graphrag.index.operations.kcore_cluster_graph import kcore_cluster_graph

G = nx.karate_club_graph()
comms = kcore_cluster_graph(G, use_lcc=False, cluster_type="RkH")
print(f"[core-smoke] karate nodes={G.number_of_nodes()} edges={G.number_of_edges()} RkH_communities={len(comms)}")
assert isinstance(comms, list) and len(comms) > 0
print("[core-smoke] ok")
