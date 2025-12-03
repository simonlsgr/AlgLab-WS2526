import math
import networkx as nx

from utils.data_schema import Solution

class DegreeBasedPreprocessor:
    """
    A preprocessor that removes low-degree vertices from the graph.
    This needs to be a class as it maintains state between the preprocessing and postprocessing steps.
    """
    def __init__(self, graph: nx.Graph):
        self.graph = graph 
        self.lower_bound_approximation = nx.approximation.large_clique_size(self.graph)
        self.non_influential_vertices = []
        for node in self.graph.nodes:
            self.graph.nodes[node]["color"] = -1

    def preprocess(self) -> nx.Graph:
        """
        Return a preprocessed graph.
        """
        reduced_graph = self.graph.copy()
        removal_candidates = [node for node, degree in reduced_graph.degree() if degree < self.lower_bound_approximation - 1] 
        
        
        while removal_candidates:
            node = removal_candidates.pop()
            neighbors = list(reduced_graph.neighbors(node))
            self.non_influential_vertices.append(node)
            reduced_graph.remove_node(node)
            for neighbor in neighbors:
                if reduced_graph.degree(neighbor) < self.lower_bound_approximation - 1 and neighbor not in removal_candidates:
                    removal_candidates.append(neighbor)

        
        return reduced_graph
        
        
    def _neighbour_colors(self, node, graph: nx.Graph) -> list[int]:
        colors = []
        for neighbor in graph.neighbors(node):
            color = graph.nodes[neighbor]["color"]
            if  color != -1:
                colors.append(color)
        return sorted(colors)
            
        

    def postprocess(self, solution: Solution) -> Solution:
        """
        Convert a solution for the reduced graph back to the original graph.
        As we are also interested in the lower bound, also pass it through.
        """
        
        for node in solution.graph:
            self.graph.nodes[node]["color"] = solution.graph.nodes[node]["color"]
        
        
        if solution.colors != math.inf:
            for node in reversed(self.non_influential_vertices):
                
                neighbor_colors = self._neighbour_colors(node, self.graph)
                
                
                for i in range(1,solution.colors+1):
                    if i not in neighbor_colors:
                        self.graph.nodes[node]["color"] = i
                        break
        
        return Solution(graph=self.graph, colors=solution.colors, status=solution.status, lower_bound=solution.lower_bound)
        