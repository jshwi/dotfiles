import os

import pyshared
import pytest


@pytest.fixture(name="pyshared_constants", autouse=True)
def fixture_pyshared_constants(dotclone):
    pyshared.REPOPATH = dotclone
    pyshared.SETUP = os.path.join(dotclone, "setup.py")
