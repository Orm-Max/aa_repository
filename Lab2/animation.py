import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
import time

# Configuration
DELAY = 0.04  # seconds between frames (lower = faster)

# Visualizer class

class SortingVisualizer:
    def __init__(self, arr):
        self.arr = arr[:]
        self.comparisons = 0
        self.swaps = 0

        plt.style.use("dark_background")
        self.fig, self.ax = plt.subplots(figsize=(14, 7))
        self.fig.patch.set_facecolor("#0d1117")
        self.ax.set_facecolor("#0d1117")

        self.bars = self.ax.bar(
            range(len(self.arr)),
            self.arr,
            color="#3b82f6",
            edgecolor="#1e3a5f",
            linewidth=0.5,
        )

        self.ax.set_xlim(-0.5, len(self.arr) - 0.5)
        self.ax.set_ylim(0, max(self.arr) * 1.15)
        self.ax.axis("off")

        # Title & stats text
        self.title_text = self.fig.text(
            0.5, 0.96, "", ha="center", va="top",
            fontsize=18, fontweight="bold", color="white"
        )
        self.stats_text = self.fig.text(
            0.5, 0.90, "", ha="center", va="top",
            fontsize=11, color="#94a3b8"
        )

        # Legend
        blue_patch  = mpatches.Patch(color="#0062ff", label="Unsorted")
        red_patch   = mpatches.Patch(color="#ff0000", label="Comparing / Pivot")
        green_patch = mpatches.Patch(color="#00ff5e", label="Sorted / Placed")
        self.ax.legend(
            handles=[blue_patch, red_patch, green_patch],
            loc="upper right", facecolor="#161b22", edgecolor="#30363d",
            labelcolor="white", fontsize=9, framealpha=0.9,
        )

        plt.tight_layout(rect=[0, 0, 1, 0.88])
        plt.ion()
        plt.show()

    def update(self, highlight_red=[], highlight_green=[], title=""):
        for i, bar in enumerate(self.bars):
            bar.set_height(self.arr[i])
            if i in highlight_red:
                bar.set_color("#ff0000")
            elif i in highlight_green:
                bar.set_color("#00ff5e")
            else:
                bar.set_color("#0062ff")

        self.title_text.set_text(title)
        self.stats_text.set_text(
            f"Comparisons: {self.comparisons}   |   Swaps: {self.swaps}"
        )
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(DELAY)

    def mark_sorted(self, title="Sorted!"):
        for i, bar in enumerate(self.bars):
            bar.set_height(self.arr[i])
            bar.set_color("#22c55e")
        self.title_text.set_text(title)
        self.stats_text.set_text(
            f"Comparisons: {self.comparisons}   |   Swaps: {self.swaps}"
        )
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    # Algorithms

    def selection_sort(self):
        n = len(self.arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                self.comparisons += 1
                self.update([j, min_idx], list(range(i)), "Selection Sort")
                if self.arr[j] < self.arr[min_idx]:
                    min_idx = j
            self.arr[i], self.arr[min_idx] = self.arr[min_idx], self.arr[i]
            self.swaps += 1
            self.update([i, min_idx], list(range(i + 1)), "Selection Sort")
        self.mark_sorted()

    def merge_sort(self):
        self.merge_sort_helper(0, len(self.arr) - 1)
        self.mark_sorted()

    def merge_sort_helper(self, left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        self.merge_sort_helper(left, mid)
        self.merge_sort_helper(mid + 1, right)
        self.merge(left, mid, right)

    def merge(self, left, mid, right):
        left_part  = self.arr[left:mid + 1]
        right_part = self.arr[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            self.comparisons += 1
            if left_part[i] <= right_part[j]:
                self.arr[k] = left_part[i]; i += 1
            else:
                self.arr[k] = right_part[j]; j += 1
            self.swaps += 1
            self.update(
                [k],
                list(range(left, k)),
                "Merge Sort"
            )
            k += 1
        while i < len(left_part):
            self.arr[k] = left_part[i]; i += 1; k += 1; self.swaps += 1
        while j < len(right_part):
            self.arr[k] = right_part[j]; j += 1; k += 1; self.swaps += 1
        self.update([], list(range(left, right + 1)), "Merge Sort")

    def quick_sort(self):
        self.quick_sort_helper(0, len(self.arr) - 1)
        self.mark_sorted()

    def quick_sort_helper(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort_helper(low, pi - 1)
            self.quick_sort_helper(pi + 1, high)

    def partition(self, low, high):
        pivot = self.arr[high]
        i = low - 1
        for j in range(low, high):
            self.comparisons += 1
            self.update([j, high], [], "Quick Sort")
            if self.arr[j] <= pivot:
                i += 1
                self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
                self.swaps += 1
        self.arr[i + 1], self.arr[high] = self.arr[high], self.arr[i + 1]
        self.swaps += 1
        self.update([i + 1], [], "Quick Sort")
        return i + 1

    def heap_sort(self):
        n = len(self.arr)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i)
        for i in range(n - 1, 0, -1):
            self.arr[0], self.arr[i] = self.arr[i], self.arr[0]
            self.swaps += 1
            self.update([0, i], list(range(i, n)), "Heap Sort")
            self.heapify(i, 0)
        self.mark_sorted()

    def heapify(self, n, i):
        largest = i
        l, r = 2 * i + 1, 2 * i + 2
        if l < n and self.arr[l] > self.arr[largest]:
            self.comparisons += 1; largest = l
        if r < n and self.arr[r] > self.arr[largest]:
            self.comparisons += 1; largest = r
        if largest != i:
            self.arr[i], self.arr[largest] = self.arr[largest], self.arr[i]
            self.swaps += 1
            self.update([i, largest], [], "Heap Sort")
            self.heapify(n, largest)


# Main

ALGORITHMS = {
    "1": ("Selection Sort", "selection_sort"),
    "2": ("Quick Sort",     "quick_sort"),
    "3": ("Heap Sort",      "heap_sort"),
    "4": ("Merge Sort",     "merge_sort"),
}

def main():
    print("""
## Sorting Algorithm Visualizer ##    

  Algorithms:
    1 - Selection Sort
    2 - Quick Sort
    3 - Heap Sort
    4 - Merge Sort
    0 - Exit
""")

    choice = input("  Enter choice: ").strip()
    if choice == "0":
        return False
    if choice not in ALGORITHMS:
        print("  Invalid choice."); return True

    size_input = input("  Array size (default 40, max 80): ").strip()
    size = int(size_input) if size_input.isdigit() else 40
    size = max(5, min(size, 80))

    speed_input = input("  Speed 1-5 (1=slow, 5=fast, default 3): ").strip()
    speed = int(speed_input) if speed_input.isdigit() and 1 <= int(speed_input) <= 5 else 3
    global DELAY
    DELAY = [0.15, 0.08, 0.04, 0.02, 0.005][speed - 1]

    arr = random.sample(range(1, 100), size)
    name, method = ALGORITHMS[choice]

    print(f"\n  Sorting {size} elements with {name}…  (close the window when done)\n")

    viz = SortingVisualizer(arr)
    viz.update([], [], f"{name} — starting array")
    time.sleep(0.5)

    getattr(viz, method)()

    print(f"\n  Done!  Comparisons: {viz.comparisons}  |  Swaps: {viz.swaps}")
    print("  Close the plot window to continue.\n")
    plt.ioff()
    plt.show()
    return True


if __name__ == "__main__":
    while True:
        again = main()
        if not again:
            break
        cont = input("\n  Sort again? (y/n): ").strip().lower()
        if cont != "y":
            break
    print("\n  Goodbye!")