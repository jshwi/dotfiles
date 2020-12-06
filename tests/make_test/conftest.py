"""
tests.make_test.conftest
========================
"""
import os

import pyshared

# noinspection PyPackageRequirements
import pytest


@pytest.fixture(name="pyshared_constants", autouse=True)
def fixture_pyshared_constants(dotclone):
    """Mock the path of setup.py to point to the cloned version of this
    repository.

    :param dotclone:    Clone this repository and return the path
                        (pointed to the tmpdir).
    """
    pyshared.REPOPATH = dotclone
    pyshared.SETUP = os.path.join(dotclone, "setup.py")
