import argparse
import os

from . import WHITELIST, WHITELISTPATH, HashCap, TextIO, announce, pipe_command


def main():
    """Prepend a line before every lines in a file."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        help="files to scan for vulture's whitelist.py",
    )
    parser.add_argument(
        "-e",
        "--executable",
        action="store",
        help="path to venv executable",
    )
    args = parser.parse_args()
    print(f"updating `{WHITELIST}'")
    stdout = []
    hashcap = HashCap(WHITELISTPATH)
    pathio = TextIO(WHITELISTPATH)
    if os.path.isfile(WHITELISTPATH):
        hashcap.hash_file()

    # append whitelist exceptions for each individual module
    for item in args.files:
        if os.path.exists(item):
            stdout.extend(
                pipe_command(args.executable, item, "--make-whitelist")
            )

    # merge the prepended PyInspection line to the beginning of every
    # entry
    lines = [line.strip() for line in stdout if line != ""]

    # clear contents of instantiated `TextIO' object to write a new file
    # and not append
    pathio.write(*lines)
    announce(hashcap, WHITELIST)
