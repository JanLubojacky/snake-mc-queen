import random
import statistics
import string
import time
from collections.abc import Callable

from cython_examples.cython_examples import hamming_dist as hamming_dist_cython
from python_examples.main import hamming_dist, hamming_dist_numba
from rust_examples import hamming_dist as hamming_dist_rust
from c_examples import hamming_dist as hamming_dist_c


def random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def benchmark(
    func: Callable[[str, str], int],
    pairs: list[tuple[str, str]],
    iterations: int = 100,
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
    lengths = [100, 1000, 10000, 100000]

    headers = [
        "Length",
        "Python (ms)",
        "Numba (ms)",
        "Cython (ms)",
        "Rust (ms)",
        "C (ms)",
        "Speedup rust",
        "Speedup numba",
        "Speedup cython",
        "Speedup C"
    ]
    col_width = 20

    # Print header row
    header_row = "".join(h.ljust(col_width) for h in headers)
    print(header_row)
    print("-" * (col_width * len(headers)))

    for length in lengths:
        # Generate 10 random string pairs for this length
        pairs = [(random_string(length), random_string(length)) for _ in range(10)]

        # Benchmark all implementations
        py_times = benchmark(hamming_dist, pairs)
        py_mean = statistics.mean(py_times)
        py_std = statistics.stdev(py_times)

        rust_times = benchmark(hamming_dist_rust, pairs)
        rust_mean = statistics.mean(rust_times)
        rust_std = statistics.stdev(rust_times)

        numba_times = benchmark(hamming_dist_numba, pairs)
        numba_mean = statistics.mean(numba_times)
        numba_std = statistics.stdev(numba_times)

        cython_times = benchmark(hamming_dist_cython, pairs)
        cython_mean = statistics.mean(cython_times)
        cython_std = statistics.stdev(cython_times)

        c_times = benchmark(hamming_dist_c, pairs)
        c_mean = statistics.mean(c_times)
        c_std = statistics.stdev(c_times)

        speedup_rust = py_mean / rust_mean
        speedup_numba = py_mean / numba_mean
        speedup_cython = py_mean / cython_mean
        speedup_c = py_mean / c_mean

        # Format each column with consistent spacing
        row = [
            f"{length}".ljust(col_width),
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
    benchmark_hamming_dist()
