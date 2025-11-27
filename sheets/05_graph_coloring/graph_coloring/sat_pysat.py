

from pysat.solvers import Solver as SATSolver
import networkx as nx
import math
from threading import Timer as ThreadTimer
from utils._timer import Timer

from utils.data_schema import Solution, ModelStatus

class PYSATDecisionVariant:
    def __init__(self, instance: nx.Graph, k: int, timelimit: float = math.inf):
        self.solver = SATSolver("Minicard")
        
        self.number_of_colors = k
        self.solver = SATSolver("Minicard")
        
        def interrupt(s):
            s.interrupt()
        if timelimit < math.inf:
            self.timer = ThreadTimer(timelimit, interrupt, [self.solver])
            
        self.graph = instance
        self.nodes = list(self.graph.nodes)
        for node in self.nodes:
            self.graph.nodes[node]["color"] = -1
        
        
        self.bound = -1
        
        self.variables = []
        
        # create a bool var for every vertex-color combination x_{v,c}
        for node in self.nodes:
            for color in range(1, self.number_of_colors+1):
                self.variables.append(self.x(self.graph.nodes[node]["v_index"], color))
                
        # every vertex has at least one color
        for i, node in enumerate(self.nodes):
            self.solver.add_clause([self.x(self.graph.nodes[node]["v_index"], color) for color in range(1, self.number_of_colors+1)])
        
        # no two adjacent vertices share the same color
        for color in range(1, self.number_of_colors+1):
            for u, v in self.graph.edges:
                self.solver.add_clause([-self.x(self.graph.nodes[u]["v_index"], color), -self.x(self.graph.nodes[v]["v_index"], color)])
    
    def x(self, node_id: int, color: int) -> str:
        return node_id*self.number_of_colors+color
    
    def solve(self):
        
        
        
        self.status = self.solver.solve_limited(expect_interrupt=True)
        self.solution = self.solver.get_model()
        
        return self.solution, self.status

    
class PYSATSolver:
    def __init__(self, instance: nx.Graph, number_of_colors: int = -1):
        self.solution_generated = False
        
        self.number_of_colors = number_of_colors
        if self.number_of_colors == -1:
            self.number_of_colors = len(list(instance.nodes()))
            
        
        self.graph = instance
        self.nodes = list(self.graph.nodes)
        for node in self.nodes:
            self.graph.nodes[node]["color"] = -1
        
        for i, node in enumerate(self.nodes):
            self.graph.nodes[node]["v_index"] = i+1
        
            
        self.bound = -1
    
    def x(self, node_id: int, color: int) -> str:
        return node_id*self.bound+color
    
    def generate_graph(self):
        for i, node in enumerate(self.nodes):
            for color in range(1, self.number_of_colors+1):
                if self.x(self.graph.nodes[node]["v_index"], color) in self.solution:
                    self.graph.nodes[node]["color"] = color
                    break
            
    
    def get_graph(self):
        if not self.solution_generated:
            self.generate_graph()
        
        return self.graph
    
    def solve(self, timelimit: float = math.inf):
    
        self.timer = Timer(timelimit)
        
        self.solution = None
        sat_status = None
        for k in range(self.number_of_colors, 0, -1):
            if self.timer.is_out_of_time():
                break
            decision_solver = PYSATDecisionVariant(self.graph.copy(), k, self.timer.remaining())
            decision_solution, current_status = decision_solver.solve()
            
            if decision_solver.status:
                self.solution = decision_solution
                self.bound = k
                sat_status = current_status
            else:
                break
        
        status = ModelStatus.UNKWOWN
        if sat_status:
            status = ModelStatus.FEASIBLE
            self.generate_graph()
        else:
            status = ModelStatus.OTHER
            
        
        return Solution(graph=self.graph, colors=self.bound, status=self.status)
        
        
                