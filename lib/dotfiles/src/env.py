import os

from . import color


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
        _color = color.yellow if count % 2 == 0 else color.cyan
        print(value + ":")
        for subkey, subval in obj.items():
            print("    " + _color.get(subkey) + "=" + _color.get(subval))
