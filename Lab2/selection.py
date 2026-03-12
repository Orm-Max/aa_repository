import time
import random
import matplotlib.pyplot as plt

def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

def measure_selection_sort(size_values):
    results = []

    for size in size_values:
        arr = [random.randint(0, 100000) for _ in range(size)]

        start_time = time.time()
        sorted_arr = selection_sort(arr)
        end_time = time.time()

        execution_time_s = end_time - start_time

        results.append({
            'size': size,
            'time_s': execution_time_s
        })

        print(f"Size: {size:>7} | Time: {execution_time_s:.6f} s")

    return results

def plot_results(results):
    sizes = [r['size'] for r in results]
    times_s = [r['time_s'] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_s, 'o-', color='mediumpurple', linewidth=2, markersize=8)
    plt.xlabel('Array Size (n)', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.title('Selection Sort Performance', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    size_values = [
        100, 250, 500, 625, 750, 875, 1000, 1125, 1250, 1875, 2500, 3125, 3750, 4375, 5000
    ]

    print("Selection Sort Measurement Results:")
    print("=" * 45)

    results = measure_selection_sort(size_values)

    plot_results(results)