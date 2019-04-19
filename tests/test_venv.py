from dephell_venvs import VEnv


def test_create(temp_path):
    venv = VEnv(path=temp_path)
    assert venv.exists() is False
    assert venv.lib_path is None
    assert venv.bin_path is None
    assert venv.python_path is None

    venv.create()

    assert venv.exists() is True
    assert venv.lib_path.exists()
    assert venv.bin_path.exists()
    assert (venv.bin_path / 'pip').exists() or (venv.bin_path / 'pip.exe').exists()
    assert venv.python_path.exists()

    venv.destroy()
    assert venv.exists() is False
