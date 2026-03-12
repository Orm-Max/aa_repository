import time
import random
import matplotlib.pyplot as plt

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) - 1]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def measure_quicksort(size_values):
    results = []

    for size in size_values:
        arr = [random.randint(0, 100000) for _ in range(size)]

        start_time = time.time()
        sorted_arr = quicksort(arr)
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
    plt.title('Recursive Quick Sort Performance', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    size_values = [
        100, 500, 1000, 2500, 5000, 7500,
        10000, 25000, 50000, 75000, 100000,
        250000, 500000, 750000, 1000000
    ]

    print("Recursive Quick Sort Measurement Results:")
    print("=" * 45)

    results = measure_quicksort(size_values)

    plot_results(results)