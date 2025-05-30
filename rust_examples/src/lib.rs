use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use rand::Rng;

/// Calculates the Hamming distance between two strings.
#[pyfunction]
fn hamming_dist(a: &str, b: &str) -> PyResult<i32> {
    // Check if strings have equal length
    if a.len() != b.len() {
        return Err(PyValueError::new_err(
            "Strings must have equal length for Hamming distance calculation",
        ));
    }

    // Calculate Hamming distance by counting differing characters
    let distance = a
        .chars()
        .zip(b.chars())
        .map(|(char_a, char_b)| if char_a != char_b { 1 } else { 0 })
        .sum();

    Ok(distance)
}

/// Estimates pi using Monte Carlo method.
#[pyfunction]
fn monte_carlo_pi(nsamples: usize) -> f64 {
    let mut rng = rand::rng();
    let mut acc = 0;

    for _ in 0..nsamples {
        let x: f64 = rng.random();
        let y: f64 = rng.random();
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
    m.add_function(wrap_pyfunction!(monte_carlo_pi, m)?)?;
    Ok(())
}
