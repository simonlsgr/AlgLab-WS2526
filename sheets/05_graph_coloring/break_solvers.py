
from graph_coloring.heuristics import NaiveGreedyGraphColoringHeuristic, MultiStartGreedyGraphColoringHeuristic, DSATUR

from graph_coloring.preprocessing import DegreeBasedPreprocessor

from graph_coloring.solvers import *

from utils.load_instance import load_instance
from utils.coloring import is_valid_coloring

from utils.data_schema import Solution, ModelStatus


if __name__ == "__main__":
    G, chromatic = load_instance("le450_15b.col")
    G_copy = G.copy()

    rep_solver_cpsat = REPILPSolverCPSat(G)

    solution_rep_cpsat = rep_solver_cpsat.solve()
    print(is_valid_coloring(solution_rep_cpsat.graph))
    print(solution_rep_cpsat.colors)
    
    
    rep_solver_gurobi = REPILPSolverGurobi(G_copy)
    
    solution_rep_gurobi = rep_solver_gurobi.solve()
    print(is_valid_coloring(solution_rep_gurobi.graph))
    print(solution_rep_gurobi.colors)
    
    
   
