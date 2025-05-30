import random
import statistics
import time

from python_examples.main import monte_carlo_pi
from rust_examples import monte_carlo_pi as monte_carlo_pi_rs
from cython_examples.cython_examples import monte_carlo_pi as monte_carlo_pi_cython


def benchmark_monte():
    random.seed(42)
    sample_counts = [1000, 10000, 100000, 1000000, 10000000]
    iterations = 10

    print("Samples\t\tNumba (ms)\t\tCython (ms)\t\tRust (ms)")
    print("-" * 60)

    for nsamples in sample_counts:
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
            pi = monte_carlo_pi(nsamples)

        # Benchmark Numba
        numba_times: list[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            pi = monte_carlo_pi(nsamples)
            numba_times.append((time.perf_counter() - start) * 1000)

        numba_mean = statistics.mean(numba_times)
        numba_std = statistics.stdev(numba_times)

        # Benchmark Cython
        cython_times: list[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            pi = monte_carlo_pi_cython(nsamples)
            cython_times.append((time.perf_counter() - start) * 1000)

        cython_mean = statistics.mean(cython_times)
        cython_std = statistics.stdev(cython_times)

        print(
            f"{nsamples}\t\t\t{numba_mean:.3f} ± {numba_std:.3f}\t\t{cython_mean:.3f} ± {cython_std:.3f}\t\t{rust_mean:.3f} ± {rust_std:.3f}"
        )


if __name__ == "__main__":
    benchmark_monte()
