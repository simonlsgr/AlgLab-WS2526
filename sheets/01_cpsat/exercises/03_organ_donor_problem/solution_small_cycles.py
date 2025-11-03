import math
from collections import defaultdict

import networkx as nx
from data_schema import Donation, Solution
from database import TransplantDatabase
from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver

from typing import List
from data_schema import Recipient

from _alglab_utils import logging

def build_recipient_donor_graph(database: TransplantDatabase) -> nx.DiGraph:
    G = nx.DiGraph()
    
    recipients = database.get_all_recipients()
    for recipient in recipients:
        G.add_node(recipient)
    
    for recipient in recipients:
        donors = database.get_partner_donors(recipient)
        for donor in donors:
            possible_partner_recipients = database.get_compatible_recipients(donor)
            for possible_partner_recipient in possible_partner_recipients:
                
                G.add_edge(recipient, possible_partner_recipient, donor=donor)

    return G



    
        
    

class CycleLimitingCrossoverTransplantSolver:
    def __init__(self, database: TransplantDatabase) -> None:
        """
        Constructs a new solver instance, using the instance data from the given database instance.
        :param Database database: The organ donor/recipients database.
        """

        self.database = database
        
        
        self.model = CpModel()
        
        logging.info("Creating Graph...")
        self.graph = build_recipient_donor_graph(self.database)
        self.nodes = list(self.graph.nodes)
        
        print("number of edges: ", len(list(self.graph.edges)))
        print("number of nodes: ",len(list(self.graph.nodes)))
        
        
        self.cycles = list(nx.simple_cycles(self.graph, length_bound=3))
        
        
        self.x = [self.model.new_bool_var(f"x_{i}") for i in range(len(self.cycles))]
        
        # constraint:
        # each recipient shall only occur at most once in the used cycles
        for i, recipient in enumerate(self.nodes):
            cycles_with_recipient = []
            for j, cycle in enumerate(self.cycles):
                for k, recipient_cycle in enumerate(cycle):
                    if recipient == recipient_cycle:
                        cycles_with_recipient.append(j)
            
            self.model.add(sum([self.x[j] for j in cycles_with_recipient]) <= 1)
            
        
        self.model.maximize(sum([len(self.cycles[i]) * self.x[i]for i in range(len(self.cycles))]))

        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
    
    
    def add_cycle_to_donations(self, donations: List[Donation], cycle: List[Recipient]) -> None:
    
        if len(cycle) == 2:
            donor = self.graph.get_edge_data(cycle[0], cycle[1])["donor"]
            donations.append(Donation(donor=donor, recipient=cycle[1]))
            donor = self.graph.get_edge_data(cycle[1], cycle[0])["donor"]
            donations.append(Donation(donor=donor, recipient=cycle[0]))
            
        if len(cycle) == 3:
            donor = self.graph.get_edge_data(cycle[0], cycle[1])["donor"]
            donations.append(Donation(donor=donor, recipient=cycle[1]))
            donor = self.graph.get_edge_data(cycle[1], cycle[2])["donor"]
            donations.append(Donation(donor=donor, recipient=cycle[2]))
            donor = self.graph.get_edge_data(cycle[2], cycle[0])["donor"]
            donations.append(Donation(donor=donor, recipient=cycle[0]))


    def optimize(self, timelimit: float = math.inf) -> Solution:
        if timelimit <= 0.0:
            return Solution(donations=[])
        if timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        
        donations = []
        
        status = self.solver.solve(self.model)
        
        for i, cycle in enumerate(self.cycles):
            if self.solver.value(self.x[i]):
                self.add_cycle_to_donations(donations, cycle)
        return Solution(donations=donations)
        
        
        


if __name__ == "__main__":
    from _db_impl import SqliteTransplantDatabase
    db = SqliteTransplantDatabase("instances/20.db")
    
    solver = CycleLimitingCrossoverTransplantSolver(db)
    
    print(solver.optimize())