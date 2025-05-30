# cython: language_level=3
import cython
from libc.stdlib cimport rand, RAND_MAX
from libc.math cimport sqrt

@cython.boundscheck(False)
@cython.wraparound(False)
def hamming_dist(str a, str b):
    """
    Calculate the Hamming distance between two strings using Cython.
    Works correctly with UTF-8/Unicode strings.
    """
    cdef int len_a = len(a)
    cdef int len_b = len(b)
    
    if len_a != len_b:
        raise ValueError(
            "Strings must have equal length for Hamming distance calculation"
        )
    
    cdef int count = 0
    cdef int i
    
    # Compare characters directly, not bytes
    for i in range(len_a):
        if a[i] != b[i]:
            count += 1
    
    return count

@cython.boundscheck(False)
@cython.wraparound(False) 
def monte_carlo_pi(int nsamples):
    """
    Estimate pi using Monte Carlo method with Cython.

    Args:
        nsamples: Number of samples to use for the estimation

    Returns:
        float: The estimated value of pi
    """
    cdef int acc = 0
    cdef int i
    cdef double x, y
    
    for i in range(nsamples):
        x = <double>rand() / <double>RAND_MAX
        y = <double>rand() / <double>RAND_MAX
        if (x * x + y * y) < 1.0:
            acc += 1
    
    return 4.0 * <double>acc / <double>nsamples
