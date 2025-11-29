
from networkx import Graph

from tests._alglab_utils import *


from utils.load_instance import load_instance
from utils.coloring import is_valid_coloring
from utils.data_schema import ModelStatus

from graph_coloring.solvers import GCSolver
from graph_coloring.heuristics import DSATUR

def solve_graph_and_compare_bound_and_check_coloring(
    graph: Graph, lower_bound: int, Solver: GCSolver, runtime: int | float
):
    
    
    dsatur_solver = DSATUR(graph.copy())
    upper_dsatur = dsatur_solver.solve()
    
    solver = Solver(graph, upper_dsatur)
    solution = solver.solve(timelimit=int(runtime*.6))
        
    if solution.status == ModelStatus.OPTIMAL or solution.status == ModelStatus.FEASIBLE:
        CHECK(lower_bound <= solution.colors, "The number of used colors must be greater or equal to the lower bound!")
        CHECK(is_valid_coloring(solution.graph), "The coloring of the graph must be correct!")
    else:
        logging.warning("The solver timed out! Tests were skipped.")


def solve_instance_and_compare_bound_and_check_coloring(
    instance_name: str, Solver: GCSolver, runtime: int | float
):
    graph, chromatic = load_instance(instance_name)
    
    dsatur_solver = DSATUR(graph.copy())
    upper_dsatur = dsatur_solver.solve()
    
    solver = Solver(graph, upper_dsatur)
    solution = solver.solve(timelimit=int(runtime*.6))
    if chromatic != -1:
        if solution.status == ModelStatus.OPTIMAL:
            CHECK(chromatic == solution.colors, "The number of used colors must equal to the chromatic number!")
        else:
            CHECK(chromatic <= solution.colors, "The number of used colors must be greater or equal to the chromatic number!")
        
    if solution.status == ModelStatus.OPTIMAL or solution.status == ModelStatus.FEASIBLE:
        CHECK(is_valid_coloring(solution.graph), "The coloring of the graph must be correct!")
    else:
        logging.warning("The solver timed out! Tests were skipped.")
