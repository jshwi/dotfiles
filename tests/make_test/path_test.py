import pathlib

import pyshared


def test_name(nocolorcapsys, project_name):
    name = pyshared.get_name(echo=False)
    assert name == project_name


def test_path(nocolorcapsys, dotclone):
    pyshared.get_path()
    out_1 = nocolorcapsys.stdout()
    mypy_cache = pathlib.Path(dotclone) / ".mypy_cache" / "3.9" / "dotfiles"
    mypy_cache.mkdir(parents=True, exist_ok=True)
    pyshared.get_path()
    out_2 = nocolorcapsys.stdout()
    assert out_1 == out_2
