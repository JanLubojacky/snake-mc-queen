import random
import statistics
import string
import time
from collections.abc import Callable

from python_examples.main import hamming_dist, hamming_dist_numba
from rust_examples import hamming_dist as hamming_dist_rust


def random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def benchmark(
    func: Callable[[str, str], int],
    pairs: list[tuple[str, str]],
    iterations: int = 1000,
) -> list[float]:
    times: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        for s1, s2 in pairs:
            _ = func(s1, s2)
        times.append((time.perf_counter() - start) * 1000)
    return times


def benchmark_hamming_dist():
    random.seed(42)
    lengths = [10, 100, 1000, 10000]

    print(
        "Length\tPython (ms)\t\tNumba (ms)\t\tRust (ms)\t\tSpeedup rust\t\tSpeedup numba"
    )
    print("-" * 130)

    for length in lengths:
        # Generate 10 random string pairs for this length
        pairs = [(random_string(length), random_string(length)) for _ in range(10)]

        # Benchmark both implementations
        py_times = benchmark(hamming_dist, pairs)
        py_mean = statistics.mean(py_times)
        py_std = statistics.stdev(py_times)

        rust_times = benchmark(hamming_dist_rust, pairs)
        rust_mean = statistics.mean(rust_times)
        rust_std = statistics.stdev(rust_times)

        numba_times = benchmark(hamming_dist_numba, pairs)
        numba_mean = statistics.mean(numba_times)
        numba_std = statistics.stdev(numba_times)

        speedup_rust = py_mean / rust_mean
        speedup_numba = py_mean / numba_mean

        print(
            f"{length}\t{py_mean:.3f} ± {py_std:.3f}\t\t{numba_mean:.3f} ± {numba_std:.3f}\t\t{rust_mean:.3f} ± {rust_std:.3f}\t\t{speedup_rust:.2f}x\t\t{speedup_numba:.2f}x"
        )
