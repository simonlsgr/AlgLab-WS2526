

from ortools.sat.python.cp_model import FEASIBLE as CPFEASIBLE, OPTIMAL as CPOPTIMAL, CpModel, CpSolver, LinearExpr
import networkx as nx
import math

from utils.data_schema import Solution, ModelStatus
from graph_coloring.solvers_code.gc_solver import GCSolver

class REPILPSolverCPSat(GCSolver):
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
        self.model = CpModel()
        
        
        
        
        # create a decision variable vor every pair v,w where w is not in the neighborhood of v and the index of v is smaller of w
        self.x = {}
        for v in self.nodes:
            for w in (list(nx.non_neighbors(self.graph, v)) + [v]):
                if self.graph.nodes[v]["index"] >= self.graph.nodes[w]["index"]:
                    self.x[v, w] = self.model.NewBoolVar(f"x_{v}_{w}")
                else:
                    self.x[v, w] = 0
        
        
        # every node chooses exactly one representative
        for v in self.nodes:
            self.model.Add(sum([self.x[v, w] for w in (list(nx.non_neighbors(self.graph, v)) + [v]) if (v, w) in self.x]) == 1)
    
        
        # 1. if u and v are adjacent they can not select the same representative
        # 2. if v marks w as representative then w must be a a representative
        for w in self.nodes:
            neighbors_w = list(nx.neighbors(self.graph, w))
            V_minus_N_w = [node for node in self.nodes if node not in (neighbors_w) and node != w]
            for u in V_minus_N_w:
                for v in V_minus_N_w:
                    if self.graph.has_edge(u, v):
                        self.model.Add(self.x[u, w] + self.x[v, w] <= self.x[w, w])
        
        
        self.model.Minimize(sum(self.x[v, v] for v in self.nodes))
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
        # self.solver.parameters.num_workers = 12
    
    def generate_graph(self):
        color = 1
        for v in self.nodes:
            if self.solver.Value(self.x[v, v]):
                self.graph.nodes[v]["color"] = color
                color += 1
        
        for (u, v), var in self.x.items():
            if self.solver.Value(var):
                self.graph.nodes[u]["color"] = self.graph.nodes[v]["color"]
    
    def get_graph(self):
        if not self.solution_generated:
            self.generate_graph()
        
        return self.graph
    
    def solve(self, timelimit: float = math.inf):
        
        if timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        
        cp_status = self.solver.Solve(self.model)
        used_colors = 0
        for w in self.nodes:
            var = self.solver.Value(self.x[w, w])
            if var:
                used_colors += 1
            
        
        
        self.lower_bound = None
        if cp_status in [CPFEASIBLE, CPOPTIMAL]:
            self.bound = used_colors
            self.generate_graph()
            if cp_status == CPFEASIBLE:
                self.status = ModelStatus.FEASIBLE        
                self.lower_bound = self.solver.BestObjectiveBound()
            elif cp_status == CPOPTIMAL:
                self.status = ModelStatus.OPTIMAL
        else:
            self.bound = math.inf
            self.graph = nx.Graph()
        
        return Solution(graph=self.graph, colors=self.bound, status=self.status, lower_bound=self.lower_bound)
        