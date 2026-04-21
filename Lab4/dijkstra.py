import heapq
import time
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from graph_gen import gen_sparse_adj, gen_dense_adj

INF = float('inf')
os.makedirs('figures', exist_ok=True)


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


SIZES = [50, 100, 200, 400, 600, 800, 1000, 1500, 2000, 2500, 3000]

sparse_times = []
dense_times = []

print("=== Dijkstra Measurement Results ===")
print("=" * 44)

for n in SIZES:
    g = gen_sparse_adj(n)
    t0 = time.perf_counter()
    dijkstra(g, 0, n)
    ts = time.perf_counter() - t0
    sparse_times.append(ts)

    g = gen_dense_adj(n)
    t0 = time.perf_counter()
    dijkstra(g, 0, n)
    td = time.perf_counter() - t0
    dense_times.append(td)

    print(f"Size: {n:5d} | Sparse: {ts:.6f} s | Dense: {td:.6f} s")


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


make_plot(SIZES, sparse_times, 'purple',
          "Dijkstra's Algorithm - Sparse Graph",
          'figures/dijkstra_sparse.png')

make_plot(SIZES, dense_times, 'royalblue',
          "Dijkstra's Algorithm - Dense Graph",
          'figures/dijkstra_dense.png')