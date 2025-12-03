

from graph_coloring.solvers import *
from graph_coloring.solvers import __all__ as all_solvers
from graph_coloring.preprocessing import DegreeBasedPreprocessor

from graph_coloring.heuristics import __all__ as all_heuristics
from graph_coloring.heuristics import *

from graph_coloring.heuristics import DSATUR

from utils.load_instance import load_instance
from utils.coloring import is_valid_coloring
from utils.data_schema import Solution, ModelStatus

import networkx as nx
import random
import json
import pandas as pd
import math
import signal



random.seed(42)

# def handle_sigint(signom, frame):
#     df = pd.DataFrame(results)
#     df.to_csv("./evaluations/results.csv", index=False)
    
#     exit(0)
    
# signal.signal(signal.SIGINT, handle_sigint)

def main():
    instances = ["jean.col", "huck.col", "zeroin.i.1.col", "fpsol2.i.1.col", "fpsol2.i.2.col", "fpsol2.i.3.col", "le450_15b.col", "le450_15c.col", "le450_15d.col", "le450_25a.col", "le450_25b.col", "le450_25c.col", "le450_25d.col", "le450_5a.col", "le450_5b.col", "le450_5c.col", "le450_5d.col"]
    # instances = ["jean.col", "huck.col", "zeroin.i.1.col", "le450_15b.col"]
    print("GRAPH GEN STARTED")
    # graphs1 = [nx.kneser_graph(random.randint(12,15), random.randint(2,4)) for i in range(10)]
    # random.seed(42)
    graphs1 = [nx.kneser_graph(random.randint(12,15), random.randint(2,4)) for i in range(10)]
    # graphs: chromatic_numbers =  [10, 12, 11, 6, 6, 13, 10, 11, 6, 7]
    # chromatic numbers = 
    # print([str(graph) for graph in graphs1])
    print("GRAPH GEN FINISHED")
    
    results = []
    instance_count = 1
    graph_class = "kneser_graph_"
    for i, graph in enumerate(graphs1):
    # for instance in instances:
        # graph, chromatic = load_instance(instance)
        dsatur_solver = DSATUR(graph.copy())
        upper_dsatur = dsatur_solver.solve()
        print("--------------------------",instance_count,"-----------------------")
        
        solver_count = 1
        for solver_name in all_solvers:
            
            
            if solver_name not in ["GCSolver", "PYSATDecisionVariant", "REPILPSolverCPSat", "REPILPSolverGurobi", "PYSATSolver"]:
            # if solver_name == "ASSILPSolverGurobi":
                print("--------------------------",instance_count, "--" ,solver_count, "--", solver_name,"-----------------------")
                solver_count += 1
                Solver = globals()[solver_name]
                
                solver_name = Solver.__name__
                
                solver = Solver(graph.copy(), upper_dsatur)
                
                
                try:
                    solution: Solution = solver.solve(timelimit=20)
                    if solution.status == ModelStatus.FEASIBLE and solution.lower_bound is not None:
                        results.append({
                            "instance": graph_class+str(instance_count),
                            "solver": solver_name,
                            "metric": solution.lower_bound
                        })
                        df = pd.DataFrame(results)
                        df.to_csv("./evaluations/results_best_lower_bound_kneser.csv", index=False)
                    elif solution.status == ModelStatus.OPTIMAL:
                        results.append({
                            "instance": graph_class+str(instance_count),
                            "solver": solver_name,
                            "metric": solution.colors
                        })
                        df = pd.DataFrame(results)
                        df.to_csv("./evaluations/results_best_lower_bound_kneser.csv", index=False)
                except Exception as e:
                    print(f"Error while solving with {solver_name}: {e}")
        
        instance_count += 1
        
    # instance_count = 1
    # for graph in graphs1:
    #     # graph, chromatic = load_instance(instance)
        
        
    #     dsatur_solver = DSATUR(graph.copy())
    #     upper_dsatur = dsatur_solver.solve()
    #     print("--------------------------",instance_count,"-----------------------")
        
    #     solver_count = 1
    #     for solver_name in all_solvers:
    #         if solver_name not in ["GCSolver", "PYSATDecisionVariant", "REPILPSolverCPSat", "REPILPSolverGurobi"]:
    #             print("--------------------------",instance_count, "--" ,solver_count, "--", solver_name,"-----------------------")
    #             solver_count += 1
    #             Solver = globals()[solver_name]
                
                
                
    #             preprocessor = DegreeBasedPreprocessor(graph)
    #             reduced_graph = preprocessor.preprocess()
                
    #             solver = Solver(reduced_graph, upper_dsatur)
                
                
    #             try:
    #                 solution = solver.solve(timelimit=60)
    #                 postprocessed_sol = preprocessor.postprocess(solution)
    #                 results.append({
    #                     "instance": graph_class+str(instance_count),
    #                     "solver": f"{solver_name} Preprocessed",
    #                     "metric": postprocessed_sol.colors
    #                 })
    #             except Exception as e:
    #                 print(f"Error while solving with {solver_name}: {e}")
    #     instance_count += 1
    
    # instance_count = 1
    # for graph in graphs1:
    #     # graph, chromatic = load_instance(instance)
        
    #     heuristic_count = 1        
    #     for heuristic_name in all_heuristics:
            
    #         print("--------------------------",instance_count, "--" ,heuristic_count, "--", heuristic_name,"-----------------------")
    #         heuristic_count += 1
    #         Heuristic = globals()[heuristic_name]
            
            
            
            
    #         heuristic = Heuristic(graph)
            
            
    #         try:
    #             solution = heuristic.solve()
    #             results.append({
    #                 "instance": graph_class+str(instance_count),
    #                 "solver": f"{heuristic_name}",
    #                 "metric": solution
    #             })
    #         except Exception as e:
    #             print(f"Error while solving with {heuristic_name}: {e}")
    #     instance_count += 1
    
    
    df = pd.DataFrame(results)
    df.to_csv("./evaluations/results_best_lower_bound_kneser.csv", index=False)
    
    print("GRAPH GEN STARTED")
    graphs2 = [nx.barabasi_albert_graph(150, 50, i) for i in range(10)]
    
    print("GRAPH GEN FINISHED")
    
    
    results = []
    instance_count = 1
    graph_class = "barabasi_albert_"
    for i, graph in enumerate(graphs2):
    # for instance in instances:
        # graph, chromatic = load_instance(instance)
        dsatur_solver = DSATUR(graph.copy())
        upper_dsatur = dsatur_solver.solve()
        print("--------------------------",instance_count,"-----------------------")
        
        solver_count = 1
        for solver_name in all_solvers:
            if solver_name not in ["GCSolver", "PYSATDecisionVariant", "REPILPSolverCPSat", "REPILPSolverGurobi"]:
                print("--------------------------",instance_count, "--" ,solver_count, "--", solver_name,"-----------------------")
                solver_count += 1
                Solver = globals()[solver_name]
                
                solver_name = Solver.__name__
                
                solver = Solver(graph.copy(), upper_dsatur)
                
                
                try:
                    solution: Solution = solver.solve(timelimit=20)
                    if solution.status == ModelStatus.FEASIBLE and solution.lower_bound is not None:
                        results.append({
                            "instance": graph_class+str(instance_count),
                            "solver": solver_name,
                            "metric": solution.lower_bound
                        })
                        df = pd.DataFrame(results)
                        df.to_csv("./evaluations/results_best_lower_barabasi_albert.csv", index=False)
                    elif solution.status == ModelStatus.OPTIMAL:
                        results.append({
                            "instance": graph_class+str(instance_count),
                            "solver": solver_name,
                            "metric": solution.colors
                        })
                        df = pd.DataFrame(results)
                        df.to_csv("./evaluations/results_best_lower_bound_barabasi_albert.csv", index=False)
                except Exception as e:
                    print(f"Error while solving with {solver_name}: {e}")
        
        instance_count += 1
        
    # instance_count = 1
    # for graph in graphs2:
    #     # graph, chromatic = load_instance(instance)
        
        
    #     dsatur_solver = DSATUR(graph.copy())
    #     upper_dsatur = dsatur_solver.solve()
    #     print("--------------------------",instance_count,"-----------------------")
        
    #     solver_count = 1
    #     for solver_name in all_solvers:
    #         if solver_name not in ["GCSolver", "PYSATDecisionVariant", "REPILPSolverCPSat", "REPILPSolverGurobi"]:
    #             print("--------------------------",instance_count, "--" ,solver_count, "--", solver_name,"-----------------------")
    #             solver_count += 1
    #             Solver = globals()[solver_name]
                
                
                
    #             preprocessor = DegreeBasedPreprocessor(graph)
    #             reduced_graph = preprocessor.preprocess()
                
    #             solver = Solver(reduced_graph, upper_dsatur)
                
                
    #             try:
    #                 solution = solver.solve(timelimit=60)
    #                 postprocessed_sol = preprocessor.postprocess(solution)
    #                 results.append({
    #                     "instance": graph_class+str(instance_count),
    #                     "solver": f"{solver_name} Preprocessed",
    #                     "metric": postprocessed_sol.colors
    #                 })
    #             except Exception as e:
    #                 print(f"Error while solving with {solver_name}: {e}")
    #     instance_count += 1
    
    # instance_count = 1
    # for graph in graphs2:
    #     # graph, chromatic = load_instance(instance)
        
    #     heuristic_count = 1        
    #     for heuristic_name in all_heuristics:
            
    #         print("--------------------------",instance_count, "--" ,heuristic_count, "--", heuristic_name,"-----------------------")
    #         heuristic_count += 1
    #         Heuristic = globals()[heuristic_name]
            
            
            
            
    #         heuristic = Heuristic(graph)
            
            
    #         try:
    #             solution = heuristic.solve()
    #             results.append({
    #                 "instance": graph_class+str(instance_count),
    #                 "solver": f"{heuristic_name}",
    #                 "metric": solution
    #             })
    #         except Exception as e:
    #             print(f"Error while solving with {heuristic_name}: {e}")
    #     instance_count += 1
    
    
    df = pd.DataFrame(results)
    df.to_csv("./evaluations/results_best_lower_barabasi_albert.csv", index=False)