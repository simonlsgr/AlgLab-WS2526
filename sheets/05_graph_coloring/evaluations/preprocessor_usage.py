
from graph_coloring.preprocessing import DegreeBasedPreprocessor
from graph_coloring.solvers import *
from graph_coloring.heuristics import DSATUR

from utils.load_instance import load_instance

import random
import networkx as nx


def high_clique_graph(clique_size: int, n: int, p: float):

    
    graph: nx.Graph = nx.erdos_renyi_graph(n, p)
    
    for i in range(clique_size):
        for j in range(i+1, clique_size):
            graph.add_edge(i, j)
    return graph

def very_leafy_graph(n: int, p: float):
    
    graph: nx.Graph = nx.erdos_renyi_graph(n, p)
    
    original_nodes = list(graph.nodes())
    num_nodes = len(original_nodes)
    
    leaf = num_nodes
    for node in original_nodes:
        for _ in range(num_nodes):
            graph.add_node(leaf)
            graph.add_edge(node, leaf)
            leaf += 1
    
    return graph
    
def main():
    random.seed(42)    
    
    instances = [ "zeroin.i.1.col", "fpsol2.i.1.col", "fpsol2.i.2.col", "fpsol2.i.3.col", "le450_15b.col", "le450_15c.col", "le450_15d.col", "le450_25a.col", "le450_25b.col", "le450_25c.col", "le450_25d.col", "le450_5a.col", "le450_5b.col", "le450_5c.col", "le450_5d.col"]
    
    edges_removed_relative = []
    nodes_removed_relative = []
    for instance in instances:
        graph, c = load_instance(instance)
        
        preprocessor = DegreeBasedPreprocessor(graph)
        reduced_graph = preprocessor.preprocess()
        
        
        print("Instance:",instance)
        print("Original Graph:",graph)
        print("Reduced Graph:",reduced_graph)
        if (reduced_graph.number_of_nodes() != graph.number_of_nodes() or graph.number_of_edges() != reduced_graph.number_of_edges()):
            edges_removed_relative.append((graph.number_of_edges() - reduced_graph.number_of_edges())/graph.number_of_edges())
            nodes_removed_relative.append((graph.number_of_nodes() - reduced_graph.number_of_nodes())/graph.number_of_nodes())
    
    print("Edges removed (relative to all altered graphs):",sum(edges_removed_relative)/len(edges_removed_relative))
    print("Nodes removed (relative to all altered graphs):",sum(nodes_removed_relative)/len(nodes_removed_relative))
    print("Edges removed (relative to all graphs):",sum(edges_removed_relative)/len(instances))
    print("Nodes removed (relative to all graphs):",sum(nodes_removed_relative)/len(instances))
    print("Number of altered graphs:", max(len(edges_removed_relative), len(nodes_removed_relative)))
    
    # g2 = very_leafy_graph(20, 0.5)
    # print(g2)
    
    # preprocessorg2 = DegreeBasedPreprocessor(g2)
    # reduced_g2 = preprocessorg2.preprocess()
    
    # rep_solver = NotEqualSolver(reduced_g2)
    # rep_solution = rep_solver.solve(timelimit=20)
    # print(rep_solution)
    # post_processed =preprocessorg2.postprocess(rep_solution)
    
    # print(nx.is_isomorphic(g2, post_processed.graph))