"""
dotfiles.__init__
=================
"""
import argparse
import datetime
import os
import pathlib

import appdirs
from .src import config

HOME = str(pathlib.Path.home())
CONFIGDIR = appdirs.user_config_dir(__name__)
CONFIG = os.path.join(CONFIGDIR, __name__ + ".yaml")
SUFFIX = datetime.datetime.now().strftime("%d%m%YT%H%M%S")


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


class Parser(argparse.ArgumentParser):
    """Get help or add ``--dry`` argument to the process."""

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
        self.init = self._args.init
        self.force = self._args.force
        self.dry = self._args.dry

    def _add_arguments(self):
        self.add_argument(
            "-i",
            "--init",
            action="store_true",
            help="create the default conf file",
        )
        self.add_argument(
            "-f",
            "--force",
            action="store_true",
            help=(
                "if used with --init any existing conf will be "
                "overwritten by the default"
            ),
        )
        self.add_argument(
            "-d",
            "--dry",
            action="store_true",
            help="see what actions would take place",
        )


def move(source, dest, dry):
    """Move file if it exists to make way for new symlink without
    destroying the old file. Append the date and time to the old backup
    to avoid name collisions.

    :param source:  The old, existing, file.
    :param dest:    The dotfiles symlink.
    :param dry:     Print what would but do not do anything if True.
                    Announce that this is happening.
    """
    yellow = Colors("yellow")
    notify = f"{yellow.get('[BACKUP ]')} {source} {yellow.get('->')} {dest}"

    if not dry:
        os.rename(source, dest)
        print(notify)

    else:
        print(f"[{Colors('magenta').get('DRY-RUN')}]{notify}")


def symlink(source, dest, dry):
    """Symlink dotfile to its usable location and display what is
    happening.

    :param source:  The file in this repository.
    :param dest:    The symlink's path.
    :param dry:     Print what would but do not do anything if True.
                    Announce that this is happening.
    """
    cyan = Colors("cyan")
    notify = f"{cyan.get('[SYMLINK]')} {source} {cyan.get('->')} {dest}"

    if not dry:
        try:
            os.symlink(source, dest)
            print(notify)

        except FileNotFoundError:
            pass

    else:
        print(f"[{Colors('magenta').get('DRY-RUN')}]{notify}")


def linkdest(source, dest, dry):
    """Determine that a path exists to back it up first. Attempt to
    symlink the dotfile. If a FileExistsError occurs move was unable to
    move the file and it is most likely a dead-link - the file is safe
    to remove. Again attempt to symlink - which this time should work.

    :param source:  root-file, child-file and key of main loop.
    :param dest:    root-file and basename of dotfile to link.
    :param dry:     Pass this argument on to the ``move`` process and
                    the ``symlink`` process.
    """
    # this won't work for broken symlinks
    if os.path.exists(dest):
        move(dest, f"{dest}.{SUFFIX}", dry)

    # in the case of broken symlink - safe as file is already backed up
    try:
        symlink(source, dest, dry)
    except FileExistsError:
        os.remove(dest)
        symlink(source, dest, dry)


def comment_yaml():

    with open(CONFIG) as fin:
        conf = fin.read()

    with open(CONFIG, "w") as fout:
        fout.write(config.COMMENTS + conf)


def link_dirs(dirs, source, dirpath, dry):
    for dotdir, dotfiles in dirs.items():
        dotfile_source = os.path.join(source, dotdir)
        dotdir_dest = os.path.expanduser(dirpath) + dotdir
        linkdest(dotfile_source, dotdir_dest, dry)

        for dotfile in dotfiles:
            dotfile_source = os.path.join(HOME, dotdir_dest, dotfile)
            dotfile_dest = os.path.expanduser(dirpath) + dotfile
            linkdest(dotfile_source, dotfile_dest, dry)


def link_files(files, source, dirpath, dry):
    for file in files:
        dotfile_source = os.path.join(source, file)
        filename = os.path.basename(file)
        dotfile_dest = os.path.expanduser(dirpath) + filename
        linkdest(dotfile_source, dotfile_dest, dry)


def link_all(conf, dry):
    source = os.path.join(HOME, ".dotfiles", "src")

    for dot_type in conf:

        for dirpath, obj in conf[dot_type].items():

            if dot_type == "dirs":
                link_dirs(obj, source, dirpath, dry)

            elif dot_type == "files":
                link_files(obj, source, dirpath, dry)


def main():
    """Link the main dotfiles to "$HOME": Firstly the dirs and then from
    the symlinked dirs to "$HOME". Linking files from the symlinks make
    the process a lot more scalable for the future if any changes needed
    to be made as it can get very messy linking each individual file
    from the actual existing directory.
    """
    parser = Parser()
    pathlib.Path(CONFIGDIR).mkdir(parents=True, exist_ok=True)
    conf = config.Yaml(CONFIG)

    if conf.exists:

        if parser.force:
            os.remove(CONFIG)
            conf.exists = False
        else:
            conf.read()

    if not conf.exists:
        conf.dict.update(config.DOTCONTENTS)
        conf.write()
        comment_yaml()

        if parser.init:
            print("created default conf:")
            print(CONFIG)

    if not parser.init:
        link_all(conf.dict, parser.dry)

        if parser.dry:
            notice = Colors("magenta").get("***")
            print(f"\n{notice} No files have been changed {notice}")
