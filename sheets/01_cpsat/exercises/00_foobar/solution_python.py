from data_schema import Instance, Solution


def solve(instance: Instance) -> Solution:
    """
    Implement your solver for the problem here!
    """
    numbers = instance.numbers
    
    x = min(numbers)
    y = max(numbers)
    
    return Solution(
        number_a=x,
        number_b=y,
        distance=abs(x-y),
    )
