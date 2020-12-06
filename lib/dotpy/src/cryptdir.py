"""
cryptdir
"""
import argparse
import os
import shutil
import subprocess

from . import Tar


class Parser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(prog="cryptdir")
        self._add_arguments()
        self._args = self.parse_args()
        self.rec = self._args.rec
        self.path = self._args.path

    def _add_arguments(self):
        self.add_argument(
            "path", metavar="PATH", action="store", help="path to archive"
        )
        self.add_argument(
            "-r",
            "--rec",
            action="store",
            help="recipient key-holder",
        )


class GPG:
    def __init__(self, file):
        self._file = file
        self.enc = file + ".gpg"

    def encrypt(self, recipient):
        subprocess.call(
            [
                "gpg",
                "-output",
                self.enc,
                "--encrypt",
                self._file,
                "--recipient",
                recipient,
            ]
        )

    def decrypt(self):
        subprocess.call(["gpg", "--decrypt", self.enc])


def main():
    parser = Parser()
    archive = parser.path + ".tar.gz"
    gpg = GPG(archive)

    print("Compressing " + parser.path)
    Tar(parser.path, archive)
    print(". " + parser.path + " -> " + archive)

    print("Removing " + parser.path)
    shutil.rmtree(parser.path)
    print(". removed " + parser.path)

    print("Encrypting " + archive)
    gpg.encrypt(parser.rec)
    print(". " + archive + " -> " + gpg.enc)

    print("Removing " + archive)
    os.remove(archive)
    print(". removed " + archive)

    print("Done")
