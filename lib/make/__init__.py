#!/usr/bin/env python3
"""
dev
===

Tools to help manage Python repos
"""
import argparse
import hashlib
import os
import subprocess

__author__ = "Stephen Whitlock"
__email__ = "stephen@jshwisolutions.com"
__copyright__ = "2020, Stephen Whitlock"
__license__ = "MIT"
__version__ = "1.0.0"

MAKELIB = os.path.dirname(os.path.realpath(__file__))
LIB = os.path.dirname(MAKELIB)
REPOPATH = os.path.dirname(LIB)

PIPFILELOCK = os.path.join(REPOPATH, "Pipfile.lock")
README = os.path.join(REPOPATH, "README.rst")
REQUIREMENTS = os.path.join(REPOPATH, "requirements.txt")
WHITELIST = os.path.join(REPOPATH, "whitelist.py")
DOCS = os.path.join(REPOPATH, "docs")
LOCKPATH = os.path.join(REPOPATH, PIPFILELOCK)
PACKAGENAME = os.path.basename(REPOPATH)
READMEPATH = os.path.join(REPOPATH, README)
REQPATH = os.path.join(REPOPATH, REQUIREMENTS)
WHITELISTPATH = os.path.join(REPOPATH, WHITELIST)


class Parse(argparse.ArgumentParser):
    """Parse commandline arguments.

    :param choices: List of function choices.
    """

    def __init__(self, choices):
        # noinspection PyTypeChecker
        super().__init__(
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=55
            ),
        )

        self.choices = choices
        self._add_arguments()
        self.args = self.parse_args()
        self.choice = self.args.choice[0]

    def _add_arguments(self):
        """Arguments needed for this module."""
        self.add_argument(
            "choice",
            nargs="+",
            choices=self.choices,
            help="choice of function",
        )
        self.add_argument(
            "-r", "--replace", action="store", help="replacement title"
        )
        self.add_argument(
            "-f",
            "--files",
            nargs="+",
            help="files to scan for vulture's whitelist.py",
        )
        self.add_argument(
            "-e",
            "--executable",
            action="store",
            help="path to venv executable",
        )


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


def announce(hashcap, filename):
    """Announce whether whitelist.py needed to be updated or not.

    :param hashcap:     Instantiated ``HashCap`` object containing
                        the ``snapshot`` list of file hashes.
    :param filename:    Name of the file without the preceding paths.
    """
    output = f"created `{filename}'"
    if hashcap.snapshot:
        output = f"updated `{filename}'"
        hashcap.hash_file()
        match = hashcap.compare()
        if match:
            output = f"`{filename}' is already up to date"
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


def make_requirements(args):
    """Create or update and then format ``requirements.txt`` from
    ``Pipfile.lock``.
    """
    print(f"updating `{REQUIREMENTS}'")
    hashcap = HashCap(REQUIREMENTS)
    if os.path.isfile(REQUIREMENTS):
        hashcap.hash_file()

    # get the stdout for both production and development packages
    stdout = pipe_command(args.executable, LOCKPATH)
    stdout += pipe_command(args.executable, "--dev", LOCKPATH)

    # write to file and then use sed to remove the additional
    # information following the semi-colon
    reqpathio = TextIO(REQPATH)
    reqpathio.write(*stdout)
    reqpathio.sort()
    reqpathio.deduplicate()
    reqpathio.write()
    # noinspection SubprocessShellMode
    subprocess.call("sed -i 's/;.*//' " + REQPATH, shell=True)
    announce(hashcap, REQUIREMENTS)


def make_title(args):
    """Replace the <PACKAGENAME> title in ``README.rst`` with README
    for rendering ``Sphinx`` documentation links.

    :param args: ``argparse`` ``Namespace`` object.
    """
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
    package = get_name(echo=False)
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


def make_whitelist(args):
    """Prepend a line before every lines in a file.

    :param args: ``argparse`` ``Namespace`` object.
    """
    print(f"updating `{WHITELIST}'")
    stdout = []
    hashcap = HashCap(WHITELISTPATH)
    pathio = TextIO(WHITELISTPATH)
    if os.path.isfile(WHITELISTPATH):
        hashcap.hash_file()

    # append whitelist exceptions for each individual module
    for item in args.files:
        if os.path.exists(item):
            stdout.extend(
                pipe_command(args.executable, item, "--make-whitelist")
            )

    # merge the prepended PyInspection line to the beginning of every
    # entry
    lines = [line.strip() for line in stdout if line != ""]

    # clear contents of instantiated `TextIO' object to write a new file
    # and not append
    pathio.write(*lines)
    announce(hashcap, WHITELIST)


def main():
    """Module entry point. Parse commandline arguments and run the
    selected choice from the dictionary of functions which matches the
    key. If no args can be passed to the function ignore the
    ``TypeError`` and run without.
    """

    choices = {
        "name": get_name,
        "reqs": make_requirements,
        "whitelist": make_whitelist,
        "toc": make_toc,
        "title": make_title,
    }
    parse = Parse(choices.keys())
    try:
        choices[parse.choice](parse.args)
    except TypeError:
        choices[parse.choice]()


if __name__ == "__main__":
    main()
