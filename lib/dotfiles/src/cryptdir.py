"""
cryptdir
========
"""
import argparse
import contextlib
import sys

from . import Cleanup, Colors


class Parser(argparse.ArgumentParser):
    def __init__(self):
        # noinspection PyTypeChecker
        super().__init__(
            prog=Colors("cyan").get("cryptdir"),
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=42
            ),
        )
        self._add_arguments()
        self._args = self.parse_args()
        self.path = self._args.path
        self.recipient = self._args.recip
        self.decrypt = self._args.decrypt
        self._check_valid()

    def _add_arguments(self):
        self.add_argument(
            "path", metavar="PATH", action="store", help="path to archive"
        )
        self.add_argument(
            "-d",
            "--decrypt",
            action="store_true",
            help="decrypt directory as opposed to the default encrypt",
        )
        self.add_argument(
            "-r",
            "--recip",
            metavar="RECIP",
            action="store",
            help="recipient key-holder",
        )

    def _check_valid(self):
        if not self.decrypt and not self.recipient:
            Colors("red").print(
                "Cannot encrypt directory without a recipient",
                file=sys.stderr,
            )

            with contextlib.redirect_stdout(sys.stderr):
                self.print_help()

            sys.exit(1)


def encrypt(path, recipient):
    tarfile = path + ".tar.gz"
    gpgfile = tarfile + ".gpg"

    with Cleanup(path, tarfile) as cryptdir:
        cryptdir.compress()

    with Cleanup(tarfile, gpgfile) as cryptdir:
        cryptdir.encrypt(recipient)

    print("Done")


def decrypt(path):
    tarfile = path.replace(".gpg", "")
    file = tarfile.replace(".tar.gz", "")

    with Cleanup(path, tarfile) as cryptdir:
        cryptdir.decrypt()

    with Cleanup(tarfile, file) as cryptdir:
        cryptdir.extract()

    print("Done")


def main():
    parser = Parser()
    if parser.decrypt:
        decrypt(parser.path)
    else:
        encrypt(parser.path, parser.recipient)
