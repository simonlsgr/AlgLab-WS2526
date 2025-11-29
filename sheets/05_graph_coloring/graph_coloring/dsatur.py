import networkx as nx

class DSATUR:
    def __init__(self, instance: nx.Graph):
        self.graph = instance
        self.nodes = list(self.graph.nodes)
        for node in self.nodes:
            self.graph.nodes[node]["color"] = -1
        self.bound = -1
    
    def degree_of_saturation(self, node):
        colors = {-1}
        for neighbour in nx.neighbors(self.graph, node):
            colors.add(self.graph.nodes[neighbour]["color"])
        return len(colors) - 1

    def degree_uncolored_neighors(self, node):
        degree = 0
        for neighbour in nx.neighbors(self.graph, node):
                if self.graph.nodes[neighbour]["color"] == -1:
                    degree += 1
        
        return degree
    
    def get_most_saturated_nodes(self):
        max_saturated_nodes = []
        max_saturation = 0
        for node in self.nodes:
            if self.graph.nodes[node]["color"] == -1:
                saturation = self.degree_of_saturation(node)
                if  saturation > max_saturation:
                    max_saturation = saturation
                    max_saturated_nodes = [node]
                elif saturation == max_saturation:
                    max_saturated_nodes.append(node)
        return max_saturated_nodes

    def color_with_min_color(self, node):
        colors = [self.graph.nodes[neighbor]["color"] for neighbor in self.graph.neighbors(node) if self.graph.nodes[neighbor]["color"] != -1]
        colors.sort()
        
        chosen_color = 0
        for color in colors:
            if chosen_color == color:
                chosen_color += 1
            elif color > chosen_color:
                break
        
        self.graph.nodes[node]["color"] = chosen_color
    
    def solve(self):
        
        to_color = len(self.nodes)
        
        while to_color > 0:
            saturated_nodes = self.get_most_saturated_nodes()
            if len(saturated_nodes) == 1:
                self.color_with_min_color(saturated_nodes[0])
            else:
                degrees_uncolored = [self.degree_uncolored_neighors(saturated_node) for saturated_node in saturated_nodes]
                index_max_degree_uncolored = degrees_uncolored.index(max(degrees_uncolored))
                self.color_with_min_color(saturated_nodes[index_max_degree_uncolored])
            to_color -= 1
        
        used = {self.graph.nodes[i]["color"] for i in self.nodes}
        
        self.bound = len(used)
        return self.bound
    