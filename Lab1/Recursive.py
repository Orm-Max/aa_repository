import time
import matplotlib.pyplot as plt

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def measure_fibonacci(n_values):
    results = []
    
    for n in n_values:
        start_time = time.time()
        fib_value = fibonacci(n)
        end_time = time.time()
        
        execution_time_s = end_time - start_time
        
        results.append({
            'n': n,
            'fibonacci': fib_value,
            'time_s': execution_time_s
        })
        
        print(f"{n}. {fib_value} (Time: {execution_time_s:.4f} s)")
    
    return results

def plot_results(results):
    n_values = [r['n'] for r in results]
    times_s = [r['time_s'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times_s, 'o-', linewidth=2, markersize=8)
    plt.xlabel('n-th Fibonacci Term', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.title('Recursive Fibonacci Function', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Display the graph
    plt.show()

if __name__ == "__main__":
    # Define the scope of n values
    n_values = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]
    
    print("Recursive Fibonacci Calculation Results:")
    print("=" * 50)
    
    # Calculate and measure
    results = measure_fibonacci(n_values)
    
    # Create the graph
    plot_results(results)