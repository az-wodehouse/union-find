class UnionFind:
    def __init__(self, n):
        self.arr = [i for i in range(n+1)]
        self.size = [1 for _ in range(n+1)]
        self.biggest = self.arr.copy()
        self.components = n + 1
    
    def find(self, n):
        """
        finds biggest element in connected components
        """
        return self.biggest[self.root(n)]

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
            self.arr[aRoot] = bRoot
            self.size[bRoot] += self.size[aRoot]
            self.biggest[bRoot] = max(self.biggest[aRoot], self.biggest[bRoot])
        else:
            self.arr[bRoot] = aRoot
            self.size[aRoot] += self.size[bRoot]
            self.biggest[aRoot] = max(self.biggest[aRoot], self.biggest[bRoot])

    def connected(self, a, b):
        return self.root(a) == self.root(b)
    
    def remove(self, x):
        self.union(x, x+1)
    
    def successor(self, x):
        succ = self.find(x)
        if succ == len(self.arr) - 1:
            return -1
        else:
            return succ

def test():
    a = UnionFind(10)
    assert a.components == 11
    a.remove(1)
    assert a.successor(1) == 2
    a.remove(2)
    assert a.successor(1) == 3
    assert a.successor(2) == 3
    a.remove(9)
    assert a.successor(9) == -1
    assert a.successor(0) == 0
    print("Correct")

test()