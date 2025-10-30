from data_schema import Instance, Solution
from ortools.sat.python import cp_model


def solve(instance: Instance) -> Solution:
    """
    Implement your solver for the problem here!
    """
    
    # accidentally solved this task before pure python ,:)
    
    numbers = instance.numbers
    model = cp_model.CpModel()
    
    dom = cp_model.Domain.from_values(numbers)
    
    x = model.new_int_var_from_domain(dom,"x")
    y = model.new_int_var_from_domain(dom, "y")
    
    model.maximize(x-y)
    
    
    solver = cp_model.CpSolver()
    status_code = solver.solve(model)
    # status_name = solver.status_name()
    
    
    return Solution(
        number_a=solver.value(x),
        number_b=solver.value(y),
        distance=abs(solver.value(x) - solver.value(y)),
    )

if __name__ == "__main__":
    
    example_instance = Instance(numbers=[1,2,3,20,4,5])

    
    print(solve(example_instance))
    