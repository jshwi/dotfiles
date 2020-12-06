import pathlib
import sys
import unittest.mock

import pyshared


def test_name(project_name):
    name = pyshared.get_name(echo=False)
    assert name == project_name


def test_path(nocolorcapsys, dotclone):
    name = pyshared.get_name(echo=False)
    argv = [__name__]
    with unittest.mock.patch.object(sys, "argv", argv):
        pyshared.get_path()
        out_1 = nocolorcapsys.stdout()
    argv = [__name__, "--exclude", ".mypy_cache"]
    with unittest.mock.patch.object(sys, "argv", argv):
        mypy_cache = pathlib.Path(dotclone) / ".mypy_cache" / "3.9" / name
        mypy_cache.mkdir(parents=True, exist_ok=True)
        pyshared.get_path()
        out_2 = nocolorcapsys.stdout()
    assert out_1 == out_2
