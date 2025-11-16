Assuming that we do not branch on variables which are equal in the linear relaxation and in the optimal solution, we can save up to ${2^n}-{2^{i}}$ calculations using a relaxation (where $n = |E|$ and $i$ is the number of variables that are the same in the relaxation and in the final solution). 

This means that we can save an exponential amount of time in the relaxation. 
Additionally, the difference in the relaxations $|i_{k=1} - i_{k=2}|$ can also result in an exponential time save.

In the samples of size 50(?) an example yields a difference in overlap between $k=1$ and $k=2$ of:

42 - 35 = 7

49 - 45 = 4

44 - 38 = 6

41 - 39 = 2

49 - 44 = 5

45 - 41 = 4

45 - 36 = 9

45 - 34 = 11

47 - 36 = 11

45 - 41 = 4

44 - 37 = 7

avg = 7

In this example we could potentially save $2^{50}-2^{7}$ calculations (worst case). 