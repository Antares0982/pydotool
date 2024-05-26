import os
import subprocess
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, cmake_lists_dir='.', **kwargs):
        Extension.__init__(self, name, sources=[], **kwargs)
        self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)


class cmake_build_ext(build_ext):
    def build_extensions(self):
        # Ensure that CMake is present and working
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('Cannot find CMake executable')

        cfg = 'Release'
        py_executable = sys.executable

        _ext1_dir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(self.extensions[0].name)))
        cmake_args = [
            f'-DCMAKE_BUILD_TYPE={cfg}',
            f'-DCMAKE_INSTALL_PREFIX={_ext1_dir}',
            f'-DPython_ROOT_DIR={os.path.dirname(os.path.dirname(os.path.dirname(os.__file__)))}',
            f'-DPYTHON_EXECUTABLE={py_executable}',
        ]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Config
        subprocess.check_call(['cmake', self.extensions[0].cmake_lists_dir] + cmake_args,
                              cwd=self.build_temp)

        # Build
        subprocess.check_call(['cmake', '--build', '.', '--config', cfg, '--target', 'install'],
                              cwd=self.build_temp)

        for ext in self.extensions:
            ext_fullpath = self.get_ext_fullpath(ext.name)
            extdir = os.path.abspath(os.path.dirname(ext_fullpath))
            os.rename(os.path.join(extdir, f'{ext.name}.so'), ext_fullpath)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python-ydotool',
    version="v1.0.4",
    ext_modules=[
        CMakeExtension(name='_pydotool'),
    ],
    url='https://github.com/Antares0982/pydotool',
    project_urls={
        'Bug Tracker': 'https://github.com/Antares0982/pydotool/issues',
        'Source Code': 'https://github.com/Antares0982/pydotool',
    },
    description='ydotool client implemented in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    cmdclass={'build_ext': cmake_build_ext},
    packages=['pydotool'],  # List your Python packages
)
