
For every node i add a boolean variable $x_i$ to form the Set $X$

For every node i add the clause: 
$\lor_{x\in\{x_k;x_k\in X\land d_{ik}\leq c\}}x$

Add a clause to ensure only k centers are set:
$\sum_{x\in X}x\leq k$