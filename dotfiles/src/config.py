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
        self.path = path
        self.init(__m, **kwargs)

    def write(self):
        with open(self.path, "w") as fout:
            yaml.dump(self, fout)

    def init(self, __m, **kwargs):
        pathlib.Path(os.path.dirname(self.path)).mkdir(
            parents=True, exist_ok=True
        )
        if os.path.isfile(self.path):
            self.read()
        elif __m is not None:
            self.update(__m, **kwargs)
            self.write()

    def read(self):
        with open(self.path) as fin:
            self.update(yaml.safe_load(fin))
