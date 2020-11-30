import argparse
import os
import subprocess

from . import (
    REQUIREMENTS,
    LOCKPATH,
    REQPATH,
    HashCap,
    TextIO,
    announce,
    pipe_command,
)


def main():
    """Create or update and then format ``requirements.txt`` from
    ``Pipfile.lock``.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--executable",
        action="store",
        help="path to venv executable",
    )
    args = parser.parse_args()
    print(f"updating `{REQUIREMENTS}'")
    hashcap = HashCap(REQUIREMENTS)
    if os.path.isfile(REQUIREMENTS):
        hashcap.hash_file()

    # get the stdout for both production and development packages
    stdout = pipe_command(args.executable, LOCKPATH)
    stdout += pipe_command(args.executable, "--dev", LOCKPATH)

    # write to file and then use sed to remove the additional
    # information following the semi-colon
    reqpathio = TextIO(REQPATH)
    reqpathio.write(*stdout)
    reqpathio.sort()
    reqpathio.deduplicate()
    reqpathio.write()
    # noinspection SubprocessShellMode
    subprocess.call("sed -i 's/;.*//' " + REQPATH, shell=True)
    announce(hashcap, REQUIREMENTS)
