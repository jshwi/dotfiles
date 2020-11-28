"""
dotfiles.__init__
=================
"""
import argparse
import datetime
import os
import pathlib

import appdirs
import yaml

HOME = str(pathlib.Path.home())
CONFIGDIR = appdirs.user_config_dir(__name__)
CONFIG = os.path.join(CONFIGDIR, __name__ + ".yaml")
SUFFIX = datetime.datetime.now().strftime("%d%m%YT%H%M%S")
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
        "~/.vim/": ["vim/rc/vimrc"],
        "~/.config/Code/User": [
            "vscode.d/settings.json",
            "vscode.d/keybindings.json",
        ],
    },
)


def colors(code, *args):
    """Return a colored string or a tuple of strings

    :param code:    Ansi escape code
    :param args:    String or strings
    :return:        String or tuple of strings
    """
    result = [f"\u001b[0;3{code};40m{arg}\u001b[0;0m" for arg in args]
    return result[0] if len(result) == 1 else result


class Parser(argparse.ArgumentParser):
    """Get help or add ``--dry`` argument to the process"""

    def __init__(self):
        super().__init__(
            prog=colors(6, "./install"),
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
            help="create the default config file",
        )
        self.add_argument(
            "-f",
            "--force",
            action="store_true",
            help=(
                "if used with --init any existing config will be "
                "overwritten by the default"
            ),
        )
        self.add_argument(
            "-d",
            "--dry",
            action="store_true",
            help="see what actions would take place",
        )


class Yaml:
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.exists = os.path.isfile(self.path)
        self.dict = {}

    def write(self):
        with open(self.path, "w") as fout:
            yaml.dump(self.dict, fout)
        self.exists = True

    def read(self):
        if self.exists:
            with open(self.path) as fin:
                # noinspection PyyamlLoad
                self.dict.update(yaml.load(fin, Loader=yaml.FullLoader))


def symbols(bullet, color):
    """Return a bullet-point and an arrow in the chosen color.

    :param bullet:  Bullet of chosen argument.
    :param color:   The selected color.
    :return:        A tuple containing the stylized bullet-point and the
                    colored arrow.
    """
    return colors(color, bullet, "->")


def move(src, dst, dry):
    """Move file if it exists to make way for new symlink without
    destroying the old file

    Append the date and time to the old backup to avoid name collisions

    :param src: The old, existing, file
    :param dst: The dotfiles symlink
    :param dry: Print what would but do not do anything if True
                Announce that this is happening
    """
    bullet, arrow = symbols("[BACKUP ]", 3)
    notify = f"{bullet} {src} {arrow} {dst}"

    if not dry:
        os.rename(src, f"{dst}")
    else:
        notify = f"[{colors(5, 'DRY-RUN')}]{notify}"

    print(notify)


def symlink(src, dst, dry):
    """Symlink dotfile to its usable location and display what is
    happening

    :param src:         The file in this repository
    :param dst:         The symlink's path
    :param dry:         Print what would but do not do anything if True
                        Announce that this is happening
    """
    bullet, arrow = symbols("[SYMLINK]", 6)
    notify = f"{bullet} {src} {arrow} {dst}"

    if not dry:
        os.symlink(src, dst)
    else:
        notify = f"[{colors(5, 'DRY-RUN')}]{notify}"

    print(notify)


def linkdst(src, dst, dry):
    """Determine that a path exists to back it up first

    Attempt to symlink the dotfile

    If a FileExistsError occurs move was unable to move the file and it
    is most likely a dead-link - the file is safe to remove

    Again attempt to symlink - which this time should work

    :param src:         root-file, child-file and key of main loop
    :param dst:         root-file and basename of dotfile to link
    :param dry:         Pass this argument on to the ``move`` process
                        and the ``symlink`` process
    """
    # this won't work for broken symlinks
    if os.path.exists(dst):
        move(dst, f"{dst}.{SUFFIX}", dry)

    # in the case of broken symlink - safe as file is already backed up
    try:
        symlink(src, dst, dry)
    except FileExistsError:
        os.remove(dst)
        symlink(src, dst, dry)


def comment_yaml():
    comments = [
        f"# --- autogenerated default config ---",
        "# dictionary sorted by link destination",
        "#",
        "# e.g. ``bash`` in ``~/.`` will be linked to ``~/.bash``",
        "#",
        "# all keys containing a key-value pair are directories and their",
        "# files and both will be linked",
        "#",
        "# all keys containing individual values are only going to link that",
        "# file or directory to their key's location",
    ]

    with open(CONFIG) as fin:
        config = fin.read().splitlines()

    for i in range(len(comments)):
        config.insert(i + 1, comments[i])

    with open(CONFIG, "w") as fout:
        for line in config:
            fout.write(line + "\n")


def link_dirs(dirs, source, dirpath, dry):
    for dotdir, dotfiles in dirs.items():
        dotfile_src = os.path.join(source, dotdir)
        dotdir_dst = os.path.expanduser(dirpath) + dotdir
        linkdst(dotfile_src, dotdir_dst, dry)

        for dotfile in dotfiles:
            dotfile_src = os.path.join(HOME, dotdir_dst, dotfile)
            dotfile_dst = os.path.expanduser(dirpath) + dotfile
            linkdst(dotfile_src, dotfile_dst, dry)


def link_files(files, source, dirpath, dry):
    for file in files:
        dotfile_src = os.path.join(source, file)
        filename = os.path.basename(file)
        dotfile_dst = os.path.expanduser(dirpath) + filename
        linkdst(dotfile_src, dotfile_dst, dry)


def link_all(config, dry):
    source = os.path.join(HOME, ".dotfiles", "src")

    for dot_type in config:

        for dirpath, obj in config[dot_type].items():

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
    config = Yaml(CONFIG)

    if config.exists:

        if parser.force:
            os.remove(CONFIG)
            config.exists = False
        else:
            config.read()

    if not config.exists:
        config.dict.update(DOTCONTENTS)
        config.write()
        comment_yaml()
        print("created default config:")
        print(CONFIG)

    if not parser.init:
        link_all(config.dict, parser.dry)

        if parser.dry:
            notice = colors(5, "***")
            print(f"\n{notice} No files have been changed {notice}")
