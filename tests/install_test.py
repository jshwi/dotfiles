"""
tests.install_test.py
==============
"""
import os
import sys

import dotpy
import pytest

from . import expected


def install(nocolorcapsys):
    """Run the install process and return it's output stripped of any
    ANSI escaped color codes. The returned output can be used or ignored
    to control the stream of stdout/ stderr.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :return:                Stdout.
    """
    dotpy.install.main()
    return nocolorcapsys.stdout()


def test_clone_self(dotclone):
    # testing above fixture
    vimrc_link = os.path.join(dotclone, "src", "vim", "vimrc")
    assert os.path.isdir(dotclone)
    dotpy.install.main()
    assert os.path.islink(vimrc_link)


def test_locations(nocolorcapsys):
    install(nocolorcapsys)


def test_config_loaded_correctly(nocolorcapsys):
    install(nocolorcapsys)
    install(nocolorcapsys)


def test_output(nocolorcapsys):
    """Test that the actual output informing the user of the process
    matches the expected output.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :return:                Stdout.
    """
    out = install(nocolorcapsys)
    assert out == expected.output(dotpy.install.HOME)


def test_symlinks(nocolorcapsys):
    """Test that the process has created all symlinks. This will also
    ensure no symlinks are broken.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    install(nocolorcapsys)
    contents = os.listdir(dotpy.install.HOME)
    for _, val in expected.PAIRS.items():
        if val in expected.FOLLOW_PATH:
            path = os.path.join(dotpy.install.HOME, val)
            assert os.path.islink(path)
        else:
            assert val in contents


@pytest.mark.usefixtures("dotclone")
def test_backups(tmpdir, dotclone, nocolorcapsys, suffix):
    """Test that the actual output informing the user of the process,
    including the backing up of files, matches the expected output.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :param suffix:          The time suffix fixture to be appended to
                            the file taken from the ``dotpy.SUFFIX``
                            constant so as to ensure a match.
    """
    test_output(nocolorcapsys)
    out = install(nocolorcapsys)
    assert out == expected.backups(tmpdir, suffix)


def test_dry_run(nocolorcapsys):
    """Test that the actual output informing the user of the process,
    including the notice that this is a dry-run, matches the expected
    output. Also ensure that no files were changed, created, or removed
    by comparing a before and after.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    sys.argv.append("--dry")
    freeze_dir = os.listdir(dotpy.install.HOME)
    out = install(nocolorcapsys)
    assert out == expected.dry_run(dotpy.install.HOME)
    updated_dir = os.listdir(dotpy.install.HOME)
    assert updated_dir == freeze_dir


@pytest.mark.usefixtures("dotclone")
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
    freeze_dir = os.listdir(dotpy.install.HOME)
    out = install(nocolorcapsys)
    assert out == expected.dry_run_backups(dotpy.install.HOME, suffix)
    updated_dir = os.listdir(dotpy.install.HOME)
    assert updated_dir == freeze_dir


@pytest.mark.usefixtures("dotclone")
def test_broken_symlink(nocolorcapsys):
    """Test that the process can detect a broken symlink and then remove
    it and create a working link.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    install(nocolorcapsys)
    vimrc = os.path.join(dotpy.install.HOME, ".vim", "vimrc")
    os.remove(vimrc)  # break link
    install(nocolorcapsys)
