class UnionFind:
    def __init__(self, n):
        self.arr = [i for i in range(n)]
        self.size = [1 for _ in range(n)]
        self.biggest = self.arr.copy()
        self.components = n
    
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
    

def test():
    a = UnionFind(10)
    assert a.components == 10
    assert not a.connected(0,9)
    assert a.find(1) == 1
    a.union(1,2)
    assert a.find(1) == 2
    a.union(2,3)
    assert a.find(1) == 3
    assert a.components == 8
    assert a.connected(1,2)
    assert a.connected(1,3)
    assert not a.connected(0,9)
    a.union(3,9)
    assert a.find(4) == 4
    assert a.find(9) == 9
    assert a.components == 7
    assert a.connected(1,9)
    a.union(0,4)
    assert a.find(0) == 4
    assert a.components == 6
    a.union(1,9)
    assert a.find(1) == 9
    assert a.components == 6
    a.union(5,4)
    a.union(0,1)
    assert a.connected(0,9)
    assert a.components == 4
    print("Correct")

test()