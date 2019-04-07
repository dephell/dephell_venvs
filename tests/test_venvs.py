from dephell_venvs import VEnvs


def test_get(temp_path):
    venvs = VEnvs(path=temp_path / 'venvs' / '{project}' / '{env}')
    (temp_path / 'papa').mkdir()
    venv = venvs.get(project_path=temp_path / 'papa', env='emeritus')
    assert venv.path == temp_path / 'venvs' / 'papa' / 'emeritus'


def test_get_by_name(temp_path):
    venvs = VEnvs(path=temp_path / 'venvs' / '{project}' / '{env}')
    venv = venvs.get_by_name(name='papa')
    assert venv.path == temp_path / 'venvs' / 'papa'


def test_iter(temp_path):
    venvs = VEnvs(path=temp_path / 'venvs' / '{project}')

    (temp_path / 'papa').mkdir()
    venv1 = venvs.get(project_path=temp_path / 'papa', env='emeritus')
    venv1.create()

    venv2 = venvs.get_by_name(name='ghost')
    venv2.create()

    assert {venv.path for venv in venvs} == {venv1.path, venv2.path}
