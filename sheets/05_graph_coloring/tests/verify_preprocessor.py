
import networkx as nx


from tests._alglab_utils import *


from utils.coloring import is_valid_coloring
from utils.data_schema import ModelStatus

from graph_coloring.solvers import AllDifferentSolver
from graph_coloring.preprocessing import DegreeBasedPreprocessor



@mandatory_testcase(max_runtime_s=60)
def preprocessing():
    
    graph = nx.erdos_renyi_graph(50, .25)
    lower_bound = nx.approximation.large_clique_size(graph)
    
    preprocessor = DegreeBasedPreprocessor(graph)
    reduced_graph = preprocessor.preprocess()
    
    # it is assumed, that the solver yields correct results
    arbitrary_solver = AllDifferentSolver(reduced_graph)
    solution = arbitrary_solver.solve()
    
    post_processed_sol = preprocessor.postprocess(solution)
    CHECK(nx.is_isomorphic(solution.graph, graph), "The postprocessed graph must be isomorphic to the original graph!")
    if post_processed_sol.status == ModelStatus.OPTIMAL or post_processed_sol.status == ModelStatus.FEASIBLE:
        CHECK(lower_bound <= post_processed_sol.colors, "The number of used colors must be greater or equal to the lower bound!")
        CHECK(is_valid_coloring(post_processed_sol.graph), "The coloring of the graph must be correct!")
    else:
        logging.warning("The solver timed out! Tests were skipped.")

def run():
    main()