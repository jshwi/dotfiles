import os

from . import REPOPATH


def main(echo=True):
    """Get the name of the directory holding ``__main__.py`` or ``None``
    in which case return an exit-code of `1'

    To be used in conjunction which shell scripts so ``echo`` the output
    with print so it can be collected with ``bash``
    """
    setup = os.path.join(REPOPATH, "setup.py")
    with open(setup) as file:
        fin = file.read()
    lines = fin.splitlines()
    for line in lines:
        if "__name__" in line:
            value = line.split("=")[1].strip().replace('"', "")
            if echo:
                print(value)
            return value
    return None
