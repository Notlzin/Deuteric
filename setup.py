# setup.py #
from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# modules list #
extensions = [
    Extension("src.kernel", ["src/kernel.pyx"]),
    Extension("src.procman", ["src/procman.pyx"]),
    Extension("src.memman", ["src/memman.pyx"]),
    Extension("src.shell", ["src/shell.pyx"]),
]

# automatically include .pxd files
for e in extensions:
    e.include_dirs.append(os.path.join("src"))

setup(
    name="Deuteric",
    version="1.0.0",
    description="experimental python OS",
    author="Neiteln|Notlzin",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "boundscheck": False,
            "wraparound": False,
        },
    ),
    packages=["src"],
)

# to run: python setup.py build_ext --inplace #
# this is prob UNUSED LOL #
