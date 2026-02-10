import time
import matplotlib.pyplot as plt
import sys

# Large limit to handle large n values
sys.setrecursionlimit(20000)

def fibonacci_memo(n, memo=None):
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

def measure_fibonacci(n_values):
    results = []
    
    for n in n_values:
        start_time = time.time()
        fib_value = fibonacci_memo(n)
        end_time = time.time()
        
        execution_time_s = end_time - start_time
        
        results.append({
            'n': n,
            'time_s': execution_time_s
        })
        
        print(f"{n}. (Time: {execution_time_s:.6f} s)")
    
    return results

def plot_results(results):
    n_values = [r['n'] for r in results]
    times_s = [r['time_s'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times_s, 'o-', linewidth=2, markersize=8)
    plt.xlabel('n-th Fibonacci Term', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.title('Recursive Fibonacci with Memoization', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    n_values = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
    
    print("Recursive Fibonacci with Memoization - Time Measurements:")
    print("=" * 50)
    
    results = measure_fibonacci(n_values)
    
    plot_results(results)
    
    print("\nNote: Memoization dramatically improves performance!")
    print("Even large values of n complete in milliseconds.")