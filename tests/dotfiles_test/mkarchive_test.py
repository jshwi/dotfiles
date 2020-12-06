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
from . import expected


def test_mkarchive(nocolorcapsys, dotclone, tmpdir):
    """Test the tarring and moving of the ``mkarchive`` function.

    :param nocolorcapsys:   ``capsys`` with the ANSI codes removed.
    :param dotclone:        Path to cloned version of this repository
    :param tmpdir:          The temporary directory ``pytest`` fixture.
    """
    argv = [__name__, dotclone]
    _expected = expected.mkarchive(tmpdir, dotfiles.DATE, dotfiles.TIME)
    with unittest.mock.patch.object(sys, "argv", argv):
        dotfiles.mkarchive.main()
        out = nocolorcapsys.stdout().splitlines()
        assert out == _expected


def test_mkarchive_file(nocolorcapsys, dotclone, tmpdir):
    target = os.path.join(dotclone, "README.rst")
    argv = [__name__, target]
    _expected = expected.mkarchive(
        tmpdir, target, dotfiles.DATE, dotfiles.TIME
    )
    with unittest.mock.patch.object(sys, "argv", argv):
        dotfiles.mkarchive.main()
        out = nocolorcapsys.stdout().splitlines()
        assert out == _expected
