import random

INF = float('inf')

def gen_sparse_adj(n):
    graph = [[] for _ in range(n)]

    # Phase 1: random spanning tree (guarantees connectivity)
    for i in range(1, n):
        u = random.randint(0, i - 1)
        w = random.randint(1, 100)
        graph[u].append((i, w))
        graph[i].append((u, w))

    # Phase 2: n extra random edges
    for _ in range(n):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            w = random.randint(1, 100)
            graph[u].append((v, w))
            graph[v].append((u, w))

    return graph


def gen_dense_adj(n):
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                w = random.randint(1, 100)
                graph[i].append((j, w))
                graph[j].append((i, w))
    return graph


def adj_to_matrix(graph, n):
    matrix = [[INF] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0
    for u in range(n):
        for v, w in graph[u]:
            if w < matrix[u][v]:
                matrix[u][v] = w
    return matrix