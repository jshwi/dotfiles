"""
dotpy.src.__init__
==================
"""
import datetime
import errno
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
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
DOTFILES = str(pathlib.Path.home() / ".dotfiles")
SOURCE = str(pathlib.Path.home() / ".dotfiles" / "src")
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


class Colors:
    """Return strings in color.
    :var: black
    :var: red
    :var: green
    :var: yellow
    :var: blue
    :var: magenta
    :var: cyan
    :var: white
    """

    codes = {
        "black": 0,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
    }

    def __init__(self, color="white"):
        try:
            self.color = self.codes[color]
        except KeyError:
            self.color = self.codes["white"]

    def get(self, string):
        """Get a list of strings if there are multiple strings or just
        return the single string if there is only one.

        :param string:  String(s) to color.
        :return:        Single colored string or a list of colored
                        strings.
        """
        return f"\u001b[0;3{self.color};40m{string}\u001b[0;0m"

    def print(self, string, **kwargs):
        print(self.get(string), **kwargs)


class EnterDir:
    """Change to the selected directory entered as an argument and when
    actions are complete return to the previous directory

    :param new_path: Enter the directory to temporarily change to
    """

    def __init__(self, new_path):
        self.saved_path = os.getcwd()
        self.enter_path = os.path.expanduser(new_path)

    def __enter__(self):
        os.chdir(self.enter_path)

    def __exit__(self, _, value, __):
        os.chdir(self.saved_path)


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


class Tar:
    def __init__(self, infile, outfile=None):
        self.infile = infile
        self.outfile = outfile

    @staticmethod
    def _file_not_found(file):
        err = FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)
        Colors("red").print(str(err))
        sys.exit(1)

    def compress(self):

        if os.sep in self.infile:
            dirname = os.path.dirname(self.infile)
        else:
            dirname = os.getcwd()

        basename = os.path.basename(self.infile)

        if not os.path.isdir(dirname):
            self._file_not_found(dirname)

        with EnterDir(dirname):
            with tarfile.open(self.outfile, "w:gz") as tar:
                if os.path.isdir(basename):
                    for file in os.listdir(basename):
                        tar.add(os.path.join(basename, file))

                elif os.path.isfile(basename):
                    tar.add(basename)

                else:
                    self._file_not_found(self.infile)

    def extract(self):
        outfile_dirname = os.path.dirname(self.outfile)
        with tarfile.open(self.infile) as tar:
            tar.extractall(path=outfile_dirname)


class GPG:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    @staticmethod
    def popen(command):
        child = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        try:
            for line in iter(child.stdout.readline, ""):
                line = line.decode()
                if line == "":
                    return 0
                sys.stdout.flush()
                print(line.rstrip())
                sys.stdout.flush()
        except TypeError:
            sys.stdout.flush()
        return child.returncode

    def encrypt(self, recipient):
        return self.popen(
            ["gpg", "-o", self.outfile, "-r", recipient, "-e", self.infile]
        )

    def decrypt(self):
        return self.popen(["gpg", "-o", self.outfile, "-d", self.infile])

    @classmethod
    def add_batch_key(cls, keyfile):
        """Create a dummy .gnupg dir and keyrings for tests related to
        gpg keys
        """
        return cls.popen(["gpg", "--batch", "--gen-key", keyfile])


class CryptDir:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def _announce_rename(self):
        print(". " + self.outfile + " -> " + self.outfile)

    def compress(self):
        tar = Tar(self.infile, self.outfile)
        print("Compressing " + self.infile)
        tar.compress()
        self._announce_rename()

    def encrypt(self, recipient):
        gpg = GPG(self.infile, self.outfile)
        print("Encrypting " + self.infile)
        exit_status = gpg.encrypt(recipient)
        if exit_status:
            sys.exit(exit_status)
        self._announce_rename()

    def extract(self):
        tar = Tar(self.infile, self.outfile)
        print("Extracting " + self.infile)
        tar.extract()
        self._announce_rename()

    def decrypt(self):
        gpg = GPG(self.infile, self.outfile)
        print("Decrypting " + self.infile)
        exit_status = gpg.decrypt()
        if exit_status:
            sys.exit(exit_status)
        self._announce_rename()


class Cleanup(CryptDir):
    def __init__(self, infile, outfile):
        super().__init__(infile, outfile)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Removing " + self.infile)
        try:
            shutil.rmtree(self.infile)
        except NotADirectoryError:
            os.remove(self.infile)
        print(". removed " + self.infile)


class DirInfo:
    def __init__(self, path):
        self.list = path.split(os.sep)[1:]
        self.old = f"/{self.list.pop(0)}"
        self.new = None

    def _build_new_path(self, _dir):
        if self.new is not None:
            return os.path.join(self.new, _dir)
        return _dir

    def collate_info(self):
        for _dir in self.list:
            test_dir = os.path.join(self.old, _dir)
            if os.path.isdir(test_dir):
                self.old = test_dir
            else:
                self.new = self._build_new_path(_dir)

    def get_info(self):
        return self.old, self.new
