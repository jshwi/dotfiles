"""
tests._test.py
==============
"""
import os
import sys
import unittest.mock

import dotfiles
from . import expected


def install(nocolorcapsys):
    """Run the install process and return it's output stripped of any
    ANSI escaped color codes. The returned output can be used or ignored
    to control the stream of stdout/ stderr.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :return:                Stdout.
    """
    dotfiles.main()
    return nocolorcapsys.stdout()


def test_output(nocolorcapsys):
    """Test that the actual output informing the user of the process
    matches the expected output.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :return:                Stdout.
    """
    out = install(nocolorcapsys)
    assert out == expected.output(dotfiles.HOME)


def test_symlinks(nocolorcapsys):
    """Test that the process has created all symlinks. This will also
    ensure no symlinks are broken.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    install(nocolorcapsys)
    contents = os.listdir(dotfiles.HOME)
    for _, val in expected.PAIRS.items():
        if val in expected.FOLLOW_PATH:
            path = os.path.join(dotfiles.HOME, val)
            assert os.path.islink(path)
        else:
            assert val in contents


def test_backups(nocolorcapsys, suffix):
    """Test that the actual output informing the user of the process,
    including the backing up of files, matches the expected output.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :param suffix:          The time suffix fixture to be appended to
                            the file taken from the ``dotfiles.SUFFIX``
                            constant so as to ensure a match.
    """
    test_output(nocolorcapsys)
    out = install(nocolorcapsys)
    assert out == expected.backups(dotfiles.HOME, suffix)


def test_dry_run(nocolorcapsys):
    """Test that the actual output informing the user of the process,
    including the notice that this is a dry-run, matches the expected
    output. Also ensure that no files were changed, created, or removed
    by comparing a before and after.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    sys.argv.append("--dry")
    freeze_dir = os.listdir(dotfiles.HOME)
    out = install(nocolorcapsys)
    assert out == expected.dry_run(dotfiles.HOME)
    updated_dir = os.listdir(dotfiles.HOME)
    assert updated_dir == freeze_dir


def test_dry_run_backups(nocolorcapsys, suffix):
    """Test that the actual output informing the user of the process,
    including the notice that this is a dry-run of a run including
    backups, matches the expected output. Also ensure that no files were
    changed, created, or removed by comparing a before and after.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :param suffix:
    """
    test_output(nocolorcapsys)
    sys.argv.append("--dry")
    freeze_dir = os.listdir(dotfiles.HOME)
    out = install(nocolorcapsys)
    assert out == expected.dry_run_backups(dotfiles.HOME, suffix)
    updated_dir = os.listdir(dotfiles.HOME)
    assert updated_dir == freeze_dir


def test_broken_symlink(nocolorcapsys):
    """Test that the process can detect a broken symlink and then remove
    it and create a working link.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    install(nocolorcapsys)
    vimrc = os.path.join(dotfiles.HOME, ".vim", "vimrc")
    os.remove(vimrc)  # break link
    install(nocolorcapsys)


@unittest.mock.patch("dotfiles.WINDOWS")
def test_as_windows(mock_windows, nocolorcapsys):
    """Test that the method to install the files is to copy rather than
    symlink for Windows.

    :param mock_windows:    Mock the ``WINDOWS`` constant to always
                            return True
    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    mock_windows.return_value = True
    out = install(nocolorcapsys)
    assert "[COPYING]" in out


@unittest.mock.patch("dotfiles.WINDOWS")
def test_output_windows(mock_windows, nocolorcapsys):
    """Test that the actual output informing the user of the process
    matches the expected output.

    :param mock_windows:    Mock the ``WINDOWS`` constant to always
                            return True
    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    mock_windows.return_value = True
    out = install(nocolorcapsys)
    assert out == expected.output(dotfiles.HOME)


@unittest.mock.patch("dotfiles.WINDOWS")
def test_copies_windows(mock_windows, nocolorcapsys):
    """Test that the copies exist after installing.

    :param mock_windows:    Mock the ``WINDOWS`` constant to always
                            return True
    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    mock_windows.return_value = True
    install(nocolorcapsys)
    contents = os.listdir(dotfiles.HOME)
    for _, val in expected.PAIRS.items():
        if val in expected.FOLLOW_PATH:
            path = os.path.join(dotfiles.HOME, val)
            assert os.path.isfile(path)
        else:
            assert val in contents
