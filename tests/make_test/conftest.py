"""
tests.makefile_test.conftest
========================
"""
import os

import makefile

# noinspection PyPackageRequirements
import pytest


@pytest.fixture(name="makefile_constants", autouse=True)
def fixture_makefile_constants(dotclone):
    """Mock the path of setup.py to point to the cloned version of this
    repository.

    :param dotclone:    Clone this repository and return the path
                        (pointed to the tmpdir).
    """
    makefile.REPOPATH = dotclone
    makefile.SETUP = os.path.join(dotclone, "setup.py")
