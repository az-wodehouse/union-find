# union-find
stuff relating to union-find

The main application is run as
python3 percolation.py n trials
where n and trials are ints and n > 0 and trials > 1.

Suppose you have an n x n grid, where all of the n^2
cells are blocked. Opening one cell at a time randomly, what
is, on average, the fraction you have to open to have a connected
path from the top row to the bottom row of open cells? This program
gives an answer to that question by running a Monte Carlo simulation
and uses a union-find algorithm to efficiently solve the problem.

Problem found here:
https://coursera.cs.princeton.edu/algs4/assignments/percolation/specification.php

The number of trials in the monte carlo simulation is the trials argument.
For a large number of trials, after the grid is sufficiently large, the
value should be approximately .59. e.g. python3 percolation.py 50 100 should
give .59 or so.

The time complexity is O(trials * n^2 ((log*) n^2)). Note (log*) is not a typo,
it's iterated log so (log*) n^2 will be very small. The space complexity is
O(n^2).

All files other than percolation3.py are not necessary for the main application.
They are other assignements from the coursera Princeton Algorithms course.
