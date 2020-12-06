"""
tests.dotfiles_test.mkarchive_test
==================================

Test making of the archive and moving it to the dynamically created
dated directory path.
"""
import os
import sys
import unittest.mock

import dotfiles
import pytest

from . import expected


def test_mkarchive(nocolorcapsys, dotclone, tmpdir):
    """Test the tarring and moving of the ``mkarchive`` function.

    :param nocolorcapsys:   ``capsys`` with the ANSI codes removed.
    :param dotclone:        Path to cloned version of this repository
    :param tmpdir:          The temporary directory ``pytest`` fixture.
    """
    _expected = expected.mkarchive(
        tmpdir, dotclone, dotfiles.DATE, dotfiles.TIME
    )
    with unittest.mock.patch.object(sys, "argv", [__name__, dotclone]):
        dotfiles.mkarchive.main()
        out = nocolorcapsys.stdout().splitlines()
        assert out == _expected


def test_mkarchive_file(nocolorcapsys, dotclone, tmpdir):
    target = os.path.join(dotclone, "README.rst")
    _expected = expected.mkarchive(
        tmpdir, target, dotfiles.DATE, dotfiles.TIME
    )
    with unittest.mock.patch.object(sys, "argv", [__name__, target]):
        dotfiles.mkarchive.main()
        out = nocolorcapsys.stdout().splitlines()
        assert out == _expected


def test_mkarchive_no_file(nocolorcapsys, dotclone, tmpdir):
    target = os.path.join(dotclone, "this_is_not_a_file.txt")
    with unittest.mock.patch.object(sys, "argv", [__name__, target]):
        with pytest.raises(FileNotFoundError):
            dotfiles.mkarchive.main()
            err = nocolorcapsys.stderr().splitlines()
            assert err == f"[Errno 2] No such file or directory: '{target}'"
