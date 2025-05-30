#include <Python.h>
#include <stdlib.h>
#include <time.h>


// C implementation of hamming_dist
static PyObject* hamming_dist(PyObject* self, PyObject* args) {
    PyObject *str_a, *str_b;
    
    // Parse arguments - expect two string objects
    if (!PyArg_ParseTuple(args, "UU", &str_a, &str_b)) {
        return NULL;
    }
    
    // Get string lengths
    Py_ssize_t len_a = PyUnicode_GET_LENGTH(str_a);
    Py_ssize_t len_b = PyUnicode_GET_LENGTH(str_b);
    
    // Check if lengths are equal
    if (len_a != len_b) {
        PyErr_SetString(PyExc_ValueError, 
            "Strings must have equal length for Hamming distance calculation");
        return NULL;
    }
    
    int count = 0;
    
    // Compare characters
    for (Py_ssize_t i = 0; i < len_a; i++) {
        Py_UCS4 char_a = PyUnicode_READ_CHAR(str_a, i);
        Py_UCS4 char_b = PyUnicode_READ_CHAR(str_b, i);
        
        if (char_a != char_b) {
            count++;
        }
    }
    
    return PyLong_FromLong(count);
}

// Xoshiro256++ implementation
static inline uint64_t rotl(const uint64_t x, int k) {
    return (x << k) | (x >> (64 - k));
}


uint64_t xoshiro_next(uint64_t s[4]) {
    const uint64_t result = rotl(s[0] + s[3], 23) + s[0];
    const uint64_t t = s[1] << 17;

    s[2] ^= s[0];
    s[3] ^= s[1];
    s[1] ^= s[2];
    s[0] ^= s[3];

    s[2] ^= t;
    s[3] = rotl(s[3], 45);

    return result;
}

// C implementation of monte_carlo_pi
static PyObject* monte_carlo_pi(PyObject* self, PyObject* args) {
    int nsamples;

     uint64_t local_s[4] = {42, 42^0xAAAAAAAAAAAAAAAAULL, 
                           42^0x5555555555555555ULL, 
                           42^0xCCCCCCCCCCCCCCCCULL};   

    // Parse arguments - expect one integer
    if (!PyArg_ParseTuple(args, "i", &nsamples)) {
        return NULL;
    }
    
    if (nsamples <= 0) {
        PyErr_SetString(PyExc_ValueError, "Number of samples must be positive");
        return NULL;
    }
        
    int acc = 0;
    
    for (int i = 0; i < nsamples; i++) {
        uint64_t rand1 = xoshiro_next(local_s);
        uint64_t rand2 = xoshiro_next(local_s);
          
        double x = (double)rand1 / (double)UINT64_MAX;
        double y = (double)rand2 / (double)UINT64_MAX;

        if ((x * x + y * y) < 1.0) {
            acc++;
        }
    }
    
    double pi_estimate = 4.0 * (double)acc / (double)nsamples;
    return PyFloat_FromDouble(pi_estimate);
}

// Method definitions
static PyMethodDef module_methods[] = {
    {"hamming_dist", hamming_dist, METH_VARARGS, 
     "Calculate the Hamming distance between two strings"},
    {"monte_carlo_pi", monte_carlo_pi, METH_VARARGS, 
     "Estimate pi using Monte Carlo method"},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef c_examples_module = {
    PyModuleDef_HEAD_INIT,
    "c_examples",                    // Module name
    "Fast Hamming distance and Monte Carlo pi estimation", // Module docstring
    -1,                              // Size of per-interpreter state, -1 means global state
    module_methods                   // Method definitions
};

// Module initialization function
PyMODINIT_FUNC PyInit_c_examples(void) {
    return PyModule_Create(&c_examples_module);
}
