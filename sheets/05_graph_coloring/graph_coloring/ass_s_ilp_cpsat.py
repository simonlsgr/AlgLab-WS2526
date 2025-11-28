

from ortools.sat.python.cp_model import FEASIBLE as CPFEASIBLE, OPTIMAL as CPOPTIMAL, CpModel, CpSolver, LinearExpr
import networkx as nx
import math

from utils.data_schema import Solution, ModelStatus
from graph_coloring.gc_solver import GCSolver

class ASS_S_ILPSolverCPSat(GCSolver):
    """Assignment-based ILP Formulation with Symmetry Breaking (ASS-S)"""
    
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
        
        # create a decision variable for every node-color combination
        for node in self.nodes:
            for color in range(self.number_of_colors):
                self.graph.nodes[node][color] = self.model.NewBoolVar(f"x_{node}_{color}")
        
        # create a binary variable for every color
        self.color_vars = {}
        for color in range(self.number_of_colors):
            self.color_vars[color] = self.model.NewBoolVar(f"y_{color}")
        
        
        # adjacent nodes can not have the same color
        for u, v in self.graph.edges:
            for color in range(self.number_of_colors):
                self.model.Add(self.graph.nodes[u][color] + self.graph.nodes[v][color] <= 1)
        
        # color can only be used if y_c is true
        for node in self.nodes:
            for color in range(self.number_of_colors):
                self.model.Add(self.graph.nodes[node][color] <= self.color_vars[color])
        
        # one color has to be used in one node
        for node in self.nodes:
            self.model.Add(sum([self.graph.nodes[node][color] for color in range(self.number_of_colors)]) == 1)
            
        # breaking symmetries
        for color in range(self.number_of_colors):
            self.model.Add(
                self.color_vars[color] <= sum([self.graph.nodes[node][color] for node in self.nodes])
            )
        
        
        self.model.Minimize(sum([color_var for color_var in self.color_vars.values()]))
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
    
    def generate_graph(self):
        for node in self.nodes:
            for color in range(self.number_of_colors):
                if self.solver.Value(self.graph.nodes[node][color]):
                    self.graph.nodes[node]["color"] = color
                    break
    
    def get_graph(self):
        if not self.solution_generated:
            self.generate_graph()
        
        return self.graph
    
    def solve(self, timelimit: float = math.inf):
        
        if timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
            
        cp_status = self.solver.Solve(self.model)
        used_colors = 0
        for color in range(self.number_of_colors):
            var = self.solver.Value(self.color_vars[color])
            if var:
                used_colors += 1
                
        # for node in self.nodes:
        #     used_colors_in_node = 0
        #     for color in range(self.number_of_colors):
        #         used_colors_in_node += self.solver.Value(self.graph.nodes[node][color])
        #     assert (used_colors_in_node == 1)
            
        if cp_status in [CPFEASIBLE, CPOPTIMAL]:
            self.bound = used_colors
            self.generate_graph()
            if cp_status == CPFEASIBLE:
                self.status = ModelStatus.FEASIBLE        
            elif cp_status == CPOPTIMAL:
                self.status = ModelStatus.OPTIMAL
        else:
            self.bound = math.inf
            self.graph = nx.Graph()
        
        
        
        return Solution(graph=self.graph, colors=self.bound, status=self.status)
        
        
            