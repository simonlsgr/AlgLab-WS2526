

import gurobipy as gp
import networkx as nx
import math

from utils.data_schema import Solution, ModelStatus
from graph_coloring.solvers_code.gc_solver import GCSolver

class REPILPSolverGurobi(GCSolver):
    """Representative-based ILP Formulation (REP)"""
    
    def __init__(self, instance: nx.Graph, *args):
        self.solution_generated = False
        
        self.status = ModelStatus.UNKWOWN
        
            
        self.graph = instance
        self.nodes = list(self.graph.nodes)
        for node in self.nodes:
            self.graph.nodes[node]["color"] = -1
        for i, node in enumerate(self.nodes):
            self.graph.nodes[node]["index"] = i
            
        self.bound = -1
        self.model = gp.Model()
        
        
        # create a decision variable vor every pair v,w where w is not in the neighborhood of v and the index of v is smaller of w
        self.x = {}
        for v in self.nodes:
            for w in (list(nx.non_neighbors(self.graph, v)) + [v]):
                if self.graph.nodes[v]["index"] >= self.graph.nodes[w]["index"]:
                    self.x[v, w] = self.model.addVar(vtype=gp.GRB.BINARY, name=f"x_{v}_{w}")
                else:
                    self.x[v, w] = 0
        
        
        # every node chooses exactly one representative
        for v in self.nodes:
            self.model.addConstr(gp.quicksum([self.x[v, w] for w in (list(nx.non_neighbors(self.graph, v)) + [v]) if (v, w) in self.x]) == 1)
    
        
        # 1. if u and v are adjacent they can not select the same representative
        # 2. if v marks w as representative then w must be a a representative
        for w in self.nodes:
            neighbors_w = list(nx.neighbors(self.graph, w))
            V_minus_N_w = [node for node in self.nodes if node not in (neighbors_w) and node != w]
            for u in V_minus_N_w:
                for v in V_minus_N_w:
                    if self.graph.has_edge(u, v):
                        self.model.addConstr(self.x[u, w] + self.x[v, w] <= self.x[w, w])
        
        
        self.model.setObjective(
            gp.quicksum(self.x[v, v] for v in self.nodes),
            gp.GRB.MINIMIZE
        )
        
    
    def generate_graph(self):
        color = 1
        for v in self.nodes:
            if self.x[v, v].X:
                self.graph.nodes[v]["color"] = color
                color += 1
        
        for (u, v), var in self.x.items():
            if type(var) != int:
                if var.X:
                    self.graph.nodes[u]["color"] = self.graph.nodes[v]["color"]
    
    def get_graph(self):
        if not self.solution_generated:
            self.generate_graph()
        
        return self.graph
    
    def solve(self, timelimit: float = math.inf):
        
        
        if timelimit < math.inf:
            self.model.Params.TimeLimit = timelimit
        
        self.model.optimize()
        used_colors = 0
        for w in self.nodes:
            var = self.x[w, w].X
            if var:
                used_colors += 1
            
        
        self.bound = used_colors
        
        gp_status = self.model.Status
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
        