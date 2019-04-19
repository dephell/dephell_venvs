## Dephell VEnvs

[![travis](https://travis-ci.org/dephell/dephell_venvs.svg?branch=master)](https://travis-ci.org/dephell/dephell_venvs)
[![appveyor](https://ci.appveyor.com/api/projects/status/github/dephell/dephell_venvs?svg=true)](https://ci.appveyor.com/project/orsinium/dephell-venvs)
[![MIT License](https://img.shields.io/pypi/l/dephell-venvs.svg)](https://github.com/dephell/dephell_venvs/blob/master/LICENSE)

Manage Python virtual environments.

## Installation

Install from [PyPI](https://pypi.org/project/dephell-venvs):

```bash
python3 -m pip install --user dephell_venvs
```

## Get venv from manager

```python
from pathlib import Path
from dephell_venvs import VEnv, VEnvs

# pass here path with substitutions:
venvs = VEnvs(path=Path() / '{project}-{digest}' / '{env}')
```

`VEnvs` gets argument `path` that is path to the virtual environment with substitutions:

+ `{project}` - last part of the path to the project.
+ `{digest}` - short hash of full path to the project to avoid collisions.
+ `{env}` - name of sub-environment because most of project need more than one environment. For example, `tests`, `docs`, `tests-py35`.

Ways to get `VEnv` object from `VEnvs`:

+ `venvs.get(project_path, env)`. Pass here path to the project and sub-environment name and DepHell will substitute them is the path template and return `VEnv` instance for this path.
+ `venvs.get_by_name(name)`. Pass only name and this will be substituted as `{project}` and other substitutions (`{digest}`, `{env}`) will be just dropped out.
+ `venvs.current` -- returns current active venv if some venv is active.

Example:

```python
venv = venvs.get(project_path=Path('dephell_venvs'), env='pytest')
# VEnv(path=PosixPath('dephell_venvs/pytest'), project='dephell_venvs', env='pytest')
```

## Manage venv

`VEnv` can be got from `VEnvs` ot created manually:

```python
venv = VEnv(path=Path('venv'))
```

Check existence:

```python
venv.exists()
# False
```

Create and destroy:

```python
venv.create()
venv.destroy()
```

Some other useful information:

```python
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
```

For details about `Python` object see [dephell_pythons](https://github.com/dephell/dephell_pythons).
