import itertools

import networkx as nx
from pysat.solvers import Solver as SATSolver
import matplotlib.pyplot as plt


class HamiltonianCycleModel:
    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph
        self.solver = SATSolver("Minicard")
        self.assumptions = []

        
        for i, edge in enumerate(self.graph.edges):
            self.graph.edges[edge]["literal"] = i+1
        
            
        for v in self.graph:
            N_of_v = nx.neighbors(self.graph, v)
            incident_edges_literals = [self.graph.edges[v, neighbor]["literal"] for neighbor in N_of_v]
            self.solver.add_atmost(incident_edges_literals, k=2)
            self.solver.add_atmost([-edge for edge in incident_edges_literals], k=len(incident_edges_literals)-2)
            


    def solve(self) -> list[tuple[int, int]] | None:
        """
        Solves the Hamiltonian Cycle Problem. If a HC is found,
        its edges are returned as a list.
        If the graph has no HC, 'None' is returned.
        """
        while True:
            if not self.solver.solve():
                return None
            
            sol = self.solver.get_model()
            selected_edges = [edge for edge in self.graph.edges if sol[self.graph.edges[edge]["literal"] - 1] > 0]
            subcycles = list(nx.connected_components(nx.Graph(selected_edges)))
            
            
            if len(subcycles) == 1:
                return selected_edges

            # if there are two or more subcycles, then we need to add a clause, 
            # which ensures that at least one of the edges connecting two disjoint subcycles is used in the final solution
            for cycle in subcycles:
                necessary_literals = [self.graph.edges[u, v]["literal"] for (u,v) in self.graph.edges if (u in cycle and v not in cycle) or (u not in cycle and v in cycle)]
                self.solver.add_clause(necessary_literals)
                    


if __name__ == "__main__":
    import pathlib
    import pickle
    CWD = pathlib.Path(__file__).parent
    filepath = CWD / "./instances/alb1000.pickle"
    with filepath.open("rb") as f:
        graph = pickle.load(f)
    
    HamiltonianCycleModel(graph).solve()