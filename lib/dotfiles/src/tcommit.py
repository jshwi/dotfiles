import argparse
import datetime
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--message", action="store", help="additional message"
    )
    parser.add_argument(
        "-p", "--push", action="store_true", help="push commit"
    )
    args = parser.parse_args()
    message = " " + args.message if args.message else ""
    now = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", f"[{now}]{message}"])
    if args.push:
        subprocess.call(["git", "push"])
