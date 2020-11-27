"""
dotfiles.src.config
===================
"""
import os
import pathlib

import yaml

DOTCONTENTS = {
    "bash": ["bashrc", "bash_profile"],
    "dir_colors.d": ["dir_colors"],
    "gem": ["gemrc"],
    "git.d": ["gitconfig"],
    "hidden.d": ["hidden"],
    "neomutt": ["neomuttrc"],
    "vim": ["vimrc"],
    "vscode.d": [],
    "zsh": ["zshrc"],
}


class Yaml(dict):
    def __init__(self, path, __m=None, **kwargs):
        super().__init__()
        pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        if os.path.isfile(path):
            self.read(path)
        elif __m is not None:
            self.update(__m, **kwargs)
            self.write(path)

    def write(self, path):
        with open(path, "w") as fout:
            yaml.dump(self, fout)

    def read(self, path):
        with open(path) as fin:
            # noinspection PyyamlLoad
            self.update(yaml.load(fin, Loader=yaml.FullLoader))
