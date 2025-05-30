import random
import statistics
import time

from hamming_py.main import monte_carlo_pi
from hamming_rs import monte_carlo_pi as monte_carlo_pi_rs


def benchmark_monte():
    random.seed(42)
    sample_counts = [1000, 10000, 100000, 1000000, 10000000]
    iterations = 10

    print("Samples\t\tNumba (ms)\t\tRust (ms)")
    print("-" * 40)

    for nsamples in sample_counts:
        # Benchmark Rust
        rust_times: list[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            pi = monte_carlo_pi_rs(nsamples)
            assert round(pi) == 3
            rust_times.append((time.perf_counter() - start) * 1000)

        rust_mean = statistics.mean(rust_times)
        rust_std = statistics.stdev(rust_times)

        # Benchmark Numba
        numba_times: list[float] = []
        for _ in range(iterations):
            start = time.perf_counter()
            pi = monte_carlo_pi(nsamples)
            assert round(pi) == 3
            numba_times.append((time.perf_counter() - start) * 1000)

        numba_mean = statistics.mean(numba_times)
        numba_std = statistics.stdev(numba_times)

        print(
            f"{nsamples}\t\t\t{rust_mean:.3f} ± {rust_std:.3f}\t\t{numba_mean:.3f} ± {numba_std:.3f}"
        )


if __name__ == "__main__":
    benchmark_monte()
