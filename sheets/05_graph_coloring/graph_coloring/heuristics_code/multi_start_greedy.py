import networkx as nx
from graph_coloring.heuristics import NaiveGreedyGraphColoringHeuristic

class MultiStartGreedyGraphColoringHeuristic:
    def __init__(self, instance: nx.Graph, iterations: int = 5):
        self.iterations = iterations
        self.graph = instance
        self.solutions = []
        self.bound = -1
    
    def solve(self):
        for i in range(self.iterations):
            graph = self.graph.copy()
            
            solver = NaiveGreedyGraphColoringHeuristic(graph, random_order=True)
            k = solver.solve()
            
            self.solutions.append(k)
        self.bound = min(self.solutions)
        return self.bound