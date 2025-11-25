import networkx as nx
import json

def load_instance(path):
    """ Returns a DIMACS instance as a networkx graph. If the chromatic number is supplied in the chromatic.json file, then this is also suplied in the output. 

    Args:
        path (str): Name of the instance file in the instance folder

    Returns:
        nx.Graph: Graph of the instance
        int: Chromatic number of the Graph or -1 if unknown
    """
    G = nx.Graph()
    with open("./instances/"+path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c'):   
                continue
            if line.startswith('p'):              
                _, _, n, _ = line.split()
                G.add_nodes_from(range(1, int(n) + 1))
            if line.startswith('e'):              
                _, u, v = line.split()
                G.add_edge(int(u), int(v))
    with open("./instances/chromatic.json") as f:
        chromatic_numbers = json.load(f)
    
    try:
        return G, chromatic_numbers[path]
    except:
        return G, -1

if __name__ == "__main__":
    
    G, chromatic = load_instance("fpsol2.i.3.col")
    print(G,"Chi(G)",chromatic)
