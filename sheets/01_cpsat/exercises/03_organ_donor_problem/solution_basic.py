import math

import networkx as nx
from data_schema import Donation, Solution
from database import TransplantDatabase
from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver, LinearExpr


def build_recipient_donor_graph(database: TransplantDatabase) -> nx.DiGraph:
    G = nx.DiGraph()
    
    recipients = database.get_all_recipients()
    for recipient in recipients:
        G.add_node(recipient)
    
    
    # misunterstood the assignment, where i wouldve had to keep track of all donors in a 1 to 1 relation between two recipients
    # for recipient in recipients:
    #     r = {}
    #     donors = database.get_partner_donors(recipient)
        
    #     for donor in donors:
            
    #         possible_partner_recipients = database.get_compatible_recipients(donor)
    #         for possibile_partner_recipient in possible_partner_recipients:
    #             if possibile_partner_recipient not in r:
    #                 r[possibile_partner_recipient] = [donor]
    #             else:
    #                 r[possibile_partner_recipient].append(donor)
        
    #     for key, value in enumerate(r):
    #         G.add_edge(recipient, value, donors=r[value])
    
    
    for recipient in recipients:
        donors = database.get_partner_donors(recipient)
        for donor in donors:
            possible_partner_recipients = database.get_compatible_recipients(donor)
            for possible_partner_recipient in possible_partner_recipients:
                
                G.add_edge(recipient, possible_partner_recipient, donor=donor)
                
    # import matplotlib.pyplot as plt
    # nx.draw_networkx(G)
    # plt.draw()
    # plt.show()
    
    return G

class CrossoverTransplantSolver:
    def __init__(self, database: TransplantDatabase) -> None:
        """
        Constructs a new solver instance, using the instance data from the given database instance.
        :param Database database: The organ donor/recipients database.
        """
        self.database = database
        
        
        self.model = CpModel()
        
        print("Creating Graph...")
        self.graph = build_recipient_donor_graph(self.database)
        
        
        
            
        # misunterstood the assignment, see line 17
        # self.vars = [
        #         [
        #             [
        #                 self.model.new_bool_var(f"node{node.id}_to_node{adjacent.id}_with_donor_{possible_donor.id}") for possible_donor in self.graph.get_edge_data(node,adjacent)["donors"]
        #             ]
        #             for adjacent in self.graph.neighbors(node)
        #         ]
        #     for node in self.graph]
        
        # x[i, j] = 1, if donor of recipient i donates to the jth possible recipient
        
        # self.y = []
        
        # # for i, edge in enumerate(self.graph.edges):
        # for i, node in enumerate(self.graph.nodes):
        #     bool_vars = []
        #     for j, edge in enumerate(self.graph.out_edges(node)):
        #         bool_vars.append(self.model.new_bool_var(f"y_{i}_{j}"))
        #     self.y.append(bool_vars)
        
        
        # # donor only donates, if paired recipient receives organ transplant
        # for i, recipient_list in enumerate(self.y):
        #     for j, recipient_succ in enumerate(recipient_list):
        #         # self.y[i][j] i.e. using edge i,j => one incoming edge of i must be true
        #         self.model.add_bool_or([~self.y[i][j]] + [self.y[edge[0].id-1][i] for edge in self.graph.in_edges(list(self.graph.nodes)[i]) if len(self.y[edge[0].id-1]) > i])
        
        # # recipient may only receive one organ transplant i.e. only one incoming edge is used
        # for i, recipient_list in enumerate(self.y):
        #     for j, recipient_succ in enumerate(recipient_list):
        #         self.model.add(sum([self.y[edge[0].id-1][i] for edge in self.graph.in_edges(list(self.graph.nodes)[i]) if len(self.y[edge[0].id-1]) > i]) <= 1)
        
        
        # # only one out edge
        # for i, recipient_list in enumerate(self.y):
        #     self.model.add_at_most_one([l for l in recipient_list])    
                
                
                
        
              
        self.nodes = list(self.graph.nodes)
        self.nodes_index = {node: id for id, node in enumerate(self.nodes)}
        self.x = {}
        for i, recipient_node in enumerate(self.nodes):
            for recipient_succ_node in self.graph.successors(recipient_node):
                j = self.nodes_index[recipient_succ_node]
                self.x[i, j] = self.model.new_bool_var(f"x_{i}_{j}")
        
        
        # print(self.nodes[1])
        # print(self.nodes_index[self.nodes[1]])
        # print([ self.database.get_partner_recipient(donor) for donor in self.database.get_compatible_donors(self.nodes[0])])
        # for (i,j), var in self.x.items():
        #     if j ==
        # print(self.x)
        
        
        for i in range(len(self.nodes)):
            outgoing_edges_vars = [self.x[i, j] for (k, j) in self.x.keys() if k == i]
            self.model.add(sum(outgoing_edges_vars) <= 1)
            
            incoming_edges_vars = [self.x[k, i] for (k, j) in self.x.keys() if j == i]
            self.model.add(sum(incoming_edges_vars) <= 1)
            
            self.model.add(sum(incoming_edges_vars) == sum(outgoing_edges_vars))
            
        objective = []
        for var in self.x.values():
            objective.append(var)
        
        self.model.maximize(sum(objective))
        
        
        # print(len(self.x))
        # # donor only donates if paired recipient receives organ
        # for i, recipient in enumerate(self.graph):
        #     for j, recipient_succ in enumerate(self.graph.successors(recipient)):
        #         xij_predecessors = []
        #         for tup in self.x:
        #             if tup[1] == i:
        #                 xij_predecessors.append(self.x[tup])
        #         self.model.add_bool_or([~self.x[i, j]] + xij_predecessors)
        #         print(xij_predecessors)
        #         self.model.add(sum(xij_predecessors) <= 1)
        #         xij_successors = []
        #         for k, rec_succ in enumerate(self.graph.successors(recipient)):
        #             xij_successors.append(self.x[i, k])
                    
        #         self.model.add(sum(xij_predecessors) <= sum(xij_successors))
        # # donors of one recipient only donate to one other recipient
        # for i, recipient in enumerate(self.graph):
        #     self.model.add_at_most_one([self.x[i, j] for j, recipient_succ in enumerate(self.graph.successors(recipient))])
        
        # # recipient may only receive one organ
        
        # # for i, recipient in enumerate(self.graph):
        # #     # print("---------------")
        # #     # print(recipient)
        # #     # print([tup for tup in self.x if tup[1] == i])
        # #     # print()
        # #     # print([self.x[recipient_pre.id-1,recipient.id-1] for recipient_pre in self.graph.predecessors(recipient)])
                
        # #     self.model.add_at_most_one([self.x[tup] for tup in self.x if tup[1] == i])
        
        
        
        # objective = []
        # for i, recipient1 in enumerate(self.graph):
        #     for j, recipient2 in enumerate(self.graph.successors(recipient1)):
        #         objective.append(LinearExpr.term(self.x[i, j], 1))
        # self.model.maximize(LinearExpr.sum(objective))
        
        # # objective = []
        # # for i, recipient_list in enumerate(self.y):
        # #     for j, bool_var in enumerate(recipient_list):
        # #         objective.append(bool_var)
            

        # # self.model.maximize(sum(objective))
            
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
        
        
        



    def optimize(self, timelimit: float = math.inf) -> Solution:
        """
        Solves the constraint programming model and returns the optimal solution (if found within time limit).
        :param timelimit: The maximum time limit for the solver.
        :return: A list of Donation objects representing the best solution, or None if no solution was found.
        """
        if timelimit <= 0.0:
            return Solution(donations=[])
        if timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        
        donations = []
        status = self.solver.solve(self.model)
        
        
        for (i,j), var in self.x.items():
            if self.solver.value(var):
                recipient = self.nodes[i] # actual instance of recipient class not an index or simple integer
                recipient_succ = self.nodes[j]
                donor = self.graph.get_edge_data(recipient, recipient_succ)["donor"]
                donations.append(Donation(donor=donor, recipient=recipient_succ))
                
        
        # for i, recipient in enumerate(self.graph):
        #     for j, recipient_succ in enumerate(self.graph.successors(recipient)):
        #         if self.solver.value(self.x[i, j]):
        #             donations.append(Donation(donor=self.graph.get_edge_data(recipient, recipient_succ)["donor"], recipient=recipient_succ))
        # # for i, recipient_list in enumerate(self.y):
        # #     for j, edge_bool in enumerate(recipient_list):
        # #         if self.graph.get_edge_data(list(self.graph.nodes)[i], list(self.graph.nodes)[j]) is not None:
        # #             donations.append(Donation(donor=self.graph.get_edge_data(list(self.graph.nodes)[i], list(self.graph.nodes)[j])["donor"], recipient=list(self.graph.nodes)[j]))
                
                    
                
        return Solution(donations=donations)
    
if __name__ == "__main__":
    from _db_impl import SqliteTransplantDatabase
    db = SqliteTransplantDatabase("instances/1000.db")
    
    solver = CrossoverTransplantSolver(db)
    
    print(solver.optimize())
    