from setuptools import setup, Extension
import pybind11


ext_modules = [
    Extension(
        'data_reader',
        ['data_reader.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['/O2', '/std:c++17'],
    ),
]

setup(
    name='data_reader',
    ext_modules=ext_modules,
)