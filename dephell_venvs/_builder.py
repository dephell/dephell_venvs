# built-in
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Optional
from venv import EnvBuilder

# external
import attr
from dephell_pythons import Finder


@attr.s()
class VEnvBuilder(EnvBuilder):
    system_site_packages = attr.ib(type=bool, default=False)
    clear = attr.ib(type=bool, default=False)
    symlinks = attr.ib(type=bool, default=False)
    upgrade = attr.ib(type=bool, default=False)
    with_pip = attr.ib(type=bool, default=False)

    prompt = attr.ib(type=str, default=None)
    python = attr.ib(type=Optional[str], default=None)  # path to the python interpreter

    def get_python(self) -> str:
        if self.python is None:
            return sys.executable

        # if not venv then it's OK
        config_path = Path(self.python).parent.parent / 'pyvenv.cfg'
        if not config_path.exists():
            return self.python

        # try to get home from venv config
        lib_path = None
        for line in config_path.read_text().splitlines():
            if line.startswith('home'):
                lib_path = line.split('=', 1)[1].strip()
        if not lib_path:
            return self.python
        lib_path = Path(lib_path)

        # try to find python in real home
        finder = Finder()
        paths = list(finder.get_pythons(paths=[lib_path]))
        if not paths:
            raise LookupError('cannot find pythons in ' + str(lib_path))
        if len(paths) == 1:
            return str(paths[0])

        # get from these pythons python with the same version
        version = finder.get_version(Path(self.python))
        for path in paths:
            if finder.get_version(path) == version:
                return str(path)
        raise LookupError('cannot choose python in ' + str(lib_path))

    def ensure_directories(self, env_dir: str) -> SimpleNamespace:
        context = super().ensure_directories(env_dir)
        if self.python is None:
            return context

        context.executable = self.get_python()
        context.python_dir, context.python_exe = os.path.split(context.executable)
        context.env_exe = os.path.join(context.bin_path, context.python_exe)
        return context

    def setup_python(self, context: SimpleNamespace) -> None:
        """
        Set up a Python executable in the environment.

        :param context: The information for the environment creation request
                        being processed.
        """
        super().setup_python(context)

        if os.name == 'nt':
            return

        # copy pypy libs
        for libname in ('libpypy3-c.so', 'libpypy3-c.dylib'):
            src_library = Path(context.executable).resolve().parent / libname
            if not src_library.exists():
                continue

            dest_library = Path(context.bin_path) / libname
            if dest_library.exists():
                continue

            self.symlink_or_copy(str(src_library), str(dest_library))
            if not dest_library.is_symlink():
                dest_library.chmod(0o755)

    def _setup_pip(self, context: SimpleNamespace) -> None:
        cmd = [context.env_exe, '-Im', 'ensurepip', '--upgrade', '--default-pip']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            output = result.stdout.decode() + '\n\n' + result.stderr.decode()
            raise OSError(output)
