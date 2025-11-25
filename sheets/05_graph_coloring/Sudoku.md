# Modelling a Sudoku as a Graph Coloring Problem

For each cell in the Sudoku create a node $v \in V$ in the Graph $G$ add an edge $e \in E$ to each node where the corresponding cell is contained in the same row or column as well as in the same 3 by 3 grid.
Now set the Function $c: V \rightarrow \set{1,...,9}$ as follows: $\forall v \in \set{u \in V; \text{u has corresponding cell in the sudoku}}: c(v) = k \quad \text{Where }k\text{ is the value of the correspondung cell of }v\text{ in the sudoku.}$
This partly colored graph can now be solved and used to create a solution for the sudoku.
