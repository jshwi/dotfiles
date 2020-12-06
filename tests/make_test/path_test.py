import os
import pathlib
import sys

import pyshared
import unittest.mock


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


def test_modules(nocolorcapsys, dotclone):
    tests = os.path.join(dotclone, "tests")
    docs_conf = os.path.join(dotclone, "docs", "conf.py")
    pyshared_package = os.path.join(dotclone, "lib", "make", "pyshared")
    app_path = pyshared.get_path(echo=False)
    argv = [
        __name__,
        tests,
        docs_conf,
        pyshared_package,
        app_path,
        "--exclude",
        tests,
    ]
    var_app_path = os.path.relpath(app_path, dotclone).replace(os.sep, ".")
    with unittest.mock.patch.object(sys, "argv", argv):
        pyshared.modules()
    out = [s.strip() for s in nocolorcapsys.stdout().splitlines()]
    assert out == ["lib.make.pyshared", var_app_path]
