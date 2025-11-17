import logging

import gurobipy as gp
import networkx as nx
from data_schema import Instance, Solution
from gurobipy import GRB


class MiningRoutingSolver:
    def __init__(self, instance: Instance) -> None:
        self.instance = instance
        self.budget = instance.budget
        logging.info("Creating model ...")
        logging.info(
            "Instance has %d locations, %d mines, %d tunnels, and a budget of %.2f",
            len(instance.locations),
            len(instance.mines),
            len(instance.tunnels),
            instance.budget,
        )
        self.model = gp.Model()

        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(instance.locations, node_type="mine")
        self.graph.nodes[instance.elevator_location]["node_type"] = "elevator"

        for location, mine in instance.mines.items():
            self.graph.nodes[mine.location]["oph"] = mine.ore_per_hour

        total_cost = 0
        for tunnel in instance.tunnels:
            # data structure
            self.graph.add_edge(
                tunnel.source,
                tunnel.target,
                # given data
                throughput=tunnel.throughput_per_hour,
                maintenence_costs=tunnel.reinforcement_costs,
                # decision vars
                used=self.model.addVar(
                    vtype=GRB.BINARY, name=f"used_{tunnel.source}_to_{tunnel.target}"
                ),
                flow=self.model.addVar(
                    vtype=GRB.INTEGER,
                    name=f"flow_{tunnel.source}_to_{tunnel.target}",
                    lb=0,
                    ub=tunnel.throughput_per_hour,
                ),
            )

            self.graph.add_edge(
                tunnel.target,
                tunnel.source,
                # given data
                throughput=tunnel.throughput_per_hour,
                maintenence_costs=tunnel.reinforcement_costs,
                # decision vars
                used=self.model.addVar(
                    vtype=GRB.BINARY, name=f"used_{tunnel.target}_to_{tunnel.source}"
                ),
                flow=self.model.addVar(
                    vtype=GRB.INTEGER,
                    name=f"flow_{tunnel.target}_to_{tunnel.source}",
                    lb=0,
                    ub=tunnel.throughput_per_hour,
                ),
            )

            # constraints
            total_cost += tunnel.reinforcement_costs * (
                self.graph.edges[tunnel.source, tunnel.target]["used"]
                + self.graph.edges[tunnel.target, tunnel.source]["used"]
            )
            # one direction only
            self.model.addConstr(
                self.graph.edges[tunnel.source, tunnel.target]["used"]
                + self.graph.edges[tunnel.target, tunnel.source]["used"]
                <= 1
            )

            # directed flow
            self.model.addConstr(
                self.graph.edges[tunnel.source, tunnel.target]["flow"]
                <= self.graph.edges[tunnel.source, tunnel.target]["used"]
                * tunnel.throughput_per_hour
            )
            self.model.addConstr(
                self.graph.edges[tunnel.target, tunnel.source]["flow"]
                <= self.graph.edges[tunnel.target, tunnel.source]["used"]
                * tunnel.throughput_per_hour
            )

        self.model.addConstr(total_cost <= instance.budget)

        # adress error: There is more ore leaving mine x than entering + produced!
        for mine_node in self.graph.nodes:
            incoming_edges = [(v, mine_node) for v in self.graph.neighbors(mine_node)]
            outgoing_edges = [(mine_node, v) for v in self.graph.neighbors(mine_node)]

            incoming_ore = gp.quicksum(
                self.graph.edges[edge]["flow"] for edge in incoming_edges
            )
            outgoing_ore = gp.quicksum(
                self.graph.edges[edge]["flow"] for edge in outgoing_edges
            )

            if self.graph.nodes[mine_node]["node_type"] == "elevator":
                self.model.addConstr(outgoing_ore == 0)
            elif self.graph.nodes[mine_node]["node_type"] == "mine":
                self.model.addConstr(
                    incoming_ore + self.graph.nodes[mine_node]["oph"] >= outgoing_ore
                )

        self.model.setObjective(
            gp.quicksum(
                self.graph.edges[neighbor, instance.elevator_location]["flow"]
                for neighbor in self.graph.neighbors(instance.elevator_location)
            ),
            GRB.MAXIMIZE,
        )

    def solve(self) -> Solution:
        """
        Calculate the optimal solution to the problem.
        Returns the "flow" as a list of tuples, each tuple with two entries:
            - The *directed* edge tuple. Both entries in the edge should be ints, representing the ids of locations.
            - The throughput/utilization of the edge, in goods per hour
        """
        logging.info("Solving model...")

        self.model.optimize()
        if self.model.status == GRB.OPTIMAL:
            logging.info("Optimal solution found.")
            logging.info("Objective value: %f", self.model.ObjVal)

        if self.model.SolCount > 0:
            logging.info("Feasible solution found, but not proven optimal.")
            logging.info("Objective value: %f", self.model.ObjVal)

        flow = []
        for e in self.graph.edges:
            if self.graph.edges[e]["flow"].X > 0.01:
                flow.append((e, self.graph.edges[e]["flow"].X))
        return Solution(flow=flow)


if __name__ == "__main__":
    from pathlib import Path

    CWD = Path(__file__).parent
    filepath = CWD / "./instances/instance_200.json"
    with filepath.open() as f:
        logging.info("Loading instance from %s ...", filepath)
        instance: Instance = Instance.model_validate_json(f.read())
        MiningRoutingSolver(instance).solve()
