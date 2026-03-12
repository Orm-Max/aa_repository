import time
import random
import matplotlib.pyplot as plt

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapsort(arr):
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr

def measure_heapsort(size_values):
    results = []

    for size in size_values:
        arr = [random.randint(0, 100000) for _ in range(size)]

        start_time = time.time()
        sorted_arr = heapsort(arr)
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
    plt.plot(sizes, times_s, 'o-', color='steelblue', linewidth=2, markersize=8)
    plt.xlabel('Array Size (n)', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.title('Heap Sort Performance', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    size_values = [
        100, 500, 1000, 2500, 5000, 7500,
        10000, 25000, 50000, 75000, 100000,
        250000, 500000, 750000, 1000000
    ]

    print("Heap Sort Measurement Results:")
    print("=" * 45)

    results = measure_heapsort(size_values)

    plot_results(results)