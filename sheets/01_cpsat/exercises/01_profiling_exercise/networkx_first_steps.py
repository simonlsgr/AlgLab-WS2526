import networkx as nx

G = nx.Graph()


G.add_node("A")
G.add_node("B")
G.add_node("C")
G.add_node("D")


G.add_edge("A", "B")
G.add_edge("B", "C")
G.add_edge("C", "A")


print(G.nodes)
print(G.edges)


print(list(G.neighbors("A")))

print(G.nodes["A"])
print(G.edges[("A", "B")])

print(nx.shortest_path(G, "A", "C"))

for component in nx.connected_components(G):
    print(component)
    