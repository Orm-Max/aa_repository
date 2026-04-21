def kruskal(edges, n):
    """
    Kruskal's MST algorithm with Union-Find (path compression + union by rank).
    `edges` is a list of (w, u, v) tuples – sorting happens inside.
    Returns total MST weight.
    Complexity: O(E log E)
    """
    edges = sorted(edges)          # sort by weight

    parent = list(range(n))
    rank   = [0] * n

    def find(x):
        # Path halving (iterative)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False           # same component → would form cycle
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    mst_cost   = 0
    edge_count = 0
    for w, u, v in edges:
        if union(u, v):
            mst_cost   += w
            edge_count += 1
            if edge_count == n - 1:   # MST complete: exactly n-1 edges
                break

    return mst_cost
