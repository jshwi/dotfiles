"""
tests.makefile_test.conftest
========================
"""
import os

import makefile.src

# noinspection PyPackageRequirements
import pytest


@pytest.fixture(name="makefile_constants", autouse=True)
def fixture_makefile_constants(repoclone):
    """Mock the path of setup.py to point to the cloned version of this
    repository.

    :param repoclone:    Clone this repository and return the path
                        (pointed to the tmpdir).
    """
    makefile.src.REPOPATH = repoclone
    makefile.src.SETUP = os.path.join(repoclone, "setup.py")
    makefile.src.DOCS = os.path.join(repoclone, "docs")
