#!python3

"""
README

This file is run as
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
"""


from random import shuffle
from statistics import stdev, mean
from sys import argv

class UnionFind:
    def __init__(self, n):
        self.arr = [i for i in range(n)]
        self.size = [1 for _ in range(n)]
        self.components = n

    def root(self, a):
        origin = a
        while self.arr[a] != a:
            a = self.arr[a]
        while self.arr[origin] != a:
            tmp = self.arr[origin]
            self.arr[origin] = a
            origin = tmp
        return a

    def union(self, a, b):
        aRoot = self.root(a)
        bRoot = self.root(b)
        if aRoot == bRoot:
            return
        self.components -= 1
        if self.size[aRoot] <= self.size[bRoot]:
            self.arr[aRoot] = self.arr[bRoot]
            self.size[bRoot] += self.size[aRoot]
        else:
            self.arr[bRoot] = self.arr[aRoot]
            self.size[aRoot] += self.size[bRoot]

    def connected(self, a, b):
        return self.root(a) == self.root(b)

class Percolation:
    def _convert(self, row, col):
        """
        Converts row and col to int in range 0 to n^2-1 inclusive
        Row and Col should be 1-indexed
        2 things are next to one another if theyre in the
        same row not if they're in the same column
        """
        row -= 1
        col -= 1
        return self.n*row + col

    def __init__(self, n):
        """
        creates n-by-n grid, with all sites initially blocked
        """
        if n <= 0:
            raise ValueError
        self.n = n
        self.opensites = 0
        self.startnode = n**2
        self.endnode = n**2 + 1
        self.djs = UnionFind(n**2 + 2)
        self.grid = [[False for _ in range(n)] for _ in range(n)]

    def open(self, row, col):
        """
        opens the site (row, col) if it is not open already
        """
        if row < 1 or col < 1 or row > n or col > n:
            raise ValueError
        rowg = row - 1
        colg = col - 1
        if self.grid[rowg][colg]:
            return
        self.opensites += 1
        self.grid[rowg][colg] = True
        if row == 1:
            self.djs.union(self._convert(row, col), self.startnode)
        if row == self.n:
            self.djs.union(self._convert(row, col), self.endnode)
        if row > 1 and self.grid[rowg-1][colg]:
            self.djs.union(self._convert(row, col), self._convert(row-1, col))
        if row < n and self.grid[rowg+1][colg]:
            self.djs.union(self._convert(row, col), self._convert(row+1, col))
        if col > 1 and self.grid[rowg][colg-1]:
            self.djs.union(self._convert(row, col), self._convert(row, col-1))
        if col < n and self.grid[rowg][colg+1]:
            self.djs.union(self._convert(row, col), self._convert(row, col+1))

    def isOpen(self, row, col):
        """
        is the site (row, col) open?
        """
        if row < 1 or col < 1 or row > n or col > n:
            raise ValueError
        row -= 1
        col -= 1
        return self.grid[row][col]

    def isFull(self, row, col):
        """
        is the site (row, col) full?
        """
        if row < 1 or col < 1 or row > n or col > n:
            raise ValueError
        return self.djs.connected(self._convert(row, col), self.startnode)

    def numberOfOpenSites(self):
        """
        returns the number of open sites
        """
        return self.opensites

    def percolates(self):
        """
        does the system percolate?
        """
        return self.djs.connected(self.startnode, self.endnode)

class PercolationStats:
    def __init__(self, n, trials):
        """
        perform independent trials on an n-by-n grid
        """
        if n <= 0 or trials <= 0:
            raise ValueError
        thresholds = []
        for _ in range(trials):
            opening_order = [(x,y) for x in range(1,n+1) for y in range(1,n+1)]
            shuffle(opening_order)
            ds = Percolation(n)
            while not ds.percolates():
                ds.open(*opening_order.pop())
            thresholds.append(ds.numberOfOpenSites()/n**2)
        self.mean_val = mean(thresholds)
        self.stddev_val = stdev(thresholds)
        plusminus = 1.96*(self.stddev_val)/(trials**.5)
        self.confidenceLo_val = self.mean_val - plusminus
        self.confidenceHi_val = self.mean_val + plusminus

    def mean(self):
        """
        sample mean of percolation threshold
        """
        return self.mean_val

    def stddev(self):
        """
        sample standard deviation of percolation threshold
        """
        return self.stddev_val

    def confidenceLo(self):
        """
        low endpoint of 95% confidence interval
        """
        return self.confidenceLo_val

    def confidenceHi(self):
        """
        high endpoint of 95% confidence interval
        """
        return self.confidenceHi_val

if __name__ == "__main__":
    n = int(argv[1])
    t = int(argv[2])
    ds = PercolationStats(n, t)
    print("mean                    = " + str(ds.mean()))
    print("stddev                  = " + str(ds.stddev()))
    print("95% confidence interval = [" + str(ds.confidenceLo()) + ", " + str(ds.confidenceHi()) + "]")
