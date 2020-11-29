import argparse
import os


from . import env, classy


def repo_whitelist():
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
    print(f"updating `{env.WHITELIST}'")
    stdout = []
    hashcap = classy.HashCap(env.WHITELISTPATH)
    pathio = classy.TextIO(env.WHITELISTPATH)
    if os.path.isfile(env.WHITELISTPATH):
        hashcap.hash_file()

    # append whitelist exceptions for each individual module
    for item in args.files:
        if os.path.exists(item):
            stdout.extend(
                classy.pipe_command(args.executable, item, "--make-whitelist")
            )

    # merge the prepended PyInspection line to the beginning of every
    # entry
    lines = [line.strip() for line in stdout if line != ""]

    # clear contents of instantiated `TextIO' object to write a new file
    # and not append
    pathio.write(*lines)
    classy.announce(hashcap, env.WHITELIST)
