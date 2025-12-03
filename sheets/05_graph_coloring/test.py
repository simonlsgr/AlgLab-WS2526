
from graph_coloring.heuristics import NaiveGreedyGraphColoringHeuristic, MultiStartGreedyGraphColoringHeuristic, DSATUR

from graph_coloring.preprocessing import DegreeBasedPreprocessor

from graph_coloring.solvers import *

from utils.load_instance import load_instance
from utils.coloring import is_valid_coloring
from utils._timer import Timer

from utils.data_schema import Solution, ModelStatus

import networkx as nx
import random
import iplotx as ipx
import matplotlib.pyplot as plt

if __name__ == "__main__":
    G, chromatic = load_instance("fpsol2.i.3.col")
    # seed = random.seed(100)
    G = nx.erdos_renyi_graph(75, .25)
    G_copy = G.copy()
    G_copy_2 = G.copy()
    G_copy_3 = G.copy()
    # greedy_solver = NaiveGreedyGraphColoringHeuristic(G)
    # upper = greedy_solver.solve()
    # print(is_valid_coloring(greedy_solver.graph))
    # multi_greedy_solver = MultiStartGreedyGraphColoringHeuristic(G_copy)
    # upper_multi = multi_greedy_solver.solve()
    dsatur_solver = DSATUR(G_copy_2)
    upper_dsatur = dsatur_solver.solve()
    print(upper_dsatur)
    # print(is_valid_coloring(dsatur_solver.graph))
    
    solver = ASSILPSolverGurobi(G)
    solution = solver.solve(timelimit=40)
    print(solution)
    
    
    


    
    