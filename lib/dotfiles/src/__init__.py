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
    def __init__(self, path, obj=None):
        super().__init__()
        self.path = path
        self.dir = os.path.dirname(path)
        self.exists = os.path.isfile(self.path)
        self.dict = obj if obj else {}

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
        color.red.print(str(err), file=sys.stderr)
        raise err

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
