import heapq
import time
import random
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.makedirs('figures', exist_ok=True)
INF = float('inf')


# ---------- Graph generators ----------

def gen_sparse_adj(n):
    graph = [[] for _ in range(n)]
    for i in range(1, n):
        u = random.randint(0, i - 1)
        w = random.randint(1, 100)
        graph[u].append((i, w))
        graph[i].append((u, w))
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


# ---------- Algorithms ----------

def dijkstra(graph, src, n):
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist


def floyd_warshall(matrix, n):
    dist = [row[:] for row in matrix]
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                through_k = dist[i][k] + dist[k][j]
                if through_k < dist[i][j]:
                    dist[i][j] = through_k
    return dist


# ---------- Plotting ----------

def make_plot(sizes, times, color, title, filename):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sizes, times, 'o-', color=color, linewidth=1.5, markersize=5)
    ax.set_xlabel('Number of nodes (n)')
    ax.set_ylabel('Time (s)')
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Saved: {filename}")


# ---------- Dijkstra benchmark ----------

DIJK_SIZES = [50, 100, 200, 400, 600, 800, 1000, 1500, 2000, 2500, 3000]
dijk_sparse, dijk_dense = [], []

print("\n=== Dijkstra Measurement Results ===")
print("=" * 52)
for n in DIJK_SIZES:
    g = gen_sparse_adj(n)
    t0 = time.perf_counter()
    dijkstra(g, 0, n)
    ts = time.perf_counter() - t0
    dijk_sparse.append(ts)

    g = gen_dense_adj(n)
    t0 = time.perf_counter()
    dijkstra(g, 0, n)
    td = time.perf_counter() - t0
    dijk_dense.append(td)

    print(f"Size: {n:5d} | Sparse: {ts:.6f} s | Dense: {td:.6f} s")

make_plot(DIJK_SIZES, dijk_sparse, 'purple',
          "Dijkstra's Algorithm - Sparse Graph",
          'figures/dijkstra_sparse.png')
make_plot(DIJK_SIZES, dijk_dense, 'royalblue',
          "Dijkstra's Algorithm - Dense Graph",
          'figures/dijkstra_dense.png')


# ---------- Floyd-Warshall benchmark ----------

FW_SIZES = [10, 20, 30, 50, 70, 100, 120, 150, 200, 250, 300]
fw_sparse, fw_dense = [], []

print("\n=== Floyd-Warshall Measurement Results ===")
print("=" * 52)
for n in FW_SIZES:
    g = gen_sparse_adj(n)
    m = adj_to_matrix(g, n)
    t0 = time.perf_counter()
    floyd_warshall(m, n)
    ts = time.perf_counter() - t0
    fw_sparse.append(ts)

    g = gen_dense_adj(n)
    m = adj_to_matrix(g, n)
    t0 = time.perf_counter()
    floyd_warshall(m, n)
    td = time.perf_counter() - t0
    fw_dense.append(td)

    print(f"Size: {n:5d} | Sparse: {ts:.6f} s | Dense: {td:.6f} s")

make_plot(FW_SIZES, fw_sparse, 'green',
          'Floyd-Warshall Algorithm - Sparse Graph',
          'figures/fw_sparse.png')
make_plot(FW_SIZES, fw_dense, 'darkorange',
          'Floyd-Warshall Algorithm - Dense Graph',
          'figures/fw_dense.png')

print("\nAll done. Figures saved in figures/")