## Dephell VEnvs

Manage Python virtual environments.

## Installation

Install from [PyPI](https://pypi.org/project/dephell-pythons):

```bash
python3 -m pip install --user dephell_venvs
```

## Usage

```python
from pathlib import Path
from dephell_venvs import VEnv, VEnvs

# pass here path with substitutions:
venvs = VEnvs(path=Path() / '{project}-{digest}' / '{env}')

# pass here path to the project and subenvironment name:
venv = venvs.get(project_path=Path('dephell_venvs'), env='pytest')
# VEnv(path=PosixPath('tests/pytest'), project='dephell_venvs', env='pytest')

venv.exists()
# False

venv.create()

venv.exists()
# True

venv.bin_path
# PosixPath('dephell_venvs-njyT/pytest/bin')
venv.lib_path
# PosixPath('dephell_venvs-njyT/pytest/lib/python3.7/site-packages')
venv.python_path
# PosixPath('dephell_venvs-njyT/pytest/bin/python3.7')

venv.prompt
# 'dephell_venvs/pytest'

venv.python
# Python(path=PosixPath('dephell_venvs-njyT/pytest/bin/python3.7'), version='3.7.0', implementation='python', abstract=False)

venv.destroy()
```
