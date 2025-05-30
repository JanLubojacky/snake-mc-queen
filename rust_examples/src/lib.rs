use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use rand_xoshiro::rand_core::{SeedableRng, RngCore};
use rand_xoshiro::Xoshiro256PlusPlus;

#[pyfunction]
fn hamming_dist(a: &str, b: &str) -> PyResult<i32> {
    // Early length check - fail fast
    if a.len() != b.len() {
        return Err(PyValueError::new_err(
            "Strings must have equal length for Hamming distance calculation",
        ));
    }
    
    let distance = a.chars()
        .zip(b.chars())
        .fold(0, |acc, (char_a, char_b)| acc + (char_a != char_b) as i32);
    
    Ok(distance)
}

// this is able to check if the strings are ascii and work only on bytes if it is
#[pyfunction]
fn hamming_dist_fast(a: &str, b: &str) -> PyResult<i32> {
    if a.len() != b.len() {
        return Err(PyValueError::new_err(
            "Strings must have equal length for Hamming distance calculation",
        ));
    }
    
    let mut distance;
    if a.is_ascii() && b.is_ascii() {
        distance = 0;
        for (byte_a, byte_b) in a.bytes().zip(b.bytes()) {
            distance += (byte_a != byte_b) as i32;
        }
    } else {
        distance = a.chars()
            .zip(b.chars())
            .fold(0, |acc, (char_a, char_b)| acc + (char_a != char_b) as i32);
    }
    
    Ok(distance)
}

/// Estimates pi using Monte Carlo method.
#[pyfunction]
fn monte_carlo_pi(nsamples: usize) -> f64 {
    let mut rng = Xoshiro256PlusPlus::seed_from_u64(0);
    let mut acc = 0;

    for _ in 0..nsamples {
        let x = (rng.next_u64() / u64::MAX) as f64;
        let y = (rng.next_u64() / u64::MAX) as f64;
        if (x * x + y * y) < 1.0 {
            acc += 1;
        }
    }

    4.0 * (acc as f64) / (nsamples as f64)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_examples(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hamming_dist, m)?)?;
    m.add_function(wrap_pyfunction!(hamming_dist_fast, m)?)?;
    m.add_function(wrap_pyfunction!(monte_carlo_pi, m)?)?;
    Ok(())
}
