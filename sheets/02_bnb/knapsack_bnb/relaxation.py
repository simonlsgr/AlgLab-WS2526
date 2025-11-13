"""
Relaxation Module

In branch-and-bound, a relaxation of the original 0/1 knapsack yields an upper bound
on the best feasible solution within a branch. If this bound does not exceed your
current best feasible solution, you can prune that branch and skip exploring it.

This file provides three example strategies:
  1. VeryNaiveRelaxationSolver:
     - Ignores capacity entirely, sets every unfixed item to 1.
     - Fastest, loosest bound.
  2. NaiveRelaxationSolver:
     - Checks that already-fixed items of 1 fit capacity.
     - Sets all unfixed items to 1, ignoring capacity beyond fixed part.
     - Slightly tighter bound than VeryNaive.
  3. MyRelaxationSolver:
     - Stub for your own algorithm (e.g., fractional knapsack, propagation).

You should subclass `RelaxationSolver` and implement `solve(instance, decisions)`
so that:
  a) fixed decisions remain unchanged;
  b) objective >= best 0/1 solution consistent with those decisions.
"""

import abc
import math

from .branching_decisions import BranchingDecisions
from .instance import Instance
from .relaxed_solution import RelaxedSolution
from .instance import Item


class RelaxationSolver(abc.ABC):
    """
    Abstract base for relaxation strategies.

    Implement `solve` to compute an upper bound on the best 0/1 solution
    consistent with given decisions.
    """

    @abc.abstractmethod
    def solve(
        self, instance: Instance, decisions: BranchingDecisions
    ) -> RelaxedSolution:
        """
        Return a `RelaxedSolution` satisfying:
          - fixed items in `decisions` remain at 0 or 1;
          - upper_bound >= best feasible 0/1 solution under those decisions.
        """
        ...


class VeryNaiveRelaxationSolver(RelaxationSolver):
    """
    A relaxation solver for the knapsack problem that naively sets every unfixed
    item to 1 without considering the capacity constraint. This approach provides
    a very loose upper bound for the problem.

    Explanation:
    The solver assumes that all unfixed items can be fully included in the knapsack
    (i.e., their selection is set to 1.0) regardless of the capacity constraint.
    This results in an overestimation of the objective value, making it an upper
    bound. The rationale is that the true optimal solution cannot exceed this
    value since it must respect the capacity constraint, which this naive approach
    ignores.
    """

    def solve(
        self, instance: Instance, decisions: BranchingDecisions
    ) -> RelaxedSolution:
        # build selection: 1.0 for fixed 1 or unfixed, 0 for fixed 0
        selection = [0.0 if x == 0 else 1.0 for x in decisions]
        # compute objective value
        upper = sum(item.value * sel for item, sel in zip(instance.items, selection))
        return RelaxedSolution(instance, selection, upper)


class NaiveRelaxationSolver(RelaxationSolver):
    """
    Ensure fixed 1's fit capacity; set every unfixed item to 1.
    """

    def solve(
        self, instance: Instance, decisions: BranchingDecisions
    ) -> RelaxedSolution:
        # compute capacity after fixed 1 items
        used = sum(item.weight for item, x in zip(instance.items, decisions) if x == 1)
        if used > instance.capacity:
            return RelaxedSolution.create_infeasible(instance)

        selection = [0.0 if x == 0 else 1.0 for x in decisions]
        upper = sum(item.value * sel for item, sel in zip(instance.items, selection))
        return RelaxedSolution(instance, selection, upper)


class MyRelaxationSolver(RelaxationSolver):
    """
    Your relaxation solver stub.

    Implement any relaxation (e.g., fractional knapsack, propagation) to tighten bounds.
    """

    # run_second_instance(

    def sort_by(self, tup):
        return tup[0]
        
    def solve(
        self, instance: Instance, decisions: BranchingDecisions
    ) -> RelaxedSolution:
        # placeholder: behave like NaiveRelaxationSolver
        
        
        
        
        value_over_weight = [item.weight / item.value for item in instance.items]
        
        used = sum(item.weight for item, x in zip(instance.items, decisions) if x == 1)
        enforced_weight = used
        if used > instance.capacity:
            return RelaxedSolution.create_infeasible(instance)
        round = not any([False if int(i.value) == i.value else True for i in instance.items])
        
        
        # print("------------------sorted")
        # print(list(decisions.__iter__()))
        selection = [0.0 if x == 0 or x is None else 1.0 for x in decisions]
        for i, (relative_value, item) in enumerate(sorted(zip(value_over_weight, instance.items), key=self.sort_by)):
            item_index_in_instance = instance.items.index(item)
            if decisions[item_index_in_instance] is None:
                used += item.weight
                if used > instance.capacity:
                    used -= item.weight
                    # use item only partially if the item would fit into the knapsack if greedy would not have been used
                    enforced_remaining_weight = instance.capacity - enforced_weight
                    for j, (relative_value2, item2) in enumerate(sorted(zip(value_over_weight, instance.items), key=self.sort_by)):
                        if j >= i:
                            if item.weight <= enforced_remaining_weight:
                                if round:
                                    selection[instance.items.index(item2)] = (instance.capacity - used)/item2.weight
                                else:
                                    selection[instance.items.index(item2)] = (instance.capacity - used)/item2.weight
                                break
                    break
                else:
                    selection[item_index_in_instance] = 1.0
        
        # min_item : Item = None
        # if len(["." for x in selection if 0 < x < 1]) == 0:
        #     for item, decision in zip(instance.items, decisions):
        #         if decision is None:
        #             if min_item is None:
        #                 min_item = item
        #             elif min_item.weight > item.weight:
        #                 min_item = item

        # if min_item is not None:
        #     print("-------------")
        #     print(instance.capacity)
        #     print(sum([item.weight*sel for item, sel in zip(instance.items, selection)]))
        #     idx = instance.items.index(min_item)
        #     selection[idx] = (instance.capacity - used)/min_item.weight
        #     print(sum([item.weight*sel for item, sel in zip(instance.items, selection)]))
            
            
            

        # selection = [0.0 if x == 0 else 1.0 for x in decisions]
        
        upper = sum(item.value * sel for item, sel in zip(instance.items, selection))
        
        # if round:
        #     upper = math.floor(upper)
        return RelaxedSolution(instance, selection, upper)

