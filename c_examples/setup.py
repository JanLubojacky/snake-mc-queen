from setuptools import setup, Extension

# Define the extension module
c_examples_module = Extension(
    'c_examples',
    sources=['c_examples.c'],
    # Optional: add optimization flags
    extra_compile_args=['-O3', '-march=native', '-ffast-math', '-funroll-loops', '-flto'],
    extra_link_args=['-flto'],  # Link-time optimization
)

setup(
    name='c_examples',
    version='1.0',
    description='Fast Hamming distance and Monte Carlo pi estimation',
    ext_modules=[c_examples_module],
    zip_safe=False,
    verbose=True,
)
