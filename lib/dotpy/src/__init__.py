"""
dotpy.src.__init__
==================
"""
import datetime
import hashlib
import os
import pathlib
import subprocess
import tarfile

import appdirs
import yaml

CONFIGDIR = appdirs.user_config_dir(__name__)
CONFIG = os.path.join(CONFIGDIR, __name__ + ".yaml")
DATE = datetime.date.today().strftime("%Y/%m/%d")
DOTCONTENTS = dict(
    dirs={
        "~/.": {
            "bash": ["bashrc", "bash_profile"],
            "dir_colors.d": ["dir_colors"],
            "gem": ["gemrc"],
            "git.d": ["gitconfig"],
            "hidden.d": ["hidden"],
            "neomutt": ["neomuttrc"],
            "vim": ["vimrc"],
            "zsh": ["zshrc"],
        },
    },
    files={
        "~/.config/Code/User/": [
            "vscode.d/settings.json",
            "vscode.d/keybindings.json",
        ],
    },
)
PACKAGE = os.path.dirname(os.path.realpath(__file__))
PYLIB = os.path.dirname(PACKAGE)
LIB = os.path.dirname(PYLIB)
REPOPATH = os.path.dirname(LIB)
DOCS = os.path.join(REPOPATH, "docs")
GNUPG_PASSPHRASE = os.environ.get("GNUPG_PASSPHRASE", "")
HOME = str(pathlib.Path.home())
PIPFILELOCK = "Pipfile.lock"
LOCKPATH = os.path.join(REPOPATH, PIPFILELOCK)
PACKAGENAME = os.path.basename(REPOPATH)
README = "README.rst"
READMEPATH = os.path.join(REPOPATH, README)
REQUIREMENTS = "requirements.txt"
REQPATH = os.path.join(REPOPATH, REQUIREMENTS)
SUFFIX = datetime.datetime.now().strftime("%d%m%YT%H%M%S")
TIME = datetime.datetime.now().strftime("%H:%M:%S")
WHITELIST = "whitelist.py"
WHITELISTPATH = os.path.join(REPOPATH, WHITELIST)


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


class Tar:
    def __init__(self, file, archive):
        self.file = file
        self.archive = archive

    def _compress_dir(self, tar):
        dircontents = [
            os.path.join(self.file, i) for i in os.listdir(self.file)
        ]

        for content in dircontents:
            tar.add(content)

    def compress(self):
        with tarfile.open(self.archive, "w:gz") as tar:

            if os.path.isdir(self.file):
                self._compress_dir(tar)

            elif os.path.isfile(self.file):
                tar.add(self.file)

    def extract(self):
        with tarfile.open(self.archive) as tar:
            tar.extractall()


class Yaml:
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.dir = os.path.dirname(path)
        self.exists = os.path.isfile(self.path)
        self.dict = {}

    def write(self):
        if os.path.isdir(self.dir):
            with open(self.path, "w") as fout:
                yaml.dump(self.dict, fout)
            self.exists = True

    def read(self):
        if self.exists:
            with open(self.path) as fin:
                self.dict.update(yaml.safe_load(fin))
