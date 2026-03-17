import time
import random
import sys
from collections import deque
import matplotlib.pyplot as plt

sys.setrecursionlimit(100000)


def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return order


def generate_graph(num_nodes, edge_multiplier=3):
    adj = {i: [] for i in range(num_nodes)}

    # Spanning tree to ensure full connectivity
    for i in range(1, num_nodes):
        j = random.randint(0, i - 1)
        adj[i].append(j)
        adj[j].append(i)

    # Extra random edges
    extra = num_nodes * edge_multiplier - (num_nodes - 1)
    for _ in range(max(0, extra)):
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v:
            adj[u].append(v)
            adj[v].append(u)

    return adj


def measure_bfs(size_values):
    results = []

    for size in size_values:
        graph = generate_graph(size)

        start_time = time.time()
        bfs(graph, 0)
        end_time = time.time()

        execution_time_s = end_time - start_time

        results.append({
            'size': size,
            'time_s': execution_time_s
        })

        print(f"Nodes: {size:>7} | Time: {execution_time_s:.6f} s")

    return results


def plot_results(results):
    sizes = [r['size'] for r in results]
    times_s = [r['time_s'] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_s, 'o-', color='steelblue', linewidth=2, markersize=8)
    plt.xlabel('Number of Nodes (n)', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.title('BFS Performance (Breadth-First Search)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    size_values = [
        100, 500, 1000, 2500, 5000, 7500,
        10000, 25000, 50000, 75000, 100000,
        250000, 500000, 750000, 1000000
    ]

    print("BFS Measurement Results:")
    print("=" * 45)

    results = measure_bfs(size_values)
    plot_results(results)