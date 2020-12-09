"""
tests.conftest
==============
"""
import os
import pathlib
import re
import subprocess

import pytest

TESTS = os.path.abspath(os.path.dirname(__file__))
REPOPATH = os.path.dirname(TESTS)


class NoColorCapsys:
    """Capsys but with a regex to remove ANSI escape codes

    Class is preferable for this as we can instantiate the instance
    as a fixture that also contains the same attributes as capsys

    We can make sure that the class is instantiated without executing
    capsys immediately thus losing control of what stdout and stderr
    we are to capture

    :param capsys: ``pytest`` builtin fixture to capture system output
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

    def stderr(self):
        """Call this to return the stderr without referencing the tuple
        indices
        """
        return self._readouterr_index(1)


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


@pytest.fixture(name="repoclone", autouse=True)
def fixture_repoclone(tmpdir, repo_dir):
    """Clone this repository to the temporary dir returned from
    ``tmpdir`` so that tests can be run without effecting this
    repository.

    :param tmpdir:      The temporary directory ``pytest`` fixture.
    :param repo_dir:    The absolute path to this repository.
    """
    repoclone = os.path.join(tmpdir, os.path.basename(REPOPATH))
    command = ["git", "clone", repo_dir, repoclone]
    if not os.path.isdir(repoclone):
        subprocess.call(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    return repoclone
