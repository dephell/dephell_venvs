# built-in
import os
from base64 import b64encode
from hashlib import md5
from pathlib import Path
from typing import Iterator, Optional

# external
import attr

# app
from ._cached_property import cached_property
from ._venv import VEnv


@attr.s()
class VEnvs:
    path = attr.ib(type=Path, converter=Path)

    @cached_property
    def current(self) -> Optional[VEnv]:
        if 'VIRTUAL_ENV' in os.environ:
            return VEnv(path=os.environ['VIRTUAL_ENV'])
        # TODO: CONDA_PREFIX?
        return None

    @staticmethod
    def _encode(text: str) -> str:
        digest_bin = md5(text.encode('utf-8')).digest()
        digest_str = b64encode(digest_bin).decode()
        return digest_str.replace('+', '').replace('/', '')[:4]

    def get(self, project_path: Path, env: str) -> VEnv:
        if not project_path.exists():
            raise FileNotFoundError('Project directory does not exist')
        if not project_path.is_dir():
            raise IOError('Project path is not directory')
        formatted = str(self.path).format(
            project=project_path.name,
            digest=self._encode(str(project_path)),
            env=env,
        )
        path = Path(formatted.replace(os.path.sep + os.path.sep, os.path.sep))
        return VEnv(path=path, project=project_path.name, env=env)

    def get_by_name(self, name) -> VEnv:
        formatted = str(self.path).replace('-{digest}', '').format(project=name, digest='', env='')
        path = Path(formatted.replace(os.path.sep + os.path.sep, os.path.sep))
        return VEnv(path=path, project=name)

    def __iter__(self) -> Iterator[VEnv]:
        for path in self.path.iterdir():
            venv = VEnv(path=path)
            if venv.exists():
                yield venv
