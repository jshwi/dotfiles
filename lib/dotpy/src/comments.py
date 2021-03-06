"""
Dictionary sorted by symlink destination.
Source relative to ~/.dotfiles.

The dirs key contains a dictionary of destinations paired with
dictionaries of directories and their files.

The directories will be symlinked from ~/.dotfiles to their destination
and the files will be symlinked to that directory's symlink.

e.g. bash in ~/. in dirs            ~/.dotfiles/bash    -> ~/.bash
     bashrc in bash in ~/. in dirs  ~/.bash/bashrc      -> ~/.bashrc

The file key contains a dictionary of destinations paired with lists of
individual files or directories that will be symlinked individually.
"""
COMMENTS = "# --- autogenerated default conf ---\n#{}".format(
    __doc__.lower().replace("\n", "\n# ")[:-2]
)
