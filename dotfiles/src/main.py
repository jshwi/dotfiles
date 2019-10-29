"""
dotfiles.src.main
=================
"""
import argparse
import datetime
import os
import pathlib

import appdirs

HOME = str(pathlib.Path.home())

CONFIGDIR = appdirs.user_config_dir(__name__.partition(".")[0])
CONFIG = os.path.join(CONFIGDIR, "dotfiles.yaml")

SUFFIX = datetime.datetime.now().strftime("%d%m%YT%H%M%S")


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
        self.dry = self._args.dry

    def _add_arguments(self):
        self.add_argument(
            "-d",
            "--dry",
            action="store_true",
            help="see what actions would take place",
        )


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


def link_vimrc(dry):
    """Link the "$HOME/.vimrc" file from the current vim symlink.

    :param dry: Dry-run: On or off.
    """
    vimd = os.path.join(HOME, ".vim")
    vimrc = os.path.join(vimd, "vimrc")
    base_vimrc = os.path.join(vimd, "rc", "vimrc.vim")
    if not os.path.exists(vimrc):
        symlink(base_vimrc, vimrc, dry)


def link_vscode_contents(dry):
    """Link vscode settings to the user's local config.

    :param dry: Dry-run: On or off.
    """
    json_files = ["settings.json", "keybindings.json"]
    vscode_config = os.path.join(HOME, ".config", "Code", "User")
    vscoded_link = os.path.join(HOME, ".vscode.d")
    if os.path.isdir(vscode_config):

        for json_file in json_files:
            src = os.path.join(vscoded_link, json_file)
            dst = os.path.join(vscode_config, json_file)
            linkdst(src, dst, dry)


def link_mains(dry):
    """Link the main dotfiles to "$HOME": Firstly the dirs and then from
    the symlinked dirs to "$HOME". Linking files from the symlinks make
    the process a lot more scalable for the future if any changes needed
    to be made as it can get very messy linking each individual file
    from the actual existing directory.

    :param dry: Dry-run: On or off.
    """
    source = os.path.join(HOME, ".dotfiles", "src")
    for dotdir in DOTCONTENTS:
        dotfile_src = os.path.join(source, dotdir)
        dotdir_dst = os.path.join(HOME, f".{dotdir}")
        linkdst(dotfile_src, dotdir_dst, dry)

        for dotfile in DOTCONTENTS[dotdir]:
            dotfile_src = os.path.join(HOME, dotdir_dst, dotfile)
            dotfile_dst = os.path.join(HOME, f".{dotfile}")
            linkdst(dotfile_src, dotfile_dst, dry)


def main():
    """Entry point"""
    parser = Parser()
    link_mains(parser.dry)
    link_vimrc(parser.dry)
    link_vscode_contents(parser.dry)
    if parser.dry:
        notice = colors(5, "***")
        print(f"\n{notice} No files have been changed {notice}")
