# built-in
import shutil
import sys
from itertools import chain
from pathlib import Path
from typing import Optional, Union

# external
import attr
from dephell_pythons import Python, Finder

# app
from ._constants import PYTHONS, IS_WINDOWS
from ._cached_property import cached_property
from ._builder import VEnvBuilder


@attr.s()
class VEnv:
    path = attr.ib(type=Path)

    project = attr.ib(type=str, default=None)
    env = attr.ib(type=str, default=None)

    def __attrs_post_init__(self) -> None:
        # `Path` as `converter` doesn't work for Python 3.5
        if type(self.path) is str:
            self.path = Path(self.path)

    # properties

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def prompt(self) -> str:
        if self.project and self.env:
            return self.project + '/' + self.env
        if self.project:
            return self.project
        if self.env:
            return self.env
        return self.path.name

    @cached_property
    def bin_path(self) -> Optional[Path]:
        if IS_WINDOWS:
            path = self.path / 'Scripts'
            if path.exists():
                return path

        path = self.path / 'bin'
        if path.exists():
            return path
        return None

    @cached_property
    def lib_path(self) -> Optional[Path]:
        # pypy
        path = self.path / 'site-packages'
        if path.exists():
            return path

        # win
        if IS_WINDOWS:
            path = self.path / 'Lib' / 'site-packages'
            if path.exists():
                return path

        # cpython unix
        if self.python_path is not None:
            path = self.path / 'lib' / self.python_path.name / 'site-packages'
            if path.exists():
                return path

        # cpython unix when python_path detected not so good
        path = self.path / 'lib'
        paths = list(path.glob('python*'))
        if not paths:
            return None
        path = paths[0] / 'site-packages'
        if path.exists():
            return path
        return None

    @cached_property
    def python_path(self) -> Optional[Path]:
        if self.bin_path is None:
            return None
        executables = {path.name for path in self.bin_path.iterdir()}
        for implementation in ('pypy', 'python'):
            for suffix in chain(PYTHONS, ['']):
                for ext in ('', '.exe'):
                    path = self.bin_path / (implementation + suffix)
                    if ext:
                        path = path.with_suffix(ext)
                    if path.name in executables:
                        return path
        return None

    @cached_property
    def python(self) -> Python:
        finder = Finder()
        python = Python(
            path=self.python_path,
            version=finder.get_version(path=self.python_path),
            implementation=finder.get_implementation(path=self.python_path),
        )
        python.lib_paths = [self.lib_path]
        return python

    # methods

    def exists(self) -> bool:
        """Returns true if venv already created and valid.

        It's a method like in `Path`.
        """
        return bool(self.bin_path)

    def create(self, python_path: Union[Path, str, None] = None) -> None:
        if python_path is None:
            python_path = sys.executable
        builder = VEnvBuilder(
            python=str(python_path),
            with_pip=True,
            prompt=self.prompt,
        )
        builder.create(str(self.path))
        self._clear_cache()

    def destroy(self) -> None:
        shutil.rmtree(str(self.path))
        self._clear_cache()

    def clone(self, path: Path) -> 'VEnv':
        shutil.copytree(str(self.path), str(path), copy_function=shutil.copy)
        # TODO: fix executables
        # https://github.com/ofek/hatch/blob/master/hatch/venv.py
        ...
        return type(self)(path=path)

    # private methods

    def _clear_cache(self):
        if 'bin_path' in self.__dict__:
            del self.__dict__['bin_path']
        if 'lib_path' in self.__dict__:
            del self.__dict__['lib_path']
        if 'python_path' in self.__dict__:
            del self.__dict__['python_path']
