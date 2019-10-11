import shutil
from pathlib import Path
import pytest


@pytest.fixture()
def temp_path(tmp_path: Path):
    for path in tmp_path.iterdir():
        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(str(path))
    yield tmp_path


@pytest.fixture(autouse=True)
def drop_ensurepip():
    yield
    path = Path(__file__).parent.parent / 'dephell_venvs' / 'ensurepip'
    if path.exists():
        shutil.rmtree(str(path))
