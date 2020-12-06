import os

from . import Colors


def get_matches():
    matches = {}
    for key, value in os.environ.items():
        for subkey, subval in os.environ.items():
            if (
                value == subval
                and key != subkey
                and value not in ("true", "false")
            ):
                if value not in matches:
                    matches.update({value: {}})
                matches[value].update({key: value})
    return matches


def main():
    matches = get_matches()
    for count, (value, obj) in enumerate(matches.items()):
        color = Colors("yellow" if count % 2 == 0 else "cyan")
        print(value + ":")
        for subkey, subval in obj.items():
            print("    " + color.get(subkey) + "=" + color.get(subval))
