import math
from typing import List

from data_schema import Instance, Item, Solution
from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver


class MultiKnapsackSolver:
    """
    This class can be used to solve the Multi-Knapsack problem
    (also the standard knapsack problem, if only one capacity is used).

    Attributes:
    - instance (Instance): The multi-knapsack instance
        - items (List[Item]): a list of Item objects representing the items to be packed.
        - capacities (List[int]): a list of integers representing the capacities of the knapsacks.
    - model (CpModel): a CpModel object representing the constraint programming model.
    - solver (CpSolver): a CpSolver object representing the constraint programming solver.
    """

    def __init__(self, instance: Instance, activate_toxic: bool = False):
        """
        Initialize the solver with the given Multi-Knapsack instance.

        Args:
        - instance (Instance): an Instance object representing the Multi-Knapsack instance.
        """
        self.items = instance.items
        self.activate_toxic = activate_toxic
        self.capacities = instance.capacities
        self.model = CpModel()
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
        
        self.xij = []
        for index, capacity in enumerate(self.capacities):
            l = []
            for index2, item in enumerate(self.items):
                l.append(self.model.new_bool_var(f"x{index}{index2}"))
            self.xij.append(l)
        
        for index, item in enumerate(self.items):
            self.model.add_at_most_one(var[index] for var in self.xij)
        
        for index, capacity in enumerate(instance.capacities):
            self.model.add(sum(packed*item.weight for packed, item in zip(self.xij[index],self.items)) <= capacity)
            
            
        if activate_toxic:
            carrying_toxic_goods = []
            for index, _ in enumerate(self.xij):
                carrying_toxic_goods.append(self.model.new_bool_var(f"carrying_toxic_goods{index}"))
            
            # self.model.add_implication(xij, xij.toxic == carrying_toxic_goods)
            
            for index, truck_xi in enumerate(self.xij):
                for index2, packed in enumerate(truck_xi):
                    if self.items[index2].toxic:
                        self.model.add_implication(self.xij[index][index2], carrying_toxic_goods[index])
                    else:
                        self.model.add_implication(self.xij[index][index2], ~carrying_toxic_goods[index])
                        
        
        max = []
        for xj in self.xij:
            for index, xi in enumerate(xj):
                max.append(xi*self.items[index].value)
        self.model.maximize(sum(max))
        
        
        
        



    def solve(self, timelimit: float = math.inf) -> Solution:
        """
        Solve the Multi-Knapsack instance with the givenTraceback (most recent call last):

        Args:
        - timelimit (float): time limit in seconds for the cp-sat solver.

        Returns:
        - Solution: a list of lists of Item objects representing the items packed in each knapsack
        """
        
        
        # handle given time limit
        if timelimit <= 0.0:
            return Solution(trucks=[])  # empty solution
        if timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        # TODO: Implement me!
        
        
        self.solver.parameters.log_to_stdout = True
        status = self.solver.solve(self.model)
        
        truck_list = []
        if status in (OPTIMAL, FEASIBLE):
            print("Successfully found a solution")
            for i in range(len(self.capacities)):
                truck_i = []
                for item_index, packed in enumerate(self.xij[i]):
                    if self.solver.value(packed):
                        truck_i.append(self.items[item_index])
                truck_list.append(truck_i)
        
        return Solution(trucks=truck_list)  # empty solution

if __name__ == '__main__':
    import json
    with open("instances/20i_5k.json", 'r') as f:
        instance_json = f.read()
    instance = Instance.model_validate_json(instance_json)
    
    solver = MultiKnapsackSolver(instance, activate_toxic=True)
    solution = solver.solve()
    
    print(solution)
    
