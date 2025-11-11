import bisect
import logging
import math
from typing import Iterable

import networkx as nx
from pysat.solvers import Solver as SATSolver

logging.basicConfig(level=logging.INFO)

# Define the node ID type. It is an integer but this helps to make the code more readable.
NodeId = int


class Distances:
    """
    This class provides a convenient interface to query distances between nodes in a graph.
    All distances are precomputed and stored in a dictionary, making lookups efficient.
    """

    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph
        self._distances = dict(nx.all_pairs_dijkstra_path_length(self.graph))
        

    def all_vertices(self) -> Iterable[NodeId]:
        """Returns an iterable of all node IDs in the graph."""
        return self._distances.keys()

    def dist(self, u: NodeId, v: NodeId) -> float:
        """Returns the distance between nodes `u` and `v`."""
        return self._distances[u].get(v, math.inf)

    def max_dist(self, centers: Iterable[NodeId]) -> float:
        """Returns the maximum distance from any node to the closest center."""
        return max(min(self.dist(c, u) for c in centers) for u in self.all_vertices())

    def vertices_in_range(self, u: NodeId, limit: float) -> Iterable[NodeId]:
        """Returns an iterable of nodes within `limit` distance from node `u`."""
        return (v for v, d in self._distances[u].items() if d <= limit)

    def sorted_distances(self) -> list[float]:
        """Returns a sorted list of all pairwise distances in the graph."""
        return sorted(
            dist
            for dist_dict in self._distances.values()
            for dist in dist_dict.values()
        )


class KCenterDecisionVariant:
    def __init__(self, distances: Distances, k: int) -> None:
        self.distances = distances
        # Solution model
        self.k = k
        self.solver = SATSolver("Minicard")
        self.variables = list(self.distances.graph.nodes)
        self.solver.add_atmost(lits=self.variables, k=self.k) 
        self._solution: list[NodeId] | None = None
        self.status = False

    def limit_distance(self, limit: float) -> None:
        """Adds constraints to the SAT solver to ensure coverage within the given distance."""
        logging.info("Limiting to distance: %f", limit)
        for var_index, var in enumerate(self.variables):
            self.solver.add_clause([vertex for vertex in self.distances.vertices_in_range(var, limit)])

    def solve(self) -> list[NodeId] | None:
        """Solves the SAT problem and returns the list of selected nodes, if feasible."""
        
        
        self.status = self.solver.solve()
        self._solution = self.solver.get_model()
        return self._solution

    def get_solution(self) -> list[NodeId]:
        """Returns the solution if available; raises an error otherwise."""
        if self._solution is None:
            msg = "No solution available. Ensure `solve` is called first."
            raise ValueError(msg)
        return self._solution




class KCentersSolver:
    def __init__(self, graph: nx.Graph) -> None:
        """
        Creates a solver for the k-centers problem on the given networkx graph.
        The graph may not be complete, and edge weights are used to represent distances.
        """
        self.graph = graph
        self.distances = Distances(self.graph)
        

    def solve_heur(self, k: int) -> list[NodeId]:
        """
        Calculate a heuristic solution to the k-centers problem.
        Returns the k selected centers as a list of node IDs.
        """
        if k == 0:
            return None
        
        centers = [list(self.distances.graph.nodes)[0]]
        for i in range(k-1):
            selected = False
            max_dist = self.distances.max_dist(centers)
            for u in centers:
                for v in self.distances.graph.nodes:
                    if self.distances.dist(u, v) == max_dist:
                        centers.append(v)
                        selected = True
                        break
                if selected:
                    break
            
        return centers


    def solve(self, k: int) -> list[NodeId]:
        """
        Calculate the optimal solution to the k-centers problem for the given k.
        Returns the selected centers as a list of node IDs.
        """
        # Start with a heuristic solution
        centers = self.solve_heur(k)
        obj = self.distances.max_dist(centers)

        # TODO: Implement me!
        decision_solver = KCenterDecisionVariant(self.distances, k)
        bounds = list((self.distances.sorted_distances()))
        first_index = 0
        # print(first_index)
        # for index, bound in enumerate(bounds):
        #     if bound > obj:
        #         first_index = index-1 if index > 0 else 0
        #         break
        # print(first_index)
        index = bisect.bisect_left(bounds, obj)
        
        solution = None
        while index >= 0:
            decision_solver.limit_distance(bounds[index])
            decision_solver.solve()
            if decision_solver.status:
                solution = decision_solver.get_solution()
                centers_solution = [center for center in solution if center > 0]
                new_index = bisect.bisect_left(bounds, self.distances.max_dist(centers_solution))
                index = min(index - 1, new_index) 
            else:
                break
        # implement binary search to reduce the limiting constraints
        # for i in range(first_index, len(bounds)):
        #     decision_solver.limit_distance(bounds[i])
        #     decision_solver.solve()
        #     if decision_solver.status:
        #         solution = decision_solver.get_solution()
        #     else:
        #         break
        return [center for center in solution if center > 0]

if __name__ == "__main__":
    import pathlib
    import pickle
    CWD = pathlib.Path(__file__).parent
    instance_path: pathlib.Path = CWD / "./instances/att48.pickle"
    with instance_path.open("rb") as f:
        graph: nx.Graph = pickle.load(f)
    dists = Distances(graph)
    KCentersSolver(graph).solve(4)