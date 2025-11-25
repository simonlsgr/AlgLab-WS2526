import networkx as nx
import random

class NaiveGreedyGraphColoringHeuristic:
    def __init__(self, instance: nx.Graph, random_order: bool = False):
        self.order = list(range(0,len(list(instance.nodes()))))
        if random_order:
            random.shuffle(self.order)
        self.graph = instance
        self.nodes = list(self.graph.nodes)
        for node in self.nodes:
            self.graph.nodes[node]["color"] = -1
        self.bound = -1
        
    def solve(self):
        
        for i in self.order:
            colors = [self.graph.nodes[neighbor]["color"] for neighbor in self.graph.neighbors(self.nodes[i]) if self.graph.nodes[neighbor]["color"] != -1]
            colors.sort()
            
            chosen_color = 0
            for color in colors:
                if chosen_color == color:
                    chosen_color += 1
                elif color > chosen_color:
                    break
            
            self.graph.nodes[self.nodes[i]]["color"] = chosen_color
            
                    
        used = {self.graph.nodes[i]["color"] for i in self.nodes}
        self.bound = len(used)
        return self.bound
