

# Relaxtion
Implemented fractional knapsack as an upper bound.

Iterations with fractional: 1124

Iterations with naive: 788

Doesnt really seem right.. probably an error in the implementation. (Found the error, was over writing the decision variable :})

Now fractional is better with 98 iterations. 

Second instance:

    Iterations with fractional: 82

    Iterations with naive: 1716

Third instance:

    Iterations with fractional: 728

    Iterations with naive: over 5000

# Branching Strategy
First idea is to branch the item which was only partially packed by the relaxation

No change on the first instance.

Second instance:
    Iterations with fractional and branching: 46
Third instance:
    Iterations with fractional and branching: 70

# Search Strategy
Search the node with the best fractional value first, i.e. best first search, yields:
Instance 1:
    Iterations with fractional, branching, best first: 50
Instance 2:
    Iterations with fractional, branching, best first: 18
Instance 3:
    Iterations with fractional, branching, best first: 25

# Issues
In the example for the second instance the upper bound on iteration 4 is .3 units lower than the corresponding node in my solution. 
This might be because the solver for the example used another relaxation (not fractional knapsack).