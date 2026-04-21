import time

from graph_generator import gen_sparse_adj, gen_dense_adj, adj_to_edge_list
from prim import prim
from kruskal import kruskal

NODE_SIZES = [50, 100, 200, 400, 600, 800, 1000, 1500, 2000, 2500, 3000]
REPEATS    = 3          # average over this many runs per data point


def benchmark():
    results = {
        "prim_sparse":    [],
        "prim_dense":     [],
        "kruskal_sparse": [],
        "kruskal_dense":  [],
    }

    for n in NODE_SIZES:
        print(f"n = {n} ...", end=" ", flush=True)

        # --- sparse ---
        t_prim_s = t_kruskal_s = 0.0
        for _ in range(REPEATS):
            g = gen_sparse_adj(n)
            e = adj_to_edge_list(g, n)

            t0 = time.perf_counter()
            prim(g, 0, n)
            t_prim_s += time.perf_counter() - t0

            t0 = time.perf_counter()
            kruskal(e, n)
            t_kruskal_s += time.perf_counter() - t0

        results["prim_sparse"].append(t_prim_s / REPEATS)
        results["kruskal_sparse"].append(t_kruskal_s / REPEATS)

        # --- dense ---
        t_prim_d = t_kruskal_d = 0.0
        for _ in range(REPEATS):
            g = gen_dense_adj(n)
            e = adj_to_edge_list(g, n)

            t0 = time.perf_counter()
            prim(g, 0, n)
            t_prim_d += time.perf_counter() - t0

            t0 = time.perf_counter()
            kruskal(e, n)
            t_kruskal_d += time.perf_counter() - t0

        results["prim_dense"].append(t_prim_d / REPEATS)
        results["kruskal_dense"].append(t_kruskal_d / REPEATS)

        print("done")

    return results


def print_table(results):
    header = (f"{'n':>6}  {'Prim Sparse':>14}  {'Prim Dense':>14}  "
              f"{'Kruskal Sparse':>16}  {'Kruskal Dense':>14}")
    sep = "-" * len(header)
    print(f"\n{sep}\n{header}\n{sep}")
    for i, n in enumerate(NODE_SIZES):
        ps = results["prim_sparse"][i]
        pd = results["prim_dense"][i]
        ks = results["kruskal_sparse"][i]
        kd = results["kruskal_dense"][i]
        print(f"{n:>6}  {ps:>14.6f}  {pd:>14.6f}  {ks:>16.6f}  {kd:>14.6f}")
    print(sep)


if __name__ == "__main__":
    print("Running benchmarks...\n")
    results = benchmark()
    print_table(results)
    print("\nDone. Copy the times into the LaTeX report tables.")
