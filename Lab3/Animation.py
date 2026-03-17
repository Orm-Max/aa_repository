import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
import random
import time
from collections import deque

# Configuration
DELAY = 0.6  # seconds between frames (lower = faster)

# ─── Pre-defined graph layouts ────────────────────────────────────────────────

GRAPH_LAYOUTS = {
    "small": {
        "edges": [
            (0,1),(0,2),(1,3),(1,4),(2,5),(2,6),
            (3,7),(4,7),(5,8),(6,8),(7,9),(8,9)
        ],
        "pos": {
            0: (5.0, 8.5),
            1: (3.0, 6.5), 2: (7.0, 6.5),
            3: (1.5, 4.5), 4: (4.5, 4.5),
            5: (5.5, 4.5), 6: (8.5, 4.5),
            7: (3.0, 2.5), 8: (7.0, 2.5),
            9: (5.0, 0.5),
        },
    },
    "medium": {
        "edges": [
            (0,1),(0,2),(0,3),
            (1,4),(1,5),
            (2,5),(2,6),
            (3,6),(3,7),
            (4,8),(5,8),(5,9),
            (6,9),(6,10),
            (7,10),(7,11),
            (8,12),(9,12),(9,13),
            (10,13),(11,13),
        ],
        "pos": {
             0: (6.0, 9.0),
             1: (3.0, 7.0), 2: (6.0, 7.0), 3: (9.0, 7.0),
             4: (1.5, 5.0), 5: (4.5, 5.0), 6: (7.5, 5.0), 7: (10.5, 5.0),
             8: (2.5, 3.0), 9: (5.5, 3.0),10: (8.5, 3.0),11: (11.0, 3.0),
            12: (3.5, 1.0),13: (7.5, 1.0),
        },
    },
    "random": None,  # generated dynamically
}


def generate_random_graph(n=12):
    """Generate a random connected graph with n nodes placed in a circle."""
    pos = {}
    for i in range(n):
        angle = 2 * np.pi * i / n - np.pi / 2
        r = 4.0
        pos[i] = (5.5 + r * np.cos(angle), 5.0 + r * np.sin(angle))

    # Spanning tree
    edges = set()
    shuffled = list(range(1, n))
    random.shuffle(shuffled)
    for i in shuffled:
        j = random.randint(0, i - 1)
        edges.add((min(i, j), max(i, j)))

    # Extra edges
    attempts = n * 2
    for _ in range(attempts):
        u, v = random.sample(range(n), 2)
        edges.add((min(u, v), max(u, v)))

    return {"edges": list(edges), "pos": pos}


# ─── Visualizer ───────────────────────────────────────────────────────────────

class GraphVisualizer:
    NODE_RADIUS = 0.45

    COLOR_DEFAULT  = "#0062ff"   # unvisited
    COLOR_IN_DS    = "#ff8800"   # in queue / stack
    COLOR_CURRENT  = "#ff0000"   # currently processing
    COLOR_VISITED  = "#00ff5e"   # fully visited
    COLOR_EDGE     = "#2a3a4a"
    COLOR_EDGE_ACT = "#ffffff"
    BG             = "#0d1117"
    TEXT_LIGHT     = "#ffffff"
    TEXT_MUTED     = "#94a3b8"

    def __init__(self, graph, algo_name):
        self.edges  = graph["edges"]
        self.pos    = graph["pos"]
        self.n      = len(self.pos)
        self.algo   = algo_name

        # Build adjacency list (sorted neighbours → deterministic traversal)
        self.adj = {i: [] for i in range(self.n)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        for k in self.adj:
            self.adj[k].sort()

        # State tracking
        self.node_colors = [self.COLOR_DEFAULT] * self.n
        self.edge_active = set()
        self.visited_count = 0
        self.ds_contents   = []   # queue or stack snapshot

        plt.style.use("dark_background")
        self.fig, (self.ax_graph, self.ax_ds) = plt.subplots(
            1, 2, figsize=(16, 8),
            gridspec_kw={"width_ratios": [3, 1]}
        )
        self.fig.patch.set_facecolor(self.BG)

        for ax in (self.ax_graph, self.ax_ds):
            ax.set_facecolor(self.BG)
            ax.axis("off")

        # Graph axes limits
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        pad = 1.4
        self.ax_graph.set_xlim(min(xs) - pad, max(xs) + pad)
        self.ax_graph.set_ylim(min(ys) - pad, max(ys) + pad)
        self.ax_graph.set_aspect("equal")

        # Title & stats
        self.title_text = self.fig.text(
            0.38, 0.96, "", ha="center", va="top",
            fontsize=18, fontweight="bold", color=self.TEXT_LIGHT,
        )
        self.stats_text = self.fig.text(
            0.38, 0.90, "", ha="center", va="top",
            fontsize=11, color=self.TEXT_MUTED,
        )

        # Legend
        patches = [
            mpatches.Patch(color=self.COLOR_DEFAULT,  label="Unvisited"),
            mpatches.Patch(color=self.COLOR_IN_DS,    label="In Queue / Stack"),
            mpatches.Patch(color=self.COLOR_CURRENT,  label="Current node"),
            mpatches.Patch(color=self.COLOR_VISITED,  label="Visited"),
        ]
        self.ax_graph.legend(
            handles=patches, loc="lower right",
            facecolor="#161b22", edgecolor="#30363d",
            labelcolor="white", fontsize=9, framealpha=0.9,
        )

        plt.tight_layout(rect=[0, 0, 1, 0.88])
        plt.ion()
        plt.show()

        # Draw initial state
        self._draw()

    # ── Internal drawing helpers ──────────────────────────────────────────────

    def _draw(self, title="", step_msg=""):
        self.ax_graph.cla()
        self.ax_ds.cla()
        for ax in (self.ax_graph, self.ax_ds):
            ax.set_facecolor(self.BG)
            ax.axis("off")

        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        pad = 1.4
        self.ax_graph.set_xlim(min(xs) - pad, max(xs) + pad)
        self.ax_graph.set_ylim(min(ys) - pad, max(ys) + pad)
        self.ax_graph.set_aspect("equal")

        # Edges
        for u, v in self.edges:
            xu, yu = self.pos[u]
            xv, yv = self.pos[v]
            active = (u, v) in self.edge_active or (v, u) in self.edge_active
            self.ax_graph.plot(
                [xu, xv], [yu, yv],
                color=self.COLOR_EDGE_ACT if active else self.COLOR_EDGE,
                linewidth=2.0 if active else 0.8,
                zorder=1,
            )

        # Nodes
        for i in range(self.n):
            x, y = self.pos[i]
            circle = plt.Circle(
                (x, y), self.NODE_RADIUS,
                color=self.node_colors[i],
                zorder=3,
            )
            self.ax_graph.add_patch(circle)
            # Node ID label
            self.ax_graph.text(
                x, y, str(i),
                ha="center", va="center",
                fontsize=11, fontweight="bold",
                color=self.BG, zorder=4,
            )

        # Step message below graph
        self.ax_graph.text(
            np.mean(xs), min(ys) - 0.85, step_msg,
            ha="center", va="top", fontsize=10,
            color=self.TEXT_MUTED, style="italic", zorder=5,
        )

        # Legend (re-add after cla)
        patches = [
            mpatches.Patch(color=self.COLOR_DEFAULT,  label="Unvisited"),
            mpatches.Patch(color=self.COLOR_IN_DS,    label="In Queue / Stack"),
            mpatches.Patch(color=self.COLOR_CURRENT,  label="Current node"),
            mpatches.Patch(color=self.COLOR_VISITED,  label="Visited"),
        ]
        self.ax_graph.legend(
            handles=patches, loc="lower right",
            facecolor="#161b22", edgecolor="#30363d",
            labelcolor="white", fontsize=9, framealpha=0.9,
        )

        # ── Right panel: queue / stack ────────────────────────────────────────
        ds_label = "Queue (FIFO)" if self.algo == "BFS" else "Stack (LIFO)"
        self.ax_ds.text(
            0.5, 0.95, ds_label,
            ha="center", va="top", transform=self.ax_ds.transAxes,
            fontsize=13, fontweight="bold", color=self.TEXT_LIGHT,
        )

        panel_color = "#ff8800" if self.algo == "BFS" else "#cc44ff"
        items = list(self.ds_contents)  # copy; top of stack / front of queue first
        max_show = 14
        items_display = items[:max_show]
        total = len(items)

        box_h = 0.052
        box_w = 0.70
        start_y = 0.88

        # Label: front/top arrow
        if items_display:
            arrow_label = "← front" if self.algo == "BFS" else "← top"
            self.ax_ds.text(
                0.82, start_y - 0.005, arrow_label,
                ha="left", va="center", transform=self.ax_ds.transAxes,
                fontsize=8, color=panel_color,
            )

        for idx, node in enumerate(items_display):
            y_pos = start_y - idx * (box_h + 0.010)
            rect = mpatches.FancyBboxPatch(
                (0.15, y_pos - box_h / 2), box_w, box_h,
                boxstyle="round,pad=0.01",
                linewidth=1.2,
                edgecolor=panel_color,
                facecolor="#161b22",
                transform=self.ax_ds.transAxes,
                zorder=3,
            )
            self.ax_ds.add_patch(rect)
            self.ax_ds.text(
                0.50, y_pos, str(node),
                ha="center", va="center", transform=self.ax_ds.transAxes,
                fontsize=11, fontweight="bold",
                color=panel_color, zorder=4,
            )

        if total > max_show:
            self.ax_ds.text(
                0.50, start_y - max_show * (box_h + 0.010) - 0.01,
                f"… +{total - max_show} more",
                ha="center", va="top", transform=self.ax_ds.transAxes,
                fontsize=9, color=self.TEXT_MUTED,
            )

        if total == 0 and not step_msg.startswith("Done"):
            self.ax_ds.text(
                0.50, 0.50, "empty",
                ha="center", va="center", transform=self.ax_ds.transAxes,
                fontsize=11, color=self.TEXT_MUTED, style="italic",
            )

        # Global title / stats
        self.title_text.set_text(title or f"{self.algo} — Graph Traversal")
        self.stats_text.set_text(
            f"Nodes: {self.n}   |   Visited: {self.visited_count} / {self.n}"
        )

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(DELAY)

    # ── Public update method ──────────────────────────────────────────────────

    def update(self, current=None, in_ds=None, visited=None,
               active_edges=None, title="", step_msg=""):
        in_ds    = set(in_ds    or [])
        visited  = set(visited  or [])
        self.edge_active = set(active_edges or [])

        for i in range(self.n):
            if i == current:
                self.node_colors[i] = self.COLOR_CURRENT
            elif i in visited:
                self.node_colors[i] = self.COLOR_VISITED
            elif i in in_ds:
                self.node_colors[i] = self.COLOR_IN_DS
            else:
                self.node_colors[i] = self.COLOR_DEFAULT

        self.visited_count = len(visited)
        self._draw(title=title, step_msg=step_msg)

    def mark_done(self):
        for i in range(self.n):
            self.node_colors[i] = self.COLOR_VISITED
        self.edge_active = set(self.edges)
        self.ds_contents = []
        self.visited_count = self.n
        self._draw(
            title=f"{self.algo} — Complete!",
            step_msg="All nodes visited.",
        )

    # ── BFS ───────────────────────────────────────────────────────────────────

    def run_bfs(self, start=0):
        visited  = set([start])
        queue    = deque([start])
        vis_list = []
        active_edges = []

        self.ds_contents = list(queue)
        self.update(
            current=start, in_ds=list(queue), visited=vis_list,
            title="BFS — starting",
            step_msg=f"Initialize: enqueue start node {start}",
        )

        while queue:
            node = queue.popleft()
            vis_list.append(node)

            self.ds_contents = list(queue)
            self.update(
                current=node, in_ds=list(queue), visited=vis_list,
                active_edges=active_edges,
                title="BFS — dequeue & visit",
                step_msg=f"Dequeue node {node}  →  mark visited",
            )

            new_in_queue = []
            for nb in self.adj[node]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
                    new_in_queue.append(nb)
                    active_edges.append((node, nb))

            self.ds_contents = list(queue)
            self.update(
                current=node, in_ds=list(queue), visited=vis_list,
                active_edges=active_edges,
                title="BFS — enqueue neighbours",
                step_msg=(
                    f"Enqueued neighbours: {new_in_queue}"
                    if new_in_queue else f"No new neighbours from node {node}"
                ),
            )

        self.mark_done()

    # ── DFS ───────────────────────────────────────────────────────────────────

    def run_dfs(self, start=0):
        visited  = set()
        stack    = [start]
        vis_list = []
        active_edges = []

        self.ds_contents = list(reversed(stack))
        self.update(
            current=None, in_ds=stack, visited=vis_list,
            title="DFS — starting",
            step_msg=f"Initialize: push start node {start}",
        )

        while stack:
            node = stack.pop()
            if node in visited:
                self.ds_contents = list(reversed(stack))
                self.update(
                    current=node, in_ds=stack, visited=vis_list,
                    active_edges=active_edges,
                    title="DFS — skip (already visited)",
                    step_msg=f"Pop node {node}  →  already visited, skip",
                )
                continue

            visited.add(node)
            vis_list.append(node)

            self.ds_contents = list(reversed(stack))
            self.update(
                current=node, in_ds=stack, visited=vis_list,
                active_edges=active_edges,
                title="DFS — pop & visit",
                step_msg=f"Pop node {node}  →  mark visited",
            )

            new_pushed = []
            for nb in reversed(self.adj[node]):   # reversed → leftmost explored first
                if nb not in visited:
                    stack.append(nb)
                    new_pushed.append(nb)
                    active_edges.append((node, nb))

            self.ds_contents = list(reversed(stack))
            self.update(
                current=node, in_ds=stack, visited=vis_list,
                active_edges=active_edges,
                title="DFS — push neighbours",
                step_msg=(
                    f"Pushed neighbours: {list(reversed(new_pushed))}"
                    if new_pushed else f"No new neighbours from node {node}"
                ),
            )

        self.mark_done()


# ─── Menu / Main ──────────────────────────────────────────────────────────────

ALGORITHMS = {
    "1": "BFS",
    "2": "DFS",
}

GRAPHS = {
    "1": ("Small  (10 nodes, tree-like)",  "small"),
    "2": ("Medium (14 nodes, wider tree)", "medium"),
    "3": ("Random (12 nodes)",             "random"),
}


def main():
    print("""
## Graph Traversal Visualizer ##

  Algorithms:
    1 - BFS  (Breadth-First Search)
    2 - DFS  (Depth-First Search)
    0 - Exit
""")

    choice = input("  Enter algorithm choice: ").strip()
    if choice == "0":
        return False
    if choice not in ALGORITHMS:
        print("  Invalid choice."); return True

    algo = ALGORITHMS[choice]

    print("""
  Graph layouts:
    1 - Small  (10 nodes, tree-like)
    2 - Medium (14 nodes, wider tree)
    3 - Random (12 nodes)
""")
    gchoice = input("  Enter graph choice (default 1): ").strip() or "1"
    if gchoice not in GRAPHS:
        gchoice = "1"

    _, gkey = GRAPHS[gchoice]
    if gkey == "random":
        graph = generate_random_graph(12)
    else:
        graph = GRAPH_LAYOUTS[gkey]

    start_input = input(f"  Start node (0–{len(graph['pos'])-1}, default 0): ").strip()
    start = int(start_input) if start_input.isdigit() and int(start_input) < len(graph["pos"]) else 0

    speed_input = input("  Speed 1-5 (1=slow, 5=fast, default 3): ").strip()
    speed = int(speed_input) if speed_input.isdigit() and 1 <= int(speed_input) <= 5 else 3
    global DELAY
    DELAY = [1.2, 0.8, 0.5, 0.25, 0.08][speed - 1]

    print(f"\n  Running {algo} from node {start}…  (close the window when done)\n")

    viz = GraphVisualizer(graph, algo)
    time.sleep(0.4)

    if algo == "BFS":
        viz.run_bfs(start)
    else:
        viz.run_dfs(start)

    print(f"\n  Done!  Visited all {len(graph['pos'])} nodes.")
    print("  Close the plot window to continue.\n")
    plt.ioff()
    plt.show()
    return True


if __name__ == "__main__":
    while True:
        again = main()
        if not again:
            break
        cont = input("\n  Run again? (y/n): ").strip().lower()
        if cont != "y":
            break
    print("\n  Goodbye!")