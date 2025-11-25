import networkx as nx

def is_valid_coloring(graph: nx.Graph):
    for u, v in graph.edges:
        if graph.nodes[u]["color"] == graph.nodes[v]["color"]:
            return False
    return True