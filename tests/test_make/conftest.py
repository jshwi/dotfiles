import os

import pytest
import pyshared


@pytest.fixture(name="pyshared_constants", autouse=True)
def fixture_pyshared_constants(dotclone):
    pyshared.REPOPATH = dotclone
    pyshared.SETUP = os.path.join(dotclone, "setup.py")


@pytest.fixture(name="project_name")
def fixture_project_name():
    with open(pyshared.SETUP) as file:
        fin = file.read()
    lines = fin.splitlines()
    for line in lines:
        if "__name__" in line:
            value = line.split("=")[1].strip().replace('"', "")
            return value
    return None
