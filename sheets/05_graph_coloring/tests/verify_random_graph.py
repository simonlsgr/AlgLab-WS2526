

import networkx as nx
import random


from tests._alglab_utils import main, mandatory_testcase

from graph_coloring.solvers import __all__ as all_solvers
from graph_coloring.solvers import *

from tests.tests import solve_graph_and_compare_bound_and_check_coloring


runtime = 120
def make_test(graph, lower_bound, solver, test_name):
    
    def test():
        solve_graph_and_compare_bound_and_check_coloring(graph, lower_bound, solver, runtime)
    
    test.__name__ =  test_name
    return mandatory_testcase(max_runtime_s=runtime)(test)


    


seed = random.seed(100)

for solver_name in all_solvers:
    if solver_name not in ["GCSolver", "PYSATDecisionVariant"]:
        solver = globals()[solver_name]
        
        solver_name = solver.__name__
        
        
        instance = nx.erdos_renyi_graph(50, .25)
        lb = nx.approximation.large_clique_size(instance)
        test_name = f"{solver_name}_erdos_renyi"
    
        globals()[test_name] = make_test(instance, lb, solver, test_name)
    

def run():
    main()