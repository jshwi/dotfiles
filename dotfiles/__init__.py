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

HOME = str(pathlib.Path.home())
SUFFIX = datetime.datetime.now().strftime("%d%m%YT%H%M%S")
DOTCONTENTS = {
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
WINDOWS = os.name == "nt"


class EnterDir:
    """Change to the selected directory entered as an argument and when
    actions are complete return to the previous directory.

    :param path: Enter the directory to temporarily change to.
    """

    def __init__(self, path):
        self.saved_path = os.getcwd()
        self.enter_path = os.path.expanduser(path)

    def __enter__(self):
        os.chdir(self.enter_path)

    def __exit__(self, _, value, __):
        os.chdir(self.saved_path)


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


def cp_nt(src, dst):
    """For NT systems where symlinks require elevated privilege copying
    and sourcing is the preferred option.

    :param src: The file in this repository
    :param dst: The symlink's path
    """
    # try:
    method = shutil.copy if os.path.isfile(src) else shutil.copytree
    method(src, dst)

    # make the file hidden as the dot prefix is not enough
    try:
        subprocess.check_call(["attrib", "+H", dst])
    except FileNotFoundError:
        pass

    # except FileNotFoundError:
    #     pass


def link_nix(src, dst):
    """For Unix-like systems where symlinks do not require elevated
    privilege this is the preferred option.

    :param src: The file in this repository
    :param dst: The symlink's path
    """
    try:
        os.symlink(src, dst)

    except FileExistsError:

        # in the case of broken symlink - safe as file is already backed
        # up
        os.remove(dst)
        os.symlink(src, dst)


def install_files(src, dst, dry):
    """Symlink dotfile to its usable location and display what is
    happening

    :param src:         The file in this repository
    :param dst:         The symlink's path
    :param dry:         Print what would but do not do anything if True
                        Announce that this is happening
    """
    func, bullet = (cp_nt, "[COPYING]") if WINDOWS else (link_nix, "[SYMLINK]")
    bullet, arrow = symbols(bullet, 6)
    notify = f"{bullet} {src} {arrow} {dst}"
    if not dry:
        func(src, dst)
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

    install_files(src, dst, dry)


def relative_link(path, src, dst, dry):
    with EnterDir(path):
        if not os.path.exists(dst):
            install_files(src, dst, dry)


def link_vimrc(dry):
    """Link the "$HOME/.vimrc" file from the current vim symlink.

    :param dry: Dry-run: On or off.
    """
    vimd = os.path.join(HOME, ".vim")
    rc_vimrc = os.path.join("rc", "vimrc.vim")
    relative_link(vimd, rc_vimrc, "vimrc", dry)


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