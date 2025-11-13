from setuptools import setup, Extension
import pybind11


ext_modules = [
    Extension(
        'line_breaker',
        ['line_breaker.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['/O2', '/std:c++17'],
    ),
]

setup(
    name='line_breaker',
    ext_modules=ext_modules,
)