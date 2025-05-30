import random

from numba import njit


def hamming_dist(a: str, b: str) -> int:
    """
    Calculate the Hamming distance between two strings.

    Args:
        a: First string
        b: Second string

    Returns:
        int: The Hamming distance (number of differing characters)

    Raises:
        ValueError: If strings have different lengths
    """
    if len(a) != len(b):
        raise ValueError(
            "Strings must have equal length for Hamming distance calculation"
        )

    return sum(char_a != char_b for char_a, char_b in zip(a, b))


def monte_carlo_pi(nsamples: int) -> float:
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples


@njit
def hamming_dist_numba(a: str, b: str) -> int:
    """
    Alternative numba implementation using explicit indexing.
    """

    if len(a) != len(b):
        return -1

    count = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            count += 1

    return count


@njit
def monte_carlo_pi_numba(nsamples: int) -> float:
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples
