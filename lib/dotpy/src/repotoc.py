import os

from . import (
    reponame,
    PACKAGENAME,
    DOCS,
    REPOPATH,
    HashCap,
    Index,
    TextIO,
    announce,
)


def main():
    """Make the docs/<PACKAGENAME>.rst file from the package src."""
    package = reponame.main(echo=False)
    package = package if package else PACKAGENAME
    mastertoc = package + ".rst"
    tocpath = os.path.join(DOCS, mastertoc)
    srcpath = os.path.join(REPOPATH, package)

    print(f"updating `{mastertoc}'")
    lines = []
    hashcap = HashCap(tocpath)
    if os.path.isfile(tocpath):
        hashcap.hash_file()

    idx = Index(package)

    idx.walk_dirs()

    # compile a list of modules for Sphinx to document and sort them
    # e.g. [..automodule:: <PACKAGENAME>.src.<MODULE>, ...]
    if os.path.isdir(srcpath):
        files = sorted([f".. automodule:: {i}" for i in idx.file_paths])

        # add the additional toctree properties for each listed module
        lines.extend(
            [
                f
                + "\n"
                + "    :members:\n"
                + "    :undoc-members:\n"
                + "    :show-inheritance:\n"
                for f in files
            ]
        )

    # insert the title and underline and then write to file
    # announce the outcome
    lines.insert(0, f"{package}\n{len(package) * '='}\n")
    if lines[-1][-1] == "\n":
        lines.append(lines.pop().strip())
    rstio = TextIO(tocpath)
    rstio.write(*lines)
    announce(hashcap, mastertoc)
