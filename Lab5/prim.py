import heapq

INF = float('inf')


def prim(graph, src, n):
    """
    Prim's MST algorithm using a binary min-heap.
    Returns total MST weight.
    Complexity: O((V + E) log V)
    """
    key    = [INF] * n
    in_mst = [False] * n
    key[src] = 0
    pq = [(0, src)]        # (edge_weight, vertex)
    mst_cost = 0

    while pq:
        cost, u = heapq.heappop(pq)
        if in_mst[u]:      # stale entry – vertex already in MST
            continue
        in_mst[u]  = True
        mst_cost  += cost

        for v, w in graph[u]:
            if not in_mst[v] and w < key[v]:
                key[v] = w
                heapq.heappush(pq, (w, v))

    return mst_cost
