

from pysat.solvers import Solver as SATSolver
import networkx as nx

class PYSATSolver:
    def __init__(self, instance: nx.Graph, number_of_colors: int = -1):
        self.solver = SATSolver("Minicard")

        
        self.solution_generated = False
        
        self.number_of_colors = number_of_colors
        if self.number_of_colors == -1:
            self.number_of_colors = len(list(instance.nodes()))
            
        self.graph = instance
        self.nodes = list(self.graph.nodes)
        for node in self.nodes:
            self.graph.nodes[node]["color"] = -1
            
        self.bound = -1
    
    def solve(self):
        
        self.statis = self.solver.solve()
        self.solution = self.solver.get_model()
        
        colors = 0
        return colors