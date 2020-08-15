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
        if self.size[a] <= self.size[b]:
            self.arr[aRoot] = self.arr[bRoot]
        else:
            self.arr[bRoot] = self.arr[aRoot]

    def connected(self, a, b):
        return self.root(a) == self.root(b)

def social_connectivity(filename, n):
    """
    n is the number of people in the social network
    """
    connectivity_graf = UnionFind(n)
    timestamp = 0
    if connectivity_graf.components <= 1:
        return timestamp
    with open(filename) as f:
        for row in f:
            timestamp, friend1, friend2 = row.split(",")
            friend1, friend2 = int(friend1), int(friend2)
            connectivity_graf.union(friend1, friend2)
            if connectivity_graf.components == 1:
                return float(timestamp)
    return float("inf")

def test():
    assert social_connectivity("test_social_network_connectivity_1.txt", 7) == 9
    assert social_connectivity("test_social_network_connectivity_2.txt", 1) == 0
    assert social_connectivity("test_social_network_connectivity_3.txt", 7) == float("inf")
    print("Correct")

if __name__ == "__main__":
    test()