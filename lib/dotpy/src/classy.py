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
