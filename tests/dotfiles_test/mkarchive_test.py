"""
tests.dotfiles_test.mkarchive_test
==================================

Test making of the archive and moving it to the dynamically created
dated directory path.
"""
import sys
import unittest.mock

import dotfiles


def test_mkarchive(nocolorcapsys, dotclone, tmpdir):
    """Test the tarring and moving of the ``mkarchive`` function.

    :param nocolorcapsys:   ``capsys`` with the ANSI codes removed.
    :param dotclone:        Path to cloned version of this repository
    :param tmpdir:          The temporary directory ``pytest`` fixture.
    """
    argv = [__name__, dotclone]
    date = dotfiles.DATE
    time = dotfiles.TIME
    archive_name = time + "..dotfiles.tar.gz"
    expected = [
        "Adding Documents/Archive/" + date + "/ to " + str(tmpdir),
        "Making archive",
        ". created " + archive_name,
        "Storing archive",
        ". " + archive_name + " -> "
        "~/Documents/Archive/" + date + "/" + time + "..dotfiles.tar.gz",
        "Done",
    ]
    with unittest.mock.patch.object(sys, "argv", argv):
        dotfiles.mkarchive.main()
        out = nocolorcapsys.stdout().splitlines()
        assert out == expected
