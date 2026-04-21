import random

random.seed(42)


def gen_sparse_adj(n):
    """
    Sparse graph as adjacency list.
    Phase 1: random spanning tree (guarantees connectivity).
    Phase 2: n additional random edges.
    Result: ~2n edges total.
    """
    graph = [[] for _ in range(n)]

    # Phase 1 – random spanning tree
    for i in range(1, n):
        u = random.randint(0, i - 1)
        w = random.randint(1, 100)
        graph[u].append((i, w))
        graph[i].append((u, w))

    # Phase 2 – n extra random edges
    for _ in range(n):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            w = random.randint(1, 100)
            graph[u].append((v, w))
            graph[v].append((u, w))

    return graph


def gen_dense_adj(n, prob=0.9):
    """
    Dense graph as adjacency list.
    Each undirected edge (i, j) is included independently
    with probability `prob`. Results in ~prob*n*(n-1)/2 edges.
    """
    graph = [[] for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < prob:
                w = random.randint(1, 100)
                graph[u].append((v, w))
                graph[v].append((u, w))
    return graph


def adj_to_edge_list(graph, n):
    """
    Convert adjacency list to edge list [(w, u, v), ...]
    for use with Kruskal's algorithm.
    """
    edges = []
    for u in range(n):
        for v, w in graph[u]:
            if u < v:          # avoid duplicates
                edges.append((w, u, v))
    return edges
