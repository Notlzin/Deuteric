# setup.py... but i copy pasted it because TOO LAZY!!! also hobby project not a real OS thingy #
from setuptools import setup, Extension
from Cython.Build import cythonize
import glob, os

# build all .pyx under fakebins #
pyx_files = glob.glob(os.path.join("fakebins_py", "*.pyx"))
extensions = []
for p in pyx_files:
    name = os.path.splitext(os.path.basename(p))[0]
    extensions.append(Extension(name, [p]))

setup(
    name="deuteric-fakebins",
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
)
