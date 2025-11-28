

from ortools.sat.python.cp_model import FEASIBLE as CPFEASIBLE, OPTIMAL as CPOPTIMAL, CpModel, CpSolver, LinearExpr
import networkx as nx
import math

from utils.data_schema import Solution, ModelStatus
from graph_coloring.gc_solver import GCSolver

class AllDifferentSolver(GCSolver):
    """Constraint Programming: AllDifferent Formulation (CP-AllDiff)"""
    
    def __init__(self, instance: nx.Graph, number_of_colors: int = -1):
        self.solution_generated = False
        
        self.status = ModelStatus.UNKWOWN
        
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
        
        cliques = nx.find_cliques(self.graph)
        for i, clique in enumerate(cliques):
            if len(self.nodes) == i:
                break
            self.model.AddAllDifferent([self.graph.nodes[v]["z"] for v in clique])
        
        self.model.Minimize(self.z_max)
        
            
        
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
    
    def generate_graph(self):
        for node in self.nodes:
            self.graph.nodes[node]["color"] = self.solver.Value(self.graph.nodes[node]["z"])
        
        self.solution_generated = True
    
    def get_graph(self):
        if not self.solution_generated:
            self.generate_graph()
        
        return self.graph
    
    def solve(self, timelimit: float = math.inf) -> Solution:
        
        if timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        
        cp_status = self.solver.Solve(self.model)
        
        
        if cp_status in [CPFEASIBLE, CPOPTIMAL]:
            self.bound = self.solver.Value(self.z_max)
            self.generate_graph()
            if cp_status == CPFEASIBLE:
                self.status = ModelStatus.FEASIBLE        
            elif cp_status == CPOPTIMAL:
                self.status = ModelStatus.OPTIMAL
        else:
            self.bound = math.inf
            self.graph = nx.Graph()
        
        
            
        
        return Solution(graph=self.graph, colors=self.bound, status=self.status)
        
        
            