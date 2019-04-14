# built-in
import os
import subprocess
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

    def _setup_pip(self, context) -> None:
        cmd = [context.env_exe, '-Im', 'ensurepip', '--upgrade', '--default-pip']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            output = result.stdout.decode() + '\n\n' + result.stderr.decode()
            raise OSError(output)
