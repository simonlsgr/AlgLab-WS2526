import math
from enum import Enum

import networkx as nx
from _timer import Timer
from solution_hamiltonian import HamiltonianCycleModel


class SearchStrategy(Enum):
    """
    Different search strategies for the solver.
    """

    SEQUENTIAL_UP = 1  # Try smallest possible k first.
    SEQUENTIAL_DOWN = 2  # Try any improvement.
    BINARY_SEARCH = 3  # Try a binary search for the optimal k.

    def __str__(self):
        return self.name.title()

    @staticmethod
    def from_str(s: str):
        return SearchStrategy[s.upper()]


class BottleneckTSPSolver:
    def __init__(self, graph: nx.Graph) -> None:
        """
        Creates a solver for the Bottleneck Traveling Salesman Problem on the given networkx graph.
        You can assume that the input graph is complete, so all nodes are neighbors.
        The distance between two neighboring nodes is a numeric value (int / float), saved as
        an edge data parameter called "weight".
        There are multiple ways to access this data, and networkx also implements
        several algorithms that automatically make use of this value.
        Check the networkx documentation for more information!
        """
        self.graph : nx.Graph = graph
        self.sorted_weights = sorted(list(nx.get_edge_attributes(self.graph, "weight").values()))
        

    def lower_bound(self) -> float:
        # TODO: Implement me!
        return 0

    def optimize_bottleneck(
        self,
        time_limit: float = math.inf,
        search_strategy: SearchStrategy = SearchStrategy.BINARY_SEARCH,
    ) -> list[tuple[int, int]] | None:
        """
        Find the optimal bottleneck tsp tour.
        """

        self.timer = Timer(time_limit)
        upper_i = len(self.sorted_weights) -1
        lower_i = 0
        index = 0
        last_sol = "X"
        current_sol = "X"
        while lower_i <= upper_i:
            
            index = lower_i + ((upper_i - lower_i) // 2)
            
            edges_for_graph = [edge for edge in self.graph.edges if self.graph.edges[edge]["weight"] <= self.sorted_weights[index]]
            graph = nx.Graph(edges_for_graph)
            current_sol = HamiltonianCycleModel(graph).solve()
            if current_sol is None:
                lower_i = index +1
            else:
                upper_i = index - 1
                last_sol = current_sol
        
        return last_sol
        

if __name__ == "__main__":
    import pathlib
    import pickle
    CWD = pathlib.Path(__file__).parent
    filepath = CWD / "./instances/att48.tsp.pickle"
    with filepath.open("rb") as f:
        graph = pickle.load(f)
        
    BottleneckTSPSolver(graph).optimize_bottleneck()