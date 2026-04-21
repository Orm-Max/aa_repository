import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── run benchmark first to get results, or paste your own numbers here
from benchmark import benchmark, NODE_SIZES

STYLE = {
    "figure.figsize":    (8, 4.5),
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
    "font.size":         11,
}


def _save(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved → {path}")


def plot_single(nodes, times, title, color, path):
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots()
        ax.plot(nodes, times, marker="o", linewidth=2, color=color, label=title)
        ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
        ax.set_xlabel("Number of nodes (n)")
        ax.set_ylabel("Execution time (s)")
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.legend()
        _save(fig, path)


def plot_comparison(nodes, t1, t2, label1, label2, title, path):
    with plt.rc_context(STYLE):
        fig, ax = plt.subplots()
        ax.plot(nodes, t1, marker="o", linewidth=2, color="#2563EB", label=label1)
        ax.plot(nodes, t2, marker="s", linewidth=2, color="#DC2626", label=label2)
        ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
        ax.set_xlabel("Number of nodes (n)")
        ax.set_ylabel("Execution time (s)")
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.legend()
        _save(fig, path)


def make_all_plots(results):
    n = NODE_SIZES
    print("Generating plots...")

    plot_single(n, results["prim_sparse"],
                "Prim's Algorithm Performance — Sparse Graph",
                "#2563EB", "figures/prim_sparse.png")

    plot_single(n, results["prim_dense"],
                "Prim's Algorithm Performance — Dense Graph",
                "#7C3AED", "figures/prim_dense.png")

    plot_single(n, results["kruskal_sparse"],
                "Kruskal's Algorithm Performance — Sparse Graph",
                "#059669", "figures/kruskal_sparse.png")

    plot_single(n, results["kruskal_dense"],
                "Kruskal's Algorithm Performance — Dense Graph",
                "#DC2626", "figures/kruskal_dense.png")

    plot_comparison(n,
                    results["prim_sparse"], results["kruskal_sparse"],
                    "Prim (sparse)", "Kruskal (sparse)",
                    "Prim vs Kruskal — Sparse Graph",
                    "figures/comparison_sparse.png")

    plot_comparison(n,
                    results["prim_dense"], results["kruskal_dense"],
                    "Prim (dense)", "Kruskal (dense)",
                    "Prim vs Kruskal — Dense Graph",
                    "figures/comparison_dense.png")

    print("All plots saved in ./figures/")


if __name__ == "__main__":
    print("Running benchmarks for plotting...\n")
    results = benchmark()
    make_all_plots(results)
