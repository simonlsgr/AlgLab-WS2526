

# Benchmarks of the solvers and heuristics

## Heuristics
We ran the heuristics on several different instance sets. Here are the results:

### Kneser Graphs
When looking at the following performance profile one could suspect that the Naive Greedy is the best heuristic for this type of graph classes. On second look it is quite curious that the multistart greedy heuristic performs worse than only the naive greedy algorithm. This is caused by the naive greedy algorithm using the order of nodes provided by `networkx`. In future work we should investigate why this results in the best coloring of the used methods.
![Kneser Graph ordered naive](evaluations/results_heuristics/results_kneser_graph_20_heuristics.png)
If the naive greedy algorithm uses random order it performs, as suspected worse results than the multistart greedy.
![Kneser Graph unordered naive](evaluations/results_heuristics/results_kneser_graph_20_random_naive_heuristics.png)

### Cycle Graphs & Wheel Graphs

For cycle graphs DSATUR performs better than both versions of the greedy. This is not suprising, as Dsatur is optimal for cycle graphs.
![Cycle Graph unordered](evaluations/results_heuristics/results_cycle_graph_100_unordered_heuristics.png)

The same goes for wheel graphs.

![Cycle Graph unordered](evaluations/results_heuristics/results_wheel_graph_100_heuristics_unordered.png)

### Erdős-Rényi-Graphs

For Erdős-Rényi-Graphs Dsatur performs better on all instances than both Greedy versions.

![Erdős-Rényi-graphs](evaluations/results_heuristics/results_100_erdos_renyi_heuristics.png)


### Barabási-Albert-Graphs
As seen before Dsatur performs better; in comparison to the performance on Erdős-Rényi-Graphs the performance difference is even greater.
![results_barabasi_albert_100_heuristics-graphs](evaluations/results_heuristics/results_barabasi_albert_100_heuristics.png)