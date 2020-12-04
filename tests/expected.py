"""
tests.helpers
=============
"""
import os

SRC = os.path.join(".dotfiles", "src")
BASH = ".bash"
VSCODED = "vscode.d"
CONFIGD = ".config"
SETTINGS_JSON = "settings.json"
KEYBINDINGS_JSON = "keybindings.json"
CODE_USER = os.path.join(CONFIGD, "Code", "User")
FOLLOW_PATH_OBJ = {
    "vscode": [
        os.path.join(CODE_USER, SETTINGS_JSON),
        os.path.join(CODE_USER, KEYBINDINGS_JSON),
    ],
    "vim": [os.path.join(".vim", "vimrc")],
}
FOLLOW_PATH = [p for _, v in FOLLOW_PATH_OBJ.items() for p in v]
PAIRS = {
    os.path.join(SRC, "bash"): BASH,
    os.path.join(BASH, "bashrc"): ".bashrc",
    os.path.join(BASH, "bash_profile"): ".bash_profile",
    os.path.join(SRC, "dir_colors.d"): ".dir_colors.d",
    os.path.join(".dir_colors.d", "dir_colors"): ".dir_colors",
    os.path.join(SRC, "gem"): ".gem",
    os.path.join(".gem", "gemrc"): ".gemrc",
    os.path.join(SRC, "git.d"): ".git.d",
    os.path.join(".git.d", "gitconfig"): ".gitconfig",
    os.path.join(SRC, "hidden.d"): ".hidden.d",
    os.path.join(".hidden.d", "hidden"): ".hidden",
    os.path.join(SRC, "neomutt"): ".neomutt",
    os.path.join(".neomutt", "neomuttrc"): ".neomuttrc",
    os.path.join(SRC, "vim"): ".vim",
    os.path.join(".vim", "vimrc"): ".vimrc",
    os.path.join(SRC, "zsh"): ".zsh",
    os.path.join(".zsh", "zshrc"): ".zshrc",
    os.path.join(SRC, VSCODED, SETTINGS_JSON): os.path.join(
        CONFIGD, "Code", "User", SETTINGS_JSON
    ),
    os.path.join(SRC, VSCODED, KEYBINDINGS_JSON): os.path.join(
        CONFIGD, "Code", "User", KEYBINDINGS_JSON
    ),
}


def output(tmpdir):
    """Get the string that is expected when running
    ``tests._test.test_output``.

    :param tmpdir:  The temporary directory ``pytest`` fixture.
    :return:        A string that the output should match.
    """
    expected = ""
    for keyvaluepair in PAIRS.items():
        prepend = [os.path.join(tmpdir, i) for i in keyvaluepair]
        expected += f"[SYMLINK] {prepend[0]} -> {prepend[1]}\n"
    return expected


def backups(tmpdir, suffix):
    """Get the string that is expected when running
    ``tests._test.test_backup``.

    :param tmpdir:  The temporary directory ``pytest`` fixture.
    :param suffix:  The time suffix fixture to be appended to
                    the file taken from the ``dotfiles.SUFFIX``
                    constant so as to ensure a match.
    :return:        A string that the backup output should match.
    """
    expected = ""
    for keyvaluepair in PAIRS.items():
        key, value = [os.path.join(tmpdir, i) for i in keyvaluepair]
        key_basename = os.path.basename(key)
        if key_basename != "vimrc.vim":
            if key_basename in [
                os.path.basename(p) for p in FOLLOW_PATH_OBJ["vscode"]
            ]:
                backup_key = os.path.join(tmpdir, CODE_USER, key_basename)
            else:
                backup_key = os.path.join(tmpdir, f".{key_basename}")
            expected += f"[BACKUP ] {backup_key} -> {value}.{suffix}\n"
            expected += f"[SYMLINK] {key} -> {value}\n"
    return expected


def dry_run(tmpdir):
    """Get the string that is expected when running
    ``tests._test.test_dry_run``.

    :param tmpdir:  The temporary directory ``pytest`` fixture.
    :return:        A string that the dry-run output should match.
    """
    expected = ""
    bare_output = output(tmpdir)
    for line in bare_output.splitlines():
        expected += f"[DRY-RUN]{line}\n"
    return expected + "\n*** No files have been changed ***\n"


def dry_run_backups(tmpdir, suffix):
    """Get the string that is expected when running
    ``tests._test.test_dry_run_backups``.

    :param tmpdir:  The temporary directory ``pytest`` fixture.
    :param suffix:  The time suffix fixture to be appended to
                    the file taken from the ``dotfiles.SUFFIX``
                    constant so as to ensure a match.
    :return:        A string that the dry-run, including dry-run
                    "backups", output should match.
    """
    expected = ""
    bare_output = backups(tmpdir, suffix)
    for line in bare_output.splitlines():
        expected += f"[DRY-RUN]{line}\n"
    expected += "\n*** No files have been changed ***\n"
    return expected
