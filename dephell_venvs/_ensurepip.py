from pathlib import Path
from typing import Iterator

import requests


VERSION = '3.6'
URLS = (
    'https://api.github.com/repos/python/cpython/contents/Lib/ensurepip?ref=',
    'https://api.github.com/repos/python/cpython/contents/Lib/ensurepip/_bundled?ref=',
)


def get_links() -> Iterator[str]:
    for url in URLS:
        url += VERSION
        response = requests.get(url)
        response.raise_for_status()
        for info in response.json():
            if info['type'] == 'file':
                yield info['download_url']


def download_files(path: Path) -> None:
    for link in get_links():
        relpath = link.split('/ensurepip/', maxsplit=1)[1]
        fpath = path.joinpath(relpath)
        fpath.parent.mkdir(exist_ok=True, parents=True)
        response = requests.get(link)
        response.raise_for_status()
        fpath.write_bytes(response.content)


def get_path() -> Path:
    path = Path(__file__).absolute().parent / 'ensurepip'
    if not path.exists():
        download_files(path)
    return path


def native_ensurepip_exists() -> bool:
    try:
        import ensurepip  # noqa
    except ImportError:
        return False
    else:
        return True
