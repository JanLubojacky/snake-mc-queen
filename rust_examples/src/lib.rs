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
    
    // Use bytes instead of chars for ASCII strings (much faster)
    // Falls back to char iteration for Unicode
    let distance = if a.is_ascii() && b.is_ascii() {
        a.bytes()
            .zip(b.bytes())
            .fold(0, |acc, (byte_a, byte_b)| acc + (byte_a != byte_b) as i32)
    } else {
        a.chars()
            .zip(b.chars())
            .map(|(a, b)| (a != b) as i32)
            .sum()
    };
    
    Ok(distance)
}

// #[pyfunction]
// fn hamming_dist(a: &str, b: &str) -> PyResult<u32> {
//     // Check if strings have equal byte length (faster than char count for equal-length check)
//     if a.len() != b.len() {
//         return Err(PyValueError::new_err(
//             "Strings must have equal length for Hamming distance calculation",
//         ));
//     }
//
//     // Fast path for ASCII strings (most common case)
//     if a.is_ascii() && b.is_ascii() {
//         let distance = a.bytes()
//             .zip(b.bytes())
//             .fold(0u32, |acc, (byte_a, byte_b)| acc + (byte_a != byte_b) as u32);
//         return Ok(distance);
//     }
//
//     // Fallback for Unicode strings
//     let distance = a.chars()
//         .zip(b.chars())
//         .fold(0u32, |acc, (char_a, char_b)| acc + (char_a != char_b) as u32);
//
//     Ok(distance)
// }

// #[pyfunction]  
// fn hamming_dist(a: &str, b: &str) -> PyResult<u32> {
//     if a.len() != b.len() {
//         return Err(PyValueError::new_err("Strings must have equal length"));
//     }
//
//     let mut distance = 0u32;
//     for (byte_a, byte_b) in a.bytes().zip(b.bytes()) {
//         distance += (byte_a != byte_b) as u32;
//     }
//     Ok(distance)
// }

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
    m.add_function(wrap_pyfunction!(monte_carlo_pi, m)?)?;
    Ok(())
}
