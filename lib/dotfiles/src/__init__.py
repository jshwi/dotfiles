"""
dotfiles.src.__init__
======================
"""
import datetime
import errno
import os
import pathlib
import shutil
import subprocess
import sys
import tarfile

import appdirs
import object_colors
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
GNUPG_PASSPHRASE = os.environ.get("GNUPG_PASSPHRASE", "")
HOME = str(pathlib.Path.home())
SOURCE = str(pathlib.Path.home() / ".dotfiles" / "src")
SUFFIX = datetime.datetime.now().strftime("%d%m%YT%H%M%S")
TIME = datetime.datetime.now().strftime("%H:%M:%S")

color = object_colors.Color()

color.populate_colors()


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


class Yaml:
    """Read from or write to yaml config files.

    :param path:    Path to yaml file to be created or to be read from.
    :param obj:     Dictionary object to write to yaml file.
    """

    def __init__(self, path, obj=None):
        super().__init__()
        self.path = path
        self.dir = os.path.dirname(path)
        self.exists = os.path.isfile(self.path)
        self.dict = obj if obj else {}

    def write(self):
        """Write ``self.dict`` dictionary object to yaml."""
        if os.path.isdir(self.dir):
            with open(self.path, "w") as fout:
                yaml.dump(self.dict, fout)
            self.exists = True

    def read(self):
        """Read from existing yaml file into session dictionary."""
        if self.exists:
            with open(self.path) as fin:
                self.dict.update(yaml.safe_load(fin))


class Tar:
    """Compress and extract tar archives.

    :param infile:  The file or dir that will be compressed or
                    extracted.
    :param outfile: The file or dir that the infile will be compressed
                    into or extracted into.
    """

    def __init__(self, infile, outfile=None):
        self.infile = infile
        self.outfile = outfile

    @staticmethod
    def _file_not_found(file):
        err = FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)
        color.red.print(str(err), file=sys.stderr)
        raise err

    def compress(self):
        """Compress file or dir to tar.gz file"""
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
        """Extract a tar.gz archive."""
        outfile_dirname = os.path.dirname(self.outfile)
        with tarfile.open(self.infile) as tar:
            tar.extractall(path=outfile_dirname)


class GPG:
    """Encrypt and decrypt *.gpg files.

    :param infile:  File to encrypt or file to decrypt.
    :param outfile: File for infile to encrypt into or file for it to
                    decrypt into.
    """

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
        """Encrypt a file.

        :param recipient:   The gpg recipient key-holder who's private
                            key can decrypt these files.
        :return:            Exit code from command.
        """
        return self.popen(
            ["gpg", "-o", self.outfile, "-r", recipient, "-e", self.infile]
        )

    def decrypt(self):
        """Decrypt encrypted file if recipient key-holder.

        :return: Exit code from command.
        """
        return self.popen(["gpg", "-o", self.outfile, "-d", self.infile])

    @classmethod
    def add_batch_key(cls, keyfile):
        """Create a dummy .gnupg dir and keyrings for tests related to
        gpg keys

        :param keyfile: Path to keyfile to read from.
        """
        return cls.popen(["gpg", "--batch", "--gen-key", keyfile])


class CryptDir:
    """Thin wrapper combining ``Tar`` and ``GPG`` to automate the task
    of encrypting files and dirs (especially dirs).

    :param infile: Pre-process file-name.
    :param outfile: Post-process file-name
    """

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def _announce_rename(self):
        print(". " + self.outfile + " -> " + self.outfile)

    def compress(self):
        """Compress the item and announce."""
        tar = Tar(self.infile, self.outfile)
        print("Compressing " + self.infile)
        tar.compress()
        self._announce_rename()

    def encrypt(self, recipient):
        """Encrypt the item and announce."""
        gpg = GPG(self.infile, self.outfile)
        print("Encrypting " + self.infile)
        exit_status = gpg.encrypt(recipient)
        if exit_status:
            sys.exit(exit_status)
        self._announce_rename()

    def extract(self):
        """Extract the item and announce."""
        tar = Tar(self.infile, self.outfile)
        print("Extracting " + self.infile)
        tar.extract()
        self._announce_rename()

    def decrypt(self):
        """Decrypt the item and announce."""
        gpg = GPG(self.infile, self.outfile)
        print("Decrypting " + self.infile)
        exit_status = gpg.decrypt()
        if exit_status:
            sys.exit(exit_status)
        self._announce_rename()


class Cleanup(CryptDir):
    def __init__(self, infile, outfile):  # pylint: disable=W0235
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
    """Get the directory information of added archive paths for
    ``mkarchive``.

    :param path: Path to the archive.
    """

    def __init__(self, path):
        self.list = path.split(os.sep)[1:]
        self.old = f"/{self.list.pop(0)}"
        self.new = None

    def _build_new_path(self, _dir):
        if self.new is not None:
            return os.path.join(self.new, _dir)
        return _dir

    def collate_info(self):
        """Gather the info from the lists and determine if an archive
        path has already been created or not.
        """
        for _dir in self.list:
            test_dir = os.path.join(self.old, _dir)
            if os.path.isdir(test_dir):
                self.old = test_dir
            else:
                self.new = self._build_new_path(_dir)

    def get_info(self):
        """:return: the old and new directories"""
        return self.old, self.new
