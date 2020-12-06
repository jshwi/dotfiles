"""
lib.make.pyshared
=================
===

Classes and functions shared amongst the Python make tool entry points.
"""
import argparse
import hashlib
import os
import pathlib
import subprocess
import sys

REPOPATH = os.environ.get("REPOPATH", None)
REQUIREMENTS = os.environ.get("REQUIREMENTS", None)
LOCKPATH = os.environ.get("LOCKPATH", None)
READMEPATH = os.environ.get("READMEPATH", None)
DOCS = os.environ.get("DOCS", None)
WHITELIST = os.environ.get("WHITELIST", None)
SETUP = os.environ.get("SETUP", None)
TESTS = os.environ.get("TESTS", None)


class TextIO:
    """Input / output for the selected path."""

    def __init__(self, path):
        self.path = path
        self.lines = []
        self.read()

    def read(self):
        """read files into buffer."""
        if os.path.isfile(self.path):
            with open(self.path) as file:
                fin = file.read()
                self.lines.extend(fin.splitlines())

    def sort(self):
        """Sort the list of lines from file."""
        self.lines = sorted(self.lines)

    def write(self, *lines):
        """Write list to file, overwriting any text that is already
        written.

        :param lines: Tuple of strings
        """
        if lines:
            self.lines = list(lines)
        with open(self.path, "w") as file:
            for line in self.lines:
                file.write(f"{line}\n")

    def append(self, *lines):
        """write buffer back to file after any text that is already
        written.

        :param lines: Tuple of strings
        """
        self.lines.extend(lines)
        self.write()

    def deduplicate(self):
        """Remove duplicate entries in list."""
        newlines = []
        for line in self.lines:
            if line not in newlines:
                newlines.append(line)
        self.lines = newlines


class EditTitle(TextIO):
    """Take the ``path`` and ``replace`` argument from the commandline
    and reformat the README whilst returning the original title to
    the parent process.

    :param path:    Path to the ``README.rst`` file.
    :param replace: String to replace the readme title with.
    """

    def __init__(self, path, replace):
        super().__init__(path)
        self.path = path
        self.replace = replace
        self.underline = len(replace) * "="
        self.title = None

    def read_file(self):
        """Read the ``README.rst`` file. Keep the original title.

        Replace the original title and underline with the new
        ``replace provided``.
        """
        self.title = self.lines[0]
        self.lines[0] = self.replace
        self.lines[1] = self.underline

    def replace_title(self):
        """Read, save the old title as an instance attribute, replace
        and write.
        """
        self.read_file()
        self.write()


class MaxSizeList(list):
    """A ``list`` object that can only hold a maximum of the number
    supplied to ``maxlen``.

    :param maxlen: The maximum length of the ``list`` object.
    """

    def __init__(self, maxlen):
        super().__init__()
        self._maxlen = maxlen

    def append(self, element):
        """Append to ``list`` object - handle the maximum it can hold.
        If the maximum is reached remove the oldest element.

        :param element: Element to append to ``list``.
        """
        self.__delitem__(slice(0, len(self) == self._maxlen))
        super().append(element)


class HashCap:
    """Analyze hashes for before and after. ``self.snapshot``, the
    ``list`` object, only holds a maximum of two snapshots for before
    and after.

    :param path: The path of the file to hash.
    """

    def __init__(self, path):
        self.path = path
        self.snapshot = MaxSizeList(maxlen=2)

    def hash_file(self):
        """Open the files and inspect it to get its hash. Return the
        hash as a string.
        """
        with open(self.path, "rb") as lines:
            # noinspection InsecureHash
            md5_hash = hashlib.md5(lines.read())
            self.snapshot.append(md5_hash.hexdigest())

    def compare(self):
        """Compare two hashes in the ``snapshot`` list.

        :return:    Boolean: True for both match, False if they don't.
        """
        return self.snapshot[0] == self.snapshot[1]


def iter_repo(path):
    """Trawl through the project directories to find the dirname
    containing ``__main__.py``

    :param path:    The first path argument parsed with
                    ``argparse.ArgumentParser`` from the commandline and
                    then all built paths following through recursion
                    when this function calls itself
    :return:        A directory name which contains ``__main__.py`` or
                    ``None``
    """
    items = os.listdir(path)
    if "__main__.py" in items or "__init__.py" in items:
        return path
    for item in items:
        subpath = os.path.join(path, item)
        if os.path.isdir(subpath):
            returned_path = iter_repo(subpath)
            if returned_path:
                return os.path.basename(returned_path)
    return None


def get_name(echo=True):
    """Get the name of the directory holding ``__main__.py`` or ``None``
    in which case return an exit-code of `1'

    To be used in conjunction which shell scripts so ``echo`` the output
    with print so it can be collected with ``bash``
    """
    with open(SETUP) as file:
        fin = file.read()
    lines = fin.splitlines()
    for line in lines:
        if "__name__" in line:
            value = line.split("=")[1].strip().replace('"', "")
            if echo:
                print(value)
            return value
    return None


def get_path(echo=True):
    """Get the path to the current repository package.

    :param echo:    This is True when being run by a shell script to
                    treat as a return.
    :return:        The path to the package or sys.exit if it fails.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        default=[],
        help="exclude from search for path",
    )
    args = parser.parse_args()
    name = get_name(echo=False)
    path = pathlib.Path(REPOPATH)
    pathlist = [
        p for s in path.parts for p in path.rglob(name) if s in args.exclude
    ]
    if pathlist:
        item = pathlist[0]
        if echo:
            print(item)
        return item
    sys.exit(1)


def announce(hashcap, filename):
    """Announce whether whitelist.py needed to be updated or not.

    :param hashcap:     Instantiated ``HashCap`` object containing
                        the ``snapshot`` list of file hashes.
    :param filename:    Name of the file without the preceding paths.
    """
    file = os.path.basename(filename)
    output = f"created `{file}'"
    if hashcap.snapshot:
        output = f"updated `{file}'"
        hashcap.hash_file()
        match = hashcap.compare()
        if match:
            output = f"`{file}' is already up to date"
    print(output)


def pipe_command(command, *args):
    """Run a command and return the piped output.

    :param command: Command, as ``str``, to execute - find path with
                    ``shutil.which``.
    :param args:    Args to be run by the command.
    :return:        Output piped from the command as a ``str`` object.
    """
    process = subprocess.Popen([command, *args], stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    return stdout.decode().splitlines()


def make_requirements():
    """Create or update and then format ``requirements.txt`` from
    ``Pipfile.lock``.
    """
    print(f"updating `{REQUIREMENTS}'")
    hashcap = HashCap(REQUIREMENTS)
    if os.path.isfile(REQUIREMENTS):
        hashcap.hash_file()

    # get the stdout for both production and development packages
    stdout = pipe_command("pipfile2req", LOCKPATH)
    stdout += pipe_command("pipfile2req", "--dev", LOCKPATH)

    # write to file and then use sed to remove the additional
    # information following the semi-colon
    reqpathio = TextIO(REQUIREMENTS)
    reqpathio.write(*stdout)
    reqpathio.sort()
    reqpathio.deduplicate()
    reqpathio.write()
    # noinspection SubprocessShellMode
    subprocess.call("sed -i 's/;.*//' " + REQUIREMENTS, shell=True)
    announce(hashcap, REQUIREMENTS)


def make_title():
    """Replace the <PACKAGENAME> title in ``README.rst`` with README
    for rendering ``Sphinx`` documentation links.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--replace", action="store", help="replacement title"
    )
    args = parser.parse_args()
    edit = EditTitle(READMEPATH, args.replace)
    edit.replace_title()
    print(edit.title)


class Index:
    """Get all the directories in the notebook repository as a list
    object of all absolute paths

    :param root:        The root directory which the class will walk
    """

    def __init__(self, root):
        self._root = root
        self.file_paths = []

    def walk_files(self, root, files):
        """Walk through the notes directory structure and perform
        variable actions on directory files specifically

        :param root:    Top level of directory structure
        :param files:   List of files within directory structure
        """
        for file in files:
            fullpath = os.path.join(root, file)
            if fullpath.endswith(".py") and os.path.basename(fullpath) not in (
                "__main__.py",
                "__init__.py",
            ):
                module = fullpath.replace(os.sep, ".").replace(".py", "")
                self.file_paths.append(module)

    def walk_dirs(self):
        """Iterate through walk if the root directory exists

        - Skip directories in list parameter and create fullpath
          with root and files
        - forget about the directories returned by walk
        - Once files are determined perform the required actions
        """
        if os.path.isdir(self._root):
            for root, _, files in os.walk(self._root):
                self.walk_files(root, files)


def make_toc():
    """Make the docs/<PACKAGENAME>.rst file from the package src."""
    packagename = os.path.basename(REPOPATH)
    package = get_name(echo=False)
    package = package if package else packagename
    mastertoc = package + ".rst"
    tocpath = os.path.join(DOCS, mastertoc)
    srcpath = os.path.join(REPOPATH, package)

    print(f"updating `{os.path.join(DOCS, mastertoc)}'")
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


def make_whitelist():
    """Prepend a line before every lines in a file."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        help="files to scan for vulture's whitelist.py",
    )
    args = parser.parse_args()
    print(f"updating `{WHITELIST}'")
    stdout = []
    hashcap = HashCap(WHITELIST)
    pathio = TextIO(WHITELIST)
    if os.path.isfile(WHITELIST):
        hashcap.hash_file()

    # append whitelist exceptions for each individual module
    for item in args.files:
        if os.path.exists(item):
            stdout.extend(pipe_command("vulture", item, "--make-whitelist"))

    # merge the prepended PyInspection line to the beginning of every
    # entry
    lines = [line.strip() for line in stdout if line != ""]

    # clear contents of instantiated `TextIO' object to write a new file
    # and not append
    pathio.write(*lines)
    announce(hashcap, WHITELIST)


def check_tests():
    """Check that tests exist in the test dir or otherwise exit with a
    non-zero exit code.
    """
    files = []
    for pattern in ("test_*.py", "*_test.py"):
        path = pathlib.Path(TESTS)
        files.extend(path.rglob(pattern))
    if not files:
        sys.exit(1)
