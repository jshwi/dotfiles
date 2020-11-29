import argparse
import os
import subprocess

from . import classy, env


def reporeqs():
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
    print(f"updating `{env.REQUIREMENTS}'")
    hashcap = classy.HashCap(env.REQUIREMENTS)
    if os.path.isfile(env.REQUIREMENTS):
        hashcap.hash_file()

    # get the stdout for both production and development packages
    stdout = classy.pipe_command(args.executable, env.LOCKPATH)
    stdout += classy.pipe_command(args.executable, "--dev", env.LOCKPATH)

    # write to file and then use sed to remove the additional
    # information following the semi-colon
    reqpathio = classy.TextIO(env.REQPATH)
    reqpathio.write(*stdout)
    reqpathio.sort()
    reqpathio.deduplicate()
    reqpathio.write()
    # noinspection SubprocessShellMode
    subprocess.call("sed -i 's/;.*//' " + env.REQPATH, shell=True)
    classy.announce(hashcap, env.REQUIREMENTS)
