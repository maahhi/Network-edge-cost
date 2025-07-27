import networkx as nx
import pandas as pd
import random
from collections import defaultdict


def load_graph_nx(file_path):

    # Load data
    edges = pd.read_csv(file_path, sep=",", names=["FromNodeId", "ToNodeId", "weight"])

    # Create a directed graph
    G = nx.DiGraph()

    # Add edges to the graph
    for _, row in edges.iterrows():
        # random weight
        G.add_edge(row["FromNodeId"], row["ToNodeId"], weight=abs(row["weight"]))
    return G


def load_edges(file_path):
    # Load data
    df = pd.read_csv(file_path, sep=",", names=["FromNodeId", "ToNodeId", "weight"])
    edges = df.values.tolist()
    #print(edges[:5])
    return edges


def build_adjacency_list(edge_list, directed=False):
    adj = defaultdict(list)  # default to empty list

    for u, v, w in edge_list:
        adj[u].append((v, w))
        if not directed:
            adj[v].append((u, w))  # for undirected graphs

    return dict(adj)  # convert defaultdict to normal dict


if __name__ == "__main__":

    file = "sample_graph.txt"
    edges = load_edges(file)
    adjacency_list = build_adjacency_list(edges)
    print(adjacency_list)

    file = "bitcoinalpha.txt"
    graph = load_graph_nx(file)