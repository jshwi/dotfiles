"""
dotfiles.src.symlink_vim
========================
"""
import argparse
import os

from . import HOME


def main():
    """Dynamically link a base version of vim's vimrc or an ide version
    suitable for Python programming.
    """
    parser = argparse.ArgumentParser(prog="symlink_vim")
    parser.add_argument(
        "-i",
        "--ide",
        action="store_true",
        help="open vim in ide mode",
    )
    args = parser.parse_known_args()[0]
    vim_dir = os.path.join(HOME, ".vim")
    src = os.path.join("rc", "vimrc.vim")
    dst = os.path.join(vim_dir, "vimrc")

    if args.ide:
        src = os.path.join("rc", "vimide.vim")

    if os.path.islink(dst):
        os.remove(dst)

    os.symlink(src, dst)
