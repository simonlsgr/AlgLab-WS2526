

from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver, LinearExpr
import networkx as nx

class REPILPSolverCPSat:
    """Representative-based ILP Formulation (REP)"""
    
    def __init__(self, instance: nx.Graph):
        self.solution_generated = False
        
            
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
                    # print(self.graph.nodes[v]["index"], self.graph.nodes[w]["index"])
                    self.x[v, w] = self.model.NewBoolVar(f"x_{v}_{w}")
        
        
        # every node chooses exactly one representative
        for v in self.nodes:
            self.model.Add(sum([self.x[v, w] for w in (list(nx.non_neighbors(self.graph, v)) + [v]) if (v, w) in self.x]) == 1)
    
        # for entry in self.x:
        #     print(entry)
        # 1. if u and v are adjacent they can not select the same representative
        # 2. if v marks w as representative then w must be a a representative
        for w in self.nodes:
            neighbors_w = list(nx.neighbors(self.graph, w))
            V_minus_N_w = [node for node in self.nodes if node not in (neighbors_w) and node != w]
            for u in V_minus_N_w:
                for v in V_minus_N_w:
                    if self.graph.has_edge(u, v):
                        if (u, w) in self.x and (v, w) in self.x and (w, w) in self.x:
                            self.model.Add(self.x[u, w] + self.x[v, w] <= self.x[w, w])
        
        
        self.model.Minimize(sum(self.x[v, v] for v in self.nodes))
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
    
    def generate_solution(self):
        color = 1
        for v in self.nodes:
            if self.solver.Value(self.x[v, v]):
                self.graph.nodes[v]["color"] = color
                color += 1
        
        for (u, v), var in self.x.items():
            if self.solver.Value(var):
                self.graph.nodes[u]["color"] = self.graph.nodes[v]["color"]
    
    def get_solution(self):
        if not self.solution_generated:
            self.generate_solution()
        
        return self.graph
    
    def solve(self):
        
        status = self.solver.Solve(self.model)
        used_colors = 0
        for w in self.nodes:
            var = self.solver.Value(self.x[w, w])
            if var:
                used_colors += 1
            
        
        self.bound = used_colors
        
        return self.bound
        