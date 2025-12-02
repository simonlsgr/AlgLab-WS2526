import networkx as nx

def is_valid_coloring(graph: nx.Graph):
    for u, v in graph.edges:
        if graph.nodes[u]["color"] == graph.nodes[v]["color"] and graph.nodes[v]["color"] != -1:
            return False
    return True