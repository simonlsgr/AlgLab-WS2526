
# Input Parameters
Graph: $G = (V,E)$ with a single elevator node $v_{elevator}$

Mines: $m \in M \subset V $ with $o_m \in \mathbb{R}$ where $o_m$ are the ores produced by mine $m$ in an hour

Tunnels: $e=\{u,v\} \in E$  with throughput $u_e \in \mathbb{N}$ and maintenence cost $c_e \in \mathbb{R}^+$

Budget: $b \in \mathbb{R}$

# Decision Variables
$x_{uv}, x_{vu} \in \mathbb{B}\quad \forall e=\{u,v\} \in E$ where $x_{uv/vu} = 1$ if the direction is maintened and chosen.

$f_{uv},f_{uv} \in \mathbb{R}^+  \quad\forall e=\{u,v\} \in E$ where the value of $f_{uv}$ marks the amount of flow from $u$ to $v$.

# Constraints
$x_{uv} + x_{vu} \leq 1 \quad \forall e=\{u,v\} \in E$ Only one direction can be chosen.

$f_{uv} \leq  x_{uv} \cdot u_{\{u,v\}} \quad \forall e=\{u,v\} \in E$ Flow from $u$ to $v$ can only exist if the tunnel is activated in that direction and maintained. (Analogous in the direction $vu$).

$\sum_{e=\{u,v\}\in E}c_e \cdot (x_{uv} + x_{vu}) \leq b$ The cost to maintain the tunnel system can not overshoot the budget.

$\sum_{e=\{u,w\}\in E}f_{uw} + o_w \geq \sum_{e=\{u,w\}\in E} f_{wu} \quad \forall w\in M$

# Objective

$$max \sum_{\substack{ e=\{u,w\}\in E \\ w=v_{elevator}}}f_{uv_{elevator}}$$