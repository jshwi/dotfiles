import sys
import unittest.mock

import dotfiles


def test_mkarchive(nocolorcapsys, dotclone, tmpdir):
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
