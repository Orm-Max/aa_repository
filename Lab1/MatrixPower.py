import time
import matplotlib.pyplot as plt

def matrix_multiply(a, b):
    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])
    
    result = [[0] * cols_b for _ in range(rows_a)]
    
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    
    return result

def matrix_power(matrix, n):
    if n == 0:
        return [[1, 0], [0, 1]]
    
    if n == 1:
        return matrix
    
    result = [[1, 0], [0, 1]]
    base = [row[:] for row in matrix] 
    
    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, base)
        base = matrix_multiply(base, base)
        n //= 2
    
    return result

def fibonacci_matrix(n):
    F = [] 
    vec = [[0], [1]]
    Matrix = [[0, 1], [1, 1]]  
    F = matrix_power(Matrix, n)
    F = matrix_multiply(F, vec)
    return F[0][0]

def measure_fibonacci(n_values):
    results = []
    
    for n in n_values:
        start_time = time.time()
        fib_value = fibonacci_matrix(n)
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
    plt.title('Matrix Exponentiation Fibonacci Method', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    n_values = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
    
    print("Matrix Exponentiation Fibonacci Method - Time Measurements:")
    print("=" * 50)
    
    results = measure_fibonacci(n_values)
    
    plot_results(results)