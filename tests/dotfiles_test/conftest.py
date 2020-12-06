import os
import pathlib
import sys

import dotfiles
import pytest

DOTFILES = ".dotfiles"


@pytest.fixture(name="mock_constants", autouse=True)
def fixture_mock_install_constants(
    nocolorcapsys, monkeypatch, tmpdir, entry_point
):
    """Run the install process and return it's output stripped of any
    ANSI escaped color codes. The returned output can be used or ignored
    to control the stream of stdout/ stderr.

    :param entry_point:
    :param tmpdir:
    :param monkeypatch:
    :param nocolorcapsys:   The ``capsys`` fixture altered to remove
                            ANSI escape codes.
    :return:                Stdout.
    """

    def expanduser(path):
        return path.replace("~/.", f"{tmpdir}/.")

    sys.argv = [entry_point]
    monkeypatch.setattr(dotfiles.install.os.path, "expanduser", expanduser)
    dotfiles.install.HOME = tmpdir
    dotfiles.install.CONFIGDIR = os.path.join(
        dotfiles.install.HOME, ".config", __name__
    )
    dotfiles.install.CONFIG = os.path.join(
        dotfiles.install.CONFIGDIR, __name__ + ".yaml"
    )
    dotfiles.install.DOTFILES = os.path.join(tmpdir, DOTFILES)
    dotfiles.install.SOURCE = os.path.join(tmpdir, DOTFILES, "src")


@pytest.fixture(name="suffix")
def fixture_suffix():
    """Get the accurate timestamp from ``dotfiles.SUFFIX`` so that there
    is no discrepancy between the test time and the module's time.

    :return: Timestamp to be appended to backed up files.
    """
    return dotfiles.SUFFIX


@pytest.fixture(name="recipient")
def fixture_recipient(tmpdir, nocolorcapsys):
    """Create a .gnupg directory along with a temporary encryption and
    decryption key etc. to use during testing

    :param : The altered test Parser() Namespace
    """
    recipient = "joe@foo.bar"

    dummy_key = (
        "%no-protection\n"
        "Key-Type: RSA\n"
        "Key-Length: 1024\n"
        "Subkey-Type: RSA\n"
        "Subkey-Length: 1024\n"
        "Name-Real: Joe Foo\n"
        "Name-Comment: stupid passphrase\n"
        "Name-Email: " + recipient + "\n"
        "Expire-Date: 1\n"
        "%commit\n"
    )

    homedir = pathlib.Path(tmpdir) / ".gnupg"
    keyfile = homedir / "keyfile.asc"

    homedir.mkdir(parents=True, exist_ok=True)

    with keyfile.open("w") as fout:
        fout.write(dummy_key)

    homedir.chmod(0o700)
    keyfile.chmod(0o600)

    os.environ["GNUPGHOME"] = os.path.dirname(keyfile)
    exit_code = dotfiles.GPG.add_batch_key(keyfile)
    assert exit_code == 0

    return recipient
