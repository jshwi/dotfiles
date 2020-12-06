"""
dotfiles.__init__
=================
"""
import argparse
import os
import pathlib

from . import (
    SUFFIX,
    CONFIG,
    HOME,
    CONFIGDIR,
    DOTCONTENTS,
    SOURCE,
    Colors,
    Yaml,
    comments,
)


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
        fout.write(comments.COMMENTS + conf)


def link_dirs(dirs, dirpath, dry):
    for dotdir, dotfiles in dirs.items():
        dotfile_source = os.path.join(SOURCE, dotdir)
        dotdir_dest = os.path.expanduser(dirpath) + dotdir
        linkdest(dotfile_source, dotdir_dest, dry)

        for dotfile in dotfiles:
            dotfile_source = os.path.join(HOME, dotdir_dest, dotfile)
            dotfile_dest = os.path.expanduser(dirpath) + dotfile
            linkdest(dotfile_source, dotfile_dest, dry)


def link_files(files, dirpath, dry):
    for file in files:
        dotfile_source = os.path.join(SOURCE, file)
        filename = os.path.basename(file)
        dotfile_dest = os.path.expanduser(dirpath) + filename
        linkdest(dotfile_source, dotfile_dest, dry)


def link_all(conf, dry):

    for dot_type in conf:

        for dirpath, obj in conf[dot_type].items():

            if dot_type == "dirs":
                link_dirs(obj, dirpath, dry)

            elif dot_type == "files":
                link_files(obj, dirpath, dry)


def link_vimrc_version():
    src = os.path.join("rc", "vimrc.vim")
    dst = os.path.join(SOURCE, "vim", "vimrc")
    try:
        os.symlink(src, dst)
    except FileExistsError:
        os.remove(dst)
        os.symlink(src, dst)


def main():
    """Link the main dotfiles to "$HOME": Firstly the dirs and then from
    the symlinked dirs to "$HOME". Linking files from the symlinks make
    the process a lot more scalable for the future if any changes needed
    to be made as it can get very messy linking each individual file
    from the actual existing directory.
    """
    parser = Parser()
    pathlib.Path(CONFIGDIR).mkdir(parents=True, exist_ok=True)
    conf = Yaml(CONFIG)

    if conf.exists:

        if parser.force:
            os.remove(CONFIG)
            conf.exists = False
        else:
            conf.read()

    if not conf.exists:
        conf.dict.update(DOTCONTENTS)
        conf.write()
        comment_yaml()

        if parser.init:
            print("created default conf:")
            print(CONFIG)

    if not parser.init:
        link_vimrc_version()
        link_all(conf.dict, parser.dry)

        if parser.dry:
            notice = Colors("magenta").get("***")
            print(f"\n{notice} No files have been changed {notice}")
