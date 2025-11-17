"""
Implement the Dantzig-Fulkerson-Johnson formulation for the TSP.
"""

import logging
import typing

import gurobipy as gp
import networkx as nx


class GurobiTspSolver:
    """
    IMPLEMENT ME!
    """

    def __init__(self, G: nx.Graph, k: int = 2):
        """
        G is a weighted networkx graph, where the weight of an edge is stored in the
        "weight" attribute. It is strictly positive.
        """
        self.graph = G
        assert (
            G.number_of_edges() == G.number_of_nodes() * (G.number_of_nodes() - 1) / 2
        ), "Invalid graph"
        assert all(
            weight > 0
            for _, _, weight in G.edges.data("weight", default=None)  # type: ignore[attr-defined]
        ), "Invalid graph"
        assert k in {1, 2}, "Invalid k"
        self.k = k
        logging.info("Creating model ...")
        logging.info(
            "Graph has %d nodes and %d edges", G.number_of_nodes(), G.number_of_edges()
        )
        logging.info("Implementing subtour elimination with >= %d", k)
        self._model = gp.Model()
        self.solution = None

        # init vars
        for edge in self.graph.edges:
            self.graph.edges[edge]["var"] = self._model.addVar(
                vtype=gp.GRB.BINARY, name=f"edge{str(edge)}"
            )

        # obj minimize weight of used edges
        self._model.setObjective(
            gp.quicksum(
                self.graph.edges[edge]["var"] * self.graph.edges[edge]["weight"]
                for edge in self.graph.edges
            ),
            gp.GRB.MINIMIZE,
        )

        # constraint deg = 2
        for v in self.graph.nodes:
            self._model.addConstr(
                gp.quicksum(
                    self.graph.edges[edge]["var"] for edge in self.graph.edges(v)
                )
                == 2
            )

        # constraint cycle
        self._model.addConstr(
            gp.quicksum(self.graph.edges[edge]["var"] for edge in self.graph.edges)
            == len(self.graph.nodes)
        )

    def get_lower_bound(self) -> float:
        """
        Return the current lower bound.
        """
        return self._model.ObjBound if self._model.ObjBound else 0

    def get_solution(self) -> typing.Optional[nx.Graph]:
        """
        Return the current solution as a graph.
        """
        return self.solution

    def get_objective(self) -> typing.Optional[float]:
        """
        Return the objective value of the last solution.
        """
        return self._model.ObjVal if self._model.ObjVal else 0

    def solve(self, time_limit: float, opt_tol: float = 0.001) -> None:
        """
        Solve the model. After solving the model, the solution, its objective value,
        and the lower bounds should be available via the corresponding methods.
        """
        logging.info("Solving model ...")
        # Set parameters for the solver.
        self._model.Params.LogToConsole = 1
        self._model.Params.TimeLimit = time_limit
        self._model.Params.LazyConstraints = 1
        self._model.Params.MIPGap = (
            opt_tol  # https://www.gurobi.com/documentation/11.0/refman/mipgap.html
        )

        def callback(model, where):
            if where == gp.GRB.Callback.MIPSOL:
                edges_in_solution = []
                for edge in self.graph.edges:
                    if self._model.cbGetSolution(self.graph.edges[edge]["var"]) > 0.5:
                        edges_in_solution.append(edge)

                graph = nx.Graph(edges_in_solution)
                components = list(nx.connected_components(graph))

                if len(components) == 1:
                    return  # solution is connected

                for component in components:
                    necessary_edges = [
                        self.graph.edges[u, v]["var"]
                        for (u, v) in self.graph.edges
                        if (u in component and v not in component)
                        or (u not in component and v in component)
                    ]
                    self._model.cbLazy(gp.quicksum(necessary_edges) >= self.k)

        self._model.Params.LazyConstraints = 1
        self._model.optimize(callback)

        if self._model.status == gp.GRB.OPTIMAL:
            logging.info("Optimal solution found.")
            logging.info("Objective value: %f", self._model.ObjVal)

        if self._model.SolCount > 0:
            logging.info("Feasible solution found, but not proven optimal.")
            logging.info("Objective value: %f", self._model.ObjVal)

        edges_in_solution = []
        for edge in self.graph.edges:
            if self.graph.edges[edge]["var"].X > 0.5:
                edges_in_solution.append(edge)
        self.solution = nx.Graph(edges_in_solution)

        return None
