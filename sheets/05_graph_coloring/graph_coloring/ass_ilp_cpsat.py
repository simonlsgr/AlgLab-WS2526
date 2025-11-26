

from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver, LinearExpr
import networkx as nx

class ASSILPSolverCPSat:
    """Assignment-Based ILP Formulation (ASS)"""
    
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
        
        
        
        self.model.Minimize(sum([color_var for color_var in self.color_vars.values()]))
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
    
    def generate_solution(self):
        for node in self.nodes:
            for color in range(self.number_of_colors):
                if self.solver.Value(self.graph.nodes[node][color]):
                    self.graph.nodes[node]["color"] = color
                    break
    
    def get_solution(self):
        if not self.solution_generated:
            self.generate_solution()
        
        return self.graph
    
    def solve(self):
        
        status = self.solver.Solve(self.model)
        used_colors = 0
        for color in range(self.number_of_colors):
            var = self.solver.Value(self.color_vars[color])
            if var:
                used_colors += 1
                
        for node in self.nodes:
            used_colors_in_node = 0
            for color in range(self.number_of_colors):
                used_colors_in_node += self.solver.Value(self.graph.nodes[node][color])
            assert (used_colors_in_node == 1)
            
        
        self.bound = used_colors
        
        return self.bound
        
        
            