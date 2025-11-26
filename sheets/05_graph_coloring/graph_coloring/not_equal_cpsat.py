

from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver, LinearExpr
import networkx as nx

class NotEqualSolver:
    """Constraint Programming: ≠-Formulation (CP≠)"""
    
    def __init__(self, instance: nx.Graph, number_of_colors: int = -1):
        self.solution_generated = False
        
        self.number_of_colors = number_of_colors
        if self.number_of_colors == -1:
            self.number_of_colors = len(list(instance.nodes()))
            
        self.graph = instance
        self.nodes = list(self.graph.nodes)
        for node in self.nodes:
            self.graph.nodes[node]["color"] = -1
            
        self.bound = -1
        self.model = CpModel()
        
        for node in self.nodes:
            self.graph.nodes[node]["z"] = self.model.NewIntVar(lb=1, ub=self.number_of_colors, name=f"z_{node}")
        self.z_max = self.model.NewIntVar(lb=1, ub=self.number_of_colors, name="z_max")
        
        for node in self.nodes:
            self.model.Add(self.graph.nodes[node]["z"] <= self.z_max)
        
        for u, v in self.graph.edges:
            self.model.Add(self.graph.nodes[u]["z"] != self.graph.nodes[v]["z"])
        
        
        self.model.Minimize(self.z_max)
        
            
        
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
    
    def generate_solution(self):
        for node in self.nodes:
            self.graph.nodes[node]["color"] = self.solver.Value(self.graph.nodes[node]["z"])
        
        self.solution_generated = True
    
    def get_solution(self):
        if not self.solution_generated:
            self.generate_solution()
        
        return self.graph
    
    def solve(self):
        
        status = self.solver.Solve(self.model)
            
        
        self.bound = self.solver.Value(self.z_max)
        
        return self.bound
        
        
            