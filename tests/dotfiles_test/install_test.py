"""
tests.dotfiles_test.install_test.py
===================================
"""
# pylint: disable=R0801
import os
import sys
import unittest.mock

import dotfiles

# noinspection PyPackageRequirements
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
    dotfiles.install.main()
    return nocolorcapsys.stdout()


def test_config_loaded_correctly(nocolorcapsys):
    """Test the config is loaded and running on second invocation of
    this script.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    install(nocolorcapsys)
    install(nocolorcapsys)


def test_output(tmpdir, nocolorcapsys):
    """Test that the actual output informing the user of the process
    matches the expected output.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :return:                Stdout.
    """
    out = install(nocolorcapsys)
    assert out == expected.output(tmpdir)


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


@pytest.mark.usefixtures("dotclone")
def test_backups(tmpdir, nocolorcapsys, suffix):
    """Test that the actual output informing the user of the process,
    including the backing up of files, matches the expected output.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :param suffix:          The time suffix fixture to be appended to
                            the file taken from the ``dotfiles.SUFFIX``
                            constant so as to ensure a match.
    """
    test_output(tmpdir, nocolorcapsys)
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
    freeze_dir = os.listdir(dotfiles.install.HOME)
    out = install(nocolorcapsys)
    assert out == expected.dry_run(dotfiles.install.HOME)
    updated_dir = os.listdir(dotfiles.install.HOME)
    assert freeze_dir == updated_dir


@pytest.mark.usefixtures("dotclone")
def test_dry_run_backups(tmpdir, nocolorcapsys, suffix):
    """Test that the actual output informing the user of the process,
    including the notice that this is a dry-run of a run including
    backups, matches the expected output. Also ensure that no files were
    changed, created, or removed by comparing a before and after.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :param suffix:
    """
    test_output(tmpdir, nocolorcapsys)
    sys.argv.append("--dry")
    freeze_dir = os.listdir(dotfiles.install.HOME)
    out = install(nocolorcapsys)
    assert out == expected.dry_run_backups(dotfiles.install.HOME, suffix)
    updated_dir = os.listdir(dotfiles.install.HOME)
    assert freeze_dir == updated_dir


@pytest.mark.usefixtures("dotclone")
def test_broken_symlink(nocolorcapsys):
    """Test that the process can detect a broken symlink and then remove
    it and create a working link.

    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    install(nocolorcapsys)
    vimrc = os.path.join(dotfiles.install.HOME, ".vim", "vimrc")
    os.remove(vimrc)  # break link
    install(nocolorcapsys)


def get_config(tmpdir):
    """Get the mocked config path.

    :param tmpdir:  The temporary directory ``pytest`` fixture.
    :return:        Path to the mock config file in the tmpdir.
    """
    name = "tests.dotfiles_test.conftest"
    config_dir = os.path.join(tmpdir, ".config", name)
    return os.path.join(config_dir, name + ".yaml")


def test_init_config(tmpdir, nocolorcapsys):
    """Test initialization of a new config file in a brand-new install.

    :param tmpdir:          The temporary directory ``pytest`` fixture.
    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    config = get_config(tmpdir)
    with unittest.mock.patch.object(sys, "argv", [__name__, "--init"]):
        dotfiles.install.main()
        out = nocolorcapsys.stdout()
        assert out == f"created default conf:\n{config}\n"
    assert os.path.isfile(config)


def test_init_config_force(tmpdir, nocolorcapsys):
    """Test initialization of a new config file in an already existing
    installation when using the -f/--force option and test that the old
    config is overwritten.

    :param tmpdir:          The temporary directory ``pytest`` fixture.
    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    """
    config = get_config(tmpdir)
    test_init_config(tmpdir, nocolorcapsys)
    yaml = dotfiles.Yaml(config)
    yaml.read()
    yaml.dict["new_key"] = "new"
    yaml.write()
    with open(config) as fin:
        contents_1 = fin.read()
    with unittest.mock.patch.object(
        sys, "argv", [__name__, "--init", "--force"]
    ):
        dotfiles.install.main()
        out = nocolorcapsys.stdout()
        assert out == f"created default conf:\n{config}\n"
    with open(config) as fin:
        contents_2 = fin.read()
    assert contents_2 != contents_1