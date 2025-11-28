
from tests._alglab_utils import main, mandatory_testcase
from tests.tests import solve_instance_and_compare_bound_and_check_coloring
from graph_coloring.solvers import AllDifferentSolver


runtime = 60
@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_5a():
    solve_instance_and_compare_bound_and_check_coloring("le450_5a.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_5b():
    solve_instance_and_compare_bound_and_check_coloring("le450_5b.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_5c():
    solve_instance_and_compare_bound_and_check_coloring("le450_5c.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_5d():
    solve_instance_and_compare_bound_and_check_coloring("le450_5d.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_15b():
    solve_instance_and_compare_bound_and_check_coloring("le450_15b.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_15c():
    solve_instance_and_compare_bound_and_check_coloring("le450_15c.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_15d():
    solve_instance_and_compare_bound_and_check_coloring("le450_15d.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_25a():
    solve_instance_and_compare_bound_and_check_coloring("le450_25a.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_25b():
    solve_instance_and_compare_bound_and_check_coloring("le450_25b.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_25c():
    solve_instance_and_compare_bound_and_check_coloring("le450_25c.col", AllDifferentSolver, runtime)

@mandatory_testcase(max_runtime_s=runtime)
def all_different_le450_25d():
    solve_instance_and_compare_bound_and_check_coloring("le450_25d.col", AllDifferentSolver, runtime)



def run():
    main()