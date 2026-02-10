import time
import matplotlib.pyplot as plt

def fibonacci_iterative(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b

def measure_fibonacci(n_values):
    """Calculate Fibonacci numbers and measure execution time."""
    results = []
    
    for n in n_values:
        start_time = time.time()
        fib_value = fibonacci_iterative(n)
        end_time = time.time()
        
        execution_time_s = end_time - start_time  # Keep in seconds for graph
        
        results.append({
            'n': n,
            'time_s': execution_time_s
        })
        
        # Print only time (not the Fibonacci value)
        print(f"{n}. (Time: {execution_time_s:.6f} s)")
    
    return results

def plot_results(results):
    """Create a graph showing execution time vs n-th Fibonacci term."""
    n_values = [r['n'] for r in results]
    times_s = [r['time_s'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times_s, 'o-', linewidth=2, markersize=8)
    plt.xlabel('n-th Fibonacci Term', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.title('Iterative Fibonacci Method', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Display the graph
    plt.show()

if __name__ == "__main__":
    # Define the scope of n values
    n_values = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
    
    print("Iterative Fibonacci Method - Time Measurements:")
    print("=" * 50)
    
    # Calculate and measure
    results = measure_fibonacci(n_values)
    
    # Create the graph
    plot_results(results)