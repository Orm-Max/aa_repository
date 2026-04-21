import time
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from graph_gen import gen_sparse_adj, gen_dense_adj, adj_to_matrix

INF = float('inf')
os.makedirs('figures', exist_ok=True)


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


SIZES = [10, 20, 30, 50, 70, 100, 120, 150, 200, 250, 300]

sparse_times = []
dense_times = []

print("=== Floyd-Warshall Measurement Results ===")
print("=" * 44)

for n in SIZES:
    g = gen_sparse_adj(n)
    m = adj_to_matrix(g, n)
    t0 = time.perf_counter()
    floyd_warshall(m, n)
    ts = time.perf_counter() - t0
    sparse_times.append(ts)

    g = gen_dense_adj(n)
    m = adj_to_matrix(g, n)
    t0 = time.perf_counter()
    floyd_warshall(m, n)
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


make_plot(SIZES, sparse_times, 'green',
          'Floyd-Warshall Algorithm - Sparse Graph',
          'figures/fw_sparse.png')

make_plot(SIZES, dense_times, 'darkorange',
          'Floyd-Warshall Algorithm - Dense Graph',
          'figures/fw_dense.png')