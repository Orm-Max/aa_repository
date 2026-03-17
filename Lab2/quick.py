import time
import random
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(100000)

def quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]  # last element as pivot
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def measure_quicksort(size_values):
    results = []

    for size in size_values:
        arr = [random.randint(0, 100000) for _ in range(size)]

        start_time = time.time()
        quicksort(arr, 0, len(arr) - 1)
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
    plt.plot(sizes, times_s, 'o-', color='darkorange', linewidth=2, markersize=8)
    plt.xlabel('Array Size (n)', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.title('Classic Quick Sort Performance (Lomuto)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    size_values = [
        100, 500, 1000, 2500, 5000, 7500,
        10000, 25000, 50000, 75000, 100000,
        250000, 500000, 750000, 1000000
    ]

    print("Classic Quick Sort Measurement Results:")
    print("=" * 45)

    results = measure_quicksort(size_values)
    plot_results(results)