
import gurobipy as gp
import networkx as nx
import math

from utils.data_schema import Solution, ModelStatus
from graph_coloring.solvers_code.gc_solver import GCSolver

class ASS_S_ILPSolverGurobi(GCSolver):
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
        
        self.model = gp.Model()
        self.solution = None
        
        # create a decision variable for every node-color combination
        for node in self.nodes:
            for color in range(self.number_of_colors):
                self.graph.nodes[node][color] = self.model.addVar(vtype=gp.GRB.BINARY, name=f"x_{node}_{color}")
        
        # create a binary variable for every color
        self.color_vars = {}
        for color in range(self.number_of_colors):
            self.color_vars[color] = self.model.addVar(vtype=gp.GRB.BINARY, name=f"y_{color}")
        
        
        # adjacent nodes can not have the same color
        for u, v in self.graph.edges:
            for color in range(self.number_of_colors):
                self.model.addConstr(self.graph.nodes[u][color] + self.graph.nodes[v][color] <= 1)
        
        # color can only be used if y_c is true
        for node in self.nodes:
            for color in range(self.number_of_colors):
                self.model.addConstr(self.graph.nodes[node][color] <= self.color_vars[color])
        
        # one color has to be used in one node
        for node in self.nodes:
            self.model.addConstr(gp.quicksum([self.graph.nodes[node][color] for color in range(self.number_of_colors)]) == 1)
            
        
        # breaking symmetries
        for color in range(self.number_of_colors):
            self.model.addConstr(
                self.color_vars[color] <= gp.quicksum([self.graph.nodes[node][color] for node in self.nodes])
            )
        
        
        self.model.setObjective(
            gp.quicksum([color_var for color_var in self.color_vars.values()]),
            gp.GRB.MINIMIZE
        )
        
    
    def generate_graph(self):
        for node in self.nodes:
            for color in range(self.number_of_colors):
                if self.graph.nodes[node][color].X > .5:
                    self.graph.nodes[node]["color"] = color
                    break
    
    def get_graph(self):
        if not self.solution_generated:
            self.generate_graph()
        
        return self.graph
    
        
    def solve(self, timelimit: float = math.inf):
        
        if timelimit < math.inf:
            self.model.Params.TimeLimit = timelimit
        
        self.model.optimize()
        
        used_colors = 0
        for color in range(self.number_of_colors):
            var = self.color_vars[color].X
            if var > .5:
                used_colors += 1
                
        # for node in self.nodes:
        #     used_colors_in_node = 0
        #     for color in range(self.number_of_colors):
        #         used_colors_in_node += 1 if self.graph.nodes[node][color].X > .5 else 0
        #     assert (used_colors_in_node == 1)
            
        
        gp_status = self.model.Status
        self.lower_bound = None
        if gp_status == gp.GRB.OPTIMAL or self.model.SolCount > 0:
            self.bound = used_colors
            self.generate_graph()
            self.lower_bound = self.model.objBound
            if gp_status == gp.GRB.OPTIMAL:
                self.status = ModelStatus.OPTIMAL
            elif self.model.SolCount > 0:
                self.status = ModelStatus.FEASIBLE
        else:
            self.bound = math.inf
            self.graph = nx.Graph()
            
        
        return Solution(graph=self.graph, colors=self.bound, status=self.status, lower_bound=self.lower_bound)