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
    

def test():
    a = UnionFind(10)
    assert a.components == 10
    assert not a.connected(0,9)
    a.union(1,2)
    a.union(2,3)
    assert a.components == 8
    assert a.connected(1,2)
    assert a.connected(1,3)
    assert not a.connected(0,9)
    a.union(3,9)
    assert a.components == 7
    assert a.connected(1,9)
    a.union(0,4)
    assert a.components == 6
    a.union(1,9)
    assert a.components == 6
    a.union(5,4)
    a.union(0,1)
    assert a.connected(0,9)
    assert a.components == 4
    print("Correct")

if __name__ == "__main__":
    test()