

from graph_coloring.solvers import *
from graph_coloring.solvers import __all__ as all_solvers
from graph_coloring.preprocessing import DegreeBasedPreprocessor

from graph_coloring.heuristics import __all__ as all_heuristics
from graph_coloring.heuristics import *

from graph_coloring.heuristics import DSATUR

from utils.load_instance import load_instance
from utils.coloring import is_valid_coloring

import networkx as nx
import random
import json
import pandas as pd
import math
import signal


results = []
random.seed(42)

def handle_sigint(signom, frame):
    df = pd.DataFrame(results)
    df.to_csv("./evaluations/results.csv", index=False)
    
    exit(0)
    
signal.signal(signal.SIGINT, handle_sigint)

def main():
    instances = ["jean.col", "huck.col", "zeroin.i.1.col", "fpsol2.i.1.col", "fpsol2.i.2.col", "fpsol2.i.3.col", "le450_15b.col", "le450_15c.col", "le450_15d.col", "le450_25a.col", "le450_25b.col", "le450_25c.col", "le450_25d.col", "le450_5a.col", "le450_5b.col", "le450_5c.col", "le450_5d.col"]
    # instances = ["jean.col", "huck.col", "zeroin.i.1.col", "le450_15b.col"]
    print("GRAPH GEN STARTED")
    graphs = [nx.barabasi_albert_graph(random.randint(100, 250), random.randint(5, 10)) for i in range(100)]
    print("GRAPH GEN FINISHED")
    
    
    instance_count = 1
    # for i, graph in enumerate(graphs):
    # for instance in instances:
    #     graph, chromatic = load_instance(instance)
    #     dsatur_solver = DSATUR(graph.copy())
    #     upper_dsatur = dsatur_solver.solve()
    #     print("--------------------------",instance_count,"-----------------------")
        
    #     solver_count = 1
    #     for solver_name in all_solvers:
    #         if solver_name not in ["GCSolver", "PYSATDecisionVariant", "REPILPSolverCPSat", "REPILPSolverGurobi"]:
    #             print("--------------------------",instance_count, "--" ,solver_count, "--", solver_name,"-----------------------")
    #             solver_count += 1
    #             Solver = globals()[solver_name]
                
    #             solver_name = Solver.__name__
                
    #             solver = Solver(graph.copy(), upper_dsatur)
                
                
    #             try:
    #                 solution = solver.solve(timelimit=60)
    #                 results.append({
    #                     "instance": instance,
    #                     "solver": solver_name,
    #                     "metric": solution.colors
    #                 })
    #             except Exception as e:
    #                 print(f"Error while solving with {solver_name}: {e}")
    #     instance_count += 1
        
    
    # for instance in instances:
    #     graph, chromatic = load_instance(instance)
        
        
    #     dsatur_solver = DSATUR(graph.copy())
    #     upper_dsatur = dsatur_solver.solve()
    #     print("--------------------------",instance_count,"-----------------------")
        
    #     solver_count = 1
    #     for solver_name in all_solvers:
    #         if solver_name in ["REPILPSolverCPSat", "REPILPSolverGurobi"]:
    #             print("--------------------------",instance_count, "--" ,solver_count, "--", solver_name,"-----------------------")
    #             solver_count += 1
    #             Solver = globals()[solver_name]
                
    #             
                
    #             preprocessor = DegreeBasedPreprocessor(graph)
    #             reduced_graph = preprocessor.preprocess()
                
    #             solver = Solver(reduced_graph, upper_dsatur)
                
                
    #             try:
    #                 solution = solver.solve(timelimit=60)
    #                 postprocessed_sol = preprocessor.postprocess(solution)
    #                 results.append({
    #                     "instance": instance,
    #                     "solver": f"{solver_name} Preprocessed",
    #                     "metric": postprocessed_sol.colors
    #                 })
    #             except Exception as e:
    #                 print(f"Error while solving with {solver_name}: {e}")
    #     instance_count += 1
    
    for graph in graphs:
        # graph, chromatic = load_instance(instance)
        
        heuristic_count = 1        
        for heuristic_name in all_heuristics:
            
            print("--------------------------",instance_count, "--" ,heuristic_count, "--", heuristic_name,"-----------------------")
            heuristic_count += 1
            Heuristic = globals()[heuristic_name]
            
            
            
            
            heuristic = Heuristic(graph)
            
            
            try:
                solution = heuristic.solve()
                results.append({
                    "instance": str(instance_count),
                    "solver": f"{heuristic_name}",
                    "metric": solution
                })
            except Exception as e:
                print(f"Error while solving with {heuristic_name}: {e}")
        instance_count += 1
    
    # for instance in instances:
    #     G, chromatic = load_instance(instance)
        
    #     assilp_solver_cpsat = NotEqualSolver(G)
    #     value_assilp_cpsat = assilp_solver_cpsat.solve(timelimit=10)
    #     solution_assilp_cpsat = assilp_solver_cpsat.get_graph()
    #     assert is_valid_coloring(solution_assilp_cpsat)
        
    #     results.append({
    #         "instance": instance,
    #         "solver": "ASSCPSAT",
    #         "metric": value_assilp_cpsat 
    #     })
        

    # for instance in instances:
    #     G, chromatic = load_instance(instance)
        
    #     assilp_solver_gurobi = AllDifferentSolver(G)
    #     solution_all_different = assilp_solver_gurobi.solve(timelimit=10)
    #     if solution_all_different.colors != math.inf:
    #         assert is_valid_coloring(solution_all_different.graph)
        
    #     results.append({
    #         "instance": instance,
    #         "solver": "ASSGUROBI",
    #         "metric": solution_all_different.colors 
    #     })
    
    
    df = pd.DataFrame(results)
    df.to_csv("./evaluations/results.csv", index=False)
    
    
