"""
dotfiles.__init__
=================
"""
import argparse
import datetime
import os
import pathlib
import shutil
import subprocess
import sys

PACKAGE = os.path.abspath(os.path.dirname(__file__))
REPO = os.path.dirname(PACKAGE)
SOURCE = os.path.join(REPO, "src")
HOME = str(pathlib.Path.home())
SUFFIX = datetime.datetime.now().strftime("%d%m%YT%H%M%S")
WINDOWS = os.name == "nt"


class Colors:
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

    def __init__(self, color):
        self.color = self.codes[color]

    def get_tuple(self, *args):
        return [f"\u001b[0;3{self.color};40m{arg}\u001b[0;0m" for arg in args]

    def get(self, *args):
        result = self.get_tuple(*args)
        return result[0] if len(result) == 1 else result


class Parser(argparse.ArgumentParser):
    """Get help or add ``--dry`` argument to the process"""

    def __init__(self):
        super().__init__(
            prog=Colors("cyan").get("./install"),
            description=(
                'symlinks "$HOME" dotfiles and '
                "backs up any files that have the same name"
            ),
        )
        self._add_arguments()
        self._args = self.parse_args()
        self.dry = self._args.dry

    def _add_arguments(self):
        self.add_argument(
            "-d",
            "--dry",
            action="store_true",
            help="see what actions would take place",
        )


class DevNull:
    def __init__(self):
        self.stdout = sys.stdout

    @staticmethod
    def write(*args):
        """pass to suppress stdout"""
        pass

    def __enter__(self):
        sys.stdout = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.stdout


def source_file(src, dst):
    with open(dst, "w") as file:
        if os.path.basename(src) == "bashrc":
            src = os.path.join(os.path.dirname(src), "bashrc.d", "bashrc.win")
        src = src.replace(os.sep, "/")
        file.write(f"source {src}")


def link(src, dst):
    """For Unix-like systems where symlinks do not require elevated
    privilege this is the preferred option.

    :param src: The file in this repository
    :param dst: The symlink's path
    """
    source = [
        "bashrc",
        "bash_profile",
        "dir_colors",
        "neomuttrc",
        "vimrc",
        "zshrc",
    ]
    if WINDOWS:
        if os.path.isfile(src):
            if os.path.basename(src) in source:
                source_file(src, dst)
            else:
                shutil.copy(src, dst)
        else:
            shutil.copytree(src, dst)

        # make the file hidden as the dot prefix is not enough
        try:
            subprocess.check_call(["attrib", "+H", dst])
        except FileNotFoundError:
            pass
    else:
        os.symlink(src, dst)


class Install:
    def __init__(self, dry):
        self.dry = dry
        self.dotcontents = {
            "bash": ["bashrc", "bash_profile"],
            "dir_colors.d": ["dir_colors"],
            "gem": ["gemrc"],
            "git.d": ["gitconfig"],
            "hidden.d": ["hidden"],
            "neomutt": ["neomuttrc"],
            "vim": ["vimrc"],
            "vscode.d": [],
            "zsh": ["zshrc"],
        }

    def move(self, src, dst):
        """Move file if it exists to make way for new symlink without
        destroying the old file

        Append the date and time to the old backup to avoid name collisions

        :param src: The old, existing, file
        :param dst: The dotfiles symlink
        """
        bullet, arrow = Colors("yellow").get("[BACKUP ]", "->")
        notify = f"{bullet} {src} {arrow} {dst}"
        if not self.dry:
            os.rename(src, f"{dst}")

        else:
            notify = f"[{Colors('magenta').get('DRY-RUN')}]{notify}"

        print(notify)

    def linkdst(self, src, dst):
        """Determine that a path exists to back it up first

        Attempt to symlink the dotfile

        If a FileExistsError occurs move was unable to move the file and it
        is most likely a dead-link - the file is safe to remove

        Again attempt to symlink - which this time should work

        :param src:         root-file, child-file and key of main loop
        :param dst:         root-file and basename of dotfile to link
        """
        # this won't work for broken symlinks
        if os.path.exists(dst):
            self.move(dst, f"{dst}.{SUFFIX}")

        self.install_files(src, dst)

    def link_vscode_contents(self):
        """Link vscode settings to the user's local config."""
        json_files = ["settings.json", "keybindings.json"]
        vscode_config = os.path.join(HOME, ".config", "Code", "User")
        vscoded_link = os.path.join(HOME, ".vscode.d")
        if os.path.isdir(vscode_config):

            for json_file in json_files:
                src = os.path.join(vscoded_link, json_file)
                dst = os.path.join(vscode_config, json_file)
                self.linkdst(src, dst)

    def link_mains(self):
        """Link the main dotfiles to "$HOME": Firstly the dirs and then from
        the symlinked dirs to "$HOME". Linking files from the symlinks make
        the process a lot more scalable for the future if any changes needed
        to be made as it can get very messy linking each individual file
        from the actual existing directory.
        """
        source = os.path.join(HOME, ".dotfiles", "src")
        for dotdir in self.dotcontents:
            dotfile_src = os.path.join(source, dotdir)
            dotdir_dst = os.path.join(HOME, f".{dotdir}")
            self.linkdst(dotfile_src, dotdir_dst)

            for dotfile in self.dotcontents[dotdir]:
                dotfile_src = os.path.join(HOME, dotdir_dst, dotfile)
                dotfile_dst = os.path.join(HOME, f".{dotfile}")
                self.linkdst(dotfile_src, dotfile_dst)

    def link_vimrc(self):
        """Link the "$HOME/.vimrc" file from the current vim symlink."""
        vimd = os.path.join(SOURCE, "vim")
        src = os.path.join("rc", "vimrc.vim")
        dst = os.path.join(vimd, "vimrc")
        with DevNull():
            try:
                self.linkdst(src, dst)
            except FileNotFoundError:
                src = os.path.join(vimd, src)
                self.linkdst(src, dst)

    def install_files(self, src, dst):
        """Symlink dotfile to its usable location and display what is
        happening

        :param src:         The file in this repository
        :param dst:         The symlink's path
        """
        announce = "[COPYING]" if WINDOWS else "[SYMLINK]"
        bullet, arrow = Colors("cyan").get(announce, "->")
        notify = f"{bullet} {src} {arrow} {dst}"
        if not self.dry:
            link(src, dst)
        else:
            notify = f"[{Colors('magenta').get('DRY-RUN')}]{notify}"

        print(notify)


def reminder(dry):
    if dry:
        notice = Colors("magenta").get("***")
        print(f"\n{notice} No files have been changed {notice}")


def main():
    """Entry point"""
    parser = Parser()
    install = Install(parser.dry)
    install.link_vimrc()
    install.link_mains()
    install.link_vscode_contents()
    reminder(parser.dry)
