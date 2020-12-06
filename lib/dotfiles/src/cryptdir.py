"""
dotfiles.src.cryptdir
=====================
"""
import argparse
import contextlib
import sys

from . import Cleanup, color


class Parser(argparse.ArgumentParser):
    """Subclass ``argparse.ArgumentParser so that no results can be
    returned`` if the right arguments are not provided. ``_check_valid``
    will raise an error and display the parser's helps message in this
    case.
    """

    def __init__(self):
        # noinspection PyTypeChecker
        super().__init__(
            prog=color.cyan.get("cryptdir"),
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
            color.red.print(
                "Cannot encrypt directory without a recipient",
                file=sys.stderr,
            )

            with contextlib.redirect_stdout(sys.stderr):
                self.print_help()

            sys.exit(1)


def encrypt(path, recipient):
    """Encrypt a directory or file. If a directory compress the folder
    into an archive.

    :param path:        Path to the file or directory to encrypt.
    :param recipient:   Recipient key holder for gnupg.
    """
    tarfile = path + ".tar.gz"
    gpgfile = tarfile + ".gpg"

    with Cleanup(path, tarfile) as cryptdir:
        cryptdir.compress()

    with Cleanup(tarfile, gpgfile) as cryptdir:
        cryptdir.encrypt(recipient)

    print("Done")


def decrypt(path):
    """Decrypt a compressed tar directory or file.

    :param path: Path the encrypted tar archive or file.
    """
    tarfile = path.replace(".gpg", "")
    file = tarfile.replace(".tar.gz", "")

    with Cleanup(path, tarfile) as cryptdir:
        cryptdir.decrypt()

    with Cleanup(tarfile, file) as cryptdir:
        cryptdir.extract()

    print("Done")


def main():
    """Options to quickly encrypt or decrypt a directory or file. Mainly
    created to avoid the multiple steps involved with encrypting a
    directory.
    """
    parser = Parser()
    if parser.decrypt:
        decrypt(parser.path)
    else:
        encrypt(parser.path, parser.recipient)
