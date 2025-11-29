
import json
import pathlib
import math

from tests._alglab_utils import CHECK, main, mandatory_testcase
from utils.load_instance import load_instance
from utils.coloring import is_valid_coloring

from graph_coloring.solvers import __all__ as all_solvers
from graph_coloring.solvers import *

from tests.tests import solve_instance_and_compare_bound_and_check_coloring



    

runtime = 120
def make_test(instance, solver, test_name):
    
    def test():
        solve_instance_and_compare_bound_and_check_coloring(instance, solver, runtime)
    
    test.__name__ =  test_name
    return mandatory_testcase(max_runtime_s=runtime)(test)


with open("./tests/test_instances.json", "r") as f:
    
    instances = json.load(f)
    instances = instances["instances"]
    

for solver_name in all_solvers:
    if solver_name not in ["GCSolver", "PYSATDecisionVariant"]:
        solver = globals()[solver_name]
        
        solver_name = solver.__name__
        
        for instance_path in instances:
            instance_name = instance_path.split(".")[0]
            test_name = f"{solver_name}_{instance_name}"
            
            globals()[test_name] = make_test(instance_path, solver, test_name)
    

def run():
    main()