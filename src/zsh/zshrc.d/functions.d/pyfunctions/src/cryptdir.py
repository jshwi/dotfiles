"""
cryptdir
"""
import argparse

from . import tar


class Parser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(prog="mkarchive")
        self._add_arguments()
        self._args = self.parse_args()
        self.recipient = self._args.recipient
        self.path = self._args.path

    def _add_arguments(self):
        self.add_argument(
            "recip",
            metavar="RECIP",
            action="store",
            help="recipient key-holder",
        )
        self.add_argument(
            "path", metavar="PATH", action="store", help="path to archive"
        )


def main():
    parser = Parser()
    tar.Tar()
