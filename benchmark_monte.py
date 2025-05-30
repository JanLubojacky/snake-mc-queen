import random
import statistics
import time

from cython_examples.cython_examples import monte_carlo_pi as monte_carlo_pi_cython
from python_examples.main import monte_carlo_pi, monte_carlo_pi_numba
from rust_examples import monte_carlo_pi as monte_carlo_pi_rs
from c_examples import monte_carlo_pi as monte_carlo_pi_c


def benchmark_monte():
    random.seed(42)
    sample_counts = [1000, 10000, 100000, 1000000]
    iterations = 10

    headers = [
        "Length",
        "Python (ms)",
        "Numba (ms)",
        "Cython (ms)",
        "Rust (ms)",
        "C (ms)",
        "Speedup numba",
        "Speedup cython",
        "Speedup rust",
        "Speedup C"
    ]
    col_width = 20

    # Print header row
    header_row = "".join(h.ljust(col_width) for h in headers)
    print(header_row)
    print("-" * (col_width * len(headers)))

    for nsamples in sample_counts:
        # Benchmark plain Python
        py_times: list[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            pi = monte_carlo_pi(nsamples)
            py_times.append((time.perf_counter() - start) * 1000)

        py_mean = statistics.mean(py_times)
        py_std = statistics.stdev(py_times)

        # Benchmark Rust
        rust_times: list[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            pi = monte_carlo_pi_rs(nsamples)
            rust_times.append((time.perf_counter() - start) * 1000)

        rust_mean = statistics.mean(rust_times)
        rust_std = statistics.stdev(rust_times)

        # warm up numba
        for _ in range(10):
            pi = monte_carlo_pi_numba(nsamples)

        # Benchmark Numba
        numba_times: list[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            pi = monte_carlo_pi_numba(nsamples)
            numba_times.append((time.perf_counter() - start) * 1000)

        numba_mean = statistics.mean(numba_times)
        numba_std = statistics.stdev(numba_times)

        # Benchmark Cython
        cython_times: list[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            pi = monte_carlo_pi_cython(nsamples)
            cython_times.append((time.perf_counter() - start) * 1000)

        c_times: list[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            pi = monte_carlo_pi_c(nsamples)
            c_times.append((time.perf_counter() - start) * 1000)

        c_mean = statistics.mean(c_times)
        c_std = statistics.stdev(c_times)

        cython_mean = statistics.mean(cython_times)
        cython_std = statistics.stdev(cython_times)

        speedup_rust = py_mean / rust_mean
        speedup_numba = py_mean / numba_mean
        speedup_cython = py_mean / cython_mean
        speedup_c = py_mean / c_mean

        # Format each column with consistent spacing
        row = [
            f"{nsamples}".ljust(col_width),
            f"{py_mean:.3f} ± {py_std:.3f}".ljust(col_width),
            f"{numba_mean:.3f} ± {numba_std:.3f}".ljust(col_width),
            f"{cython_mean:.3f} ± {cython_std:.3f}".ljust(col_width),
            f"{rust_mean:.3f} ± {rust_std:.3f}".ljust(col_width),
            f"{c_mean:.3f} ± {c_std:.3f}".ljust(col_width),
            f"{speedup_numba:.2f}x".ljust(col_width),
            f"{speedup_cython:.2f}x".ljust(col_width),
            f"{speedup_rust:.2f}x".ljust(col_width),
            f"{speedup_c:.2f}x".ljust(col_width),
        ]

        print("".join(row))


if __name__ == "__main__":
    benchmark_monte()
