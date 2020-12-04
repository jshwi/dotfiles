"""
tests.conftest
==============
"""
import os
import pathlib
import re
import subprocess
import sys

import pytest

import dotpy


class NoColorCapsys:
    """Capsys but with a regex to remove ANSI escape codes

    Class is preferable for this as we can instantiate the instance
    as a fixture that also contains the same attributes as capsys

    We can make sure that the class is instantiated without executing
    capsys immediately thus losing control of what stdout and stderr
    we are to capture

    :param capsys: ``pytest's`` builtin fixture to capture system output
    """

    def __init__(self, capsys):
        self.capsys = capsys

    @staticmethod
    def regex(out):
        """Replace ANSI color codes with empty strings i.e. remove all
        escape codes

        Prefer to test colored output this way as colored strings can
        be tricky and the effort in testing their validity really isn't
        worth it. Also hard to read expected strings when they contain
        the codes.

        :param out: String to strip of ANSI escape codes
        :return:    Same string but without ANSI codes
        """
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", out)

    def readouterr(self):
        """Call as capsys ``readouterr`` but regex the strings for
        escape codes at the same time

        :return:    A tuple (just like the capsys) containing stdout in
                    the first index and stderr in the second
        """
        return [self.regex(r) for r in self.capsys.readouterr()]

    def _readouterr_index(self, idx):
        readouterr = self.readouterr()
        return readouterr[idx]

    def stdout(self):
        """Call this to return the stdout without referencing the tuple
        indices
        """
        return self._readouterr_index(0)


@pytest.fixture(name="nocolorcapsys")
def fixture_nocolorcapsys(capsys):
    """Instantiate capsys with the regex method

    :param capsys: ``pytest`` fixture
    :return:        Instantiated ``NoColorCapsys`` object
    """
    return NoColorCapsys(capsys)


@pytest.fixture(name="test_dir")
def fixture_test_dir():
    """Fixture object of the absolute path to this tests dir.

    :return: The dir this file is in.
    """
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(name="repo_dir")
def fixture_repo_dir(test_dir):
    """Get the parent directory, this repo, of this test dir.

    :param test_dir:    The dir this file is in.
    :return:            The absolute path of this repository.
    """
    return os.path.dirname(test_dir)


@pytest.fixture(name="package_dir")
def fixture_package_dir(repo_dir):
    """The absolute path to the ``dotpy`` package.

    :param repo_dir:    The absolute path to this repository.
    :return:            The absolute path to the ``dotpy`` package.
    """
    return os.path.join(repo_dir, "dotpy")


@pytest.fixture(name="entry_point")
def fixture_init_py(package_dir):
    """The absolute path to the __init__.py file in the ``dotpy``
    package.

    :param package_dir: The absolute path to the ``dotpy`` package.
    """
    return os.path.join(package_dir, "__init__.py")


@pytest.fixture(name="dot_constants", autouse=True)
def dot_constants(nocolorcapsys, monkeypatch, tmpdir, entry_point):
    """Run the install process and return it's output stripped of any
    ANSI escaped color codes. The returned output can be used or ignored
    to control the stream of stdout/ stderr.

    :param entry_point:
    :param tmpdir:
    :param monkeypatch:
    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :return:                Stdout.
    """

    def expanduser(path):
        return path.replace("~/.", f"{tmpdir}/.")

    sys.argv = [entry_point]
    monkeypatch.setattr(dotpy.install.os.path, "expanduser", expanduser)
    dotpy.install.HOME = tmpdir
    dotpy.install.CONFIGDIR = os.path.join(
        dotpy.install.HOME, ".config", __name__
    )
    dotpy.install.CONFIG = os.path.join(
        dotpy.install.CONFIGDIR, __name__ + ".yaml"
    )


@pytest.fixture(name="dotclone")
def fixture_dotclone(tmpdir):
    """Get the path to the mock .dotpy repository clone.

    :param tmpdir:  The temporary directory ``pytest`` fixture.
    :return:        The mock .dotpy repository clone.
    """
    return os.path.join(tmpdir, ".dotfiles")


@pytest.fixture(name="suffix")
def fixture_suffix():
    """Get the accurate timestamp from ``dotpy.SUFFIX`` so that there
    is no discrepancy between the test time and the module's time.

    :return: Timestamp to be appended to backed up files.
    """
    return dotpy.SUFFIX


@pytest.fixture(name="clone_self", autouse=True)
def fixture_clone_self(repo_dir, dotclone):
    """Clone this repository to the temporary dir returned from
    ``tmpdir`` so that tests can be run without effecting this
    repository.

    :param repo_dir:    The absolute path to this repository.
    :param dotclone:    The absolute path to this repository's temporary
                        clone.
    """
    subprocess.call(
        ["git", "clone", repo_dir, dotclone],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


@pytest.fixture(name="mock_vscode_config_dir", autouse=True)
def fixture_mock_vscode_config_dir(tmpdir):
    """Create a replica of the path to the user's local vscode settings
    in the temporary directory and return the path variable.

    :param tmpdir:  The temporary directory ``pytest`` fixture.
    :return:        The path to the temp vscode config dir.
    """
    config_dir = os.path.join(tmpdir, ".config", "Code", "User")
    dir_object = pathlib.Path(config_dir)
    dir_object.mkdir(parents=True, exist_ok=True)
    return config_dir
