"""
tests.src_test.path_test
=========================

Test ``get_path`` which should point to the package contained within
this repository.
"""
import pathlib
import sys
import unittest.mock

import src


def test_path(nocolorcapsys, repoclone):
    """Test that the correct path is produced.

    :param nocolorcapsys:   ``capsys`` with the ANSI codes removed.
    :param repoclone:        Clone this repository and return the path
                            (pointed to the tmpdir).
    """
    name = src.get_name(echo=False)
    argv = [__name__]
    with unittest.mock.patch.object(sys, "argv", argv):
        src.get_path()
        out_1 = nocolorcapsys.stdout()
    argv = [__name__, "--exclude", ".mypy_cache"]
    with unittest.mock.patch.object(sys, "argv", argv):
        mypy_cache = pathlib.Path(repoclone) / ".mypy_cache" / "3.9" / name
        mypy_cache.mkdir(parents=True, exist_ok=True)
        src.get_path()
        out_2 = nocolorcapsys.stdout()
    assert out_1 == out_2
