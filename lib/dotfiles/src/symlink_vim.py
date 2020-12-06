"""
vim
"""
import argparse
import os

from . import HOME


class Parser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(prog="vim")
        self._add_arguments()
        self._args = self.parse_known_args()[0]
        self.ide = self._args.ide

    def _add_arguments(self):
        self.add_argument(
            "-i",
            "--ide",
            action="store_true",
            help="open vim in ide mode",
        )


def main():
    parser = Parser()
    vim_dir = os.path.join(HOME, ".vim")
    src = os.path.join("rc", "vimrc.vim")
    dst = os.path.join(vim_dir, "vimrc")

    if parser.ide:
        src = os.path.join("rc", "vimide.vim")

    if os.path.islink(dst):
        os.remove(dst)

    os.symlink(src, dst)
