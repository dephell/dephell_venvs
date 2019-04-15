# built-in
import os
import subprocess
from pathlib import Path
from typing import Optional
from venv import EnvBuilder

# external
import attr


@attr.s()
class VEnvBuilder(EnvBuilder):
    system_site_packages = attr.ib(type=bool, default=False)
    clear = attr.ib(type=bool, default=False)
    symlinks = attr.ib(type=bool, default=False)
    upgrade = attr.ib(type=bool, default=False)
    with_pip = attr.ib(type=bool, default=False)

    prompt = attr.ib(type=str, default=None)
    python = attr.ib(type=Optional[str], default=None)  # path to the python interpreter

    def ensure_directories(self, env_dir):
        context = super().ensure_directories(env_dir)
        if self.python is None:
            return context

        context.executable = self.python
        context.python_dir, context.python_exe = os.path.split(self.python)
        context.env_exe = os.path.join(context.bin_path, context.python_exe)
        return context

    def setup_python(self, context) -> None:
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
            src_library = Path(context.executable).parent / libname
            if not src_library.exists():
                continue

            dest_library = Path(context.bin_path) / libname
            if dest_library.exists():
                continue

            self.symlink_or_copy(str(src_library), str(dest_library))
            if not dest_library.is_symlink():
                dest_library.chmod(0o755)

    def _setup_pip(self, context) -> None:
        cmd = [context.env_exe, '-Im', 'ensurepip', '--upgrade', '--default-pip']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            output = result.stdout.decode() + '\n\n' + result.stderr.decode()
            raise OSError(output)
