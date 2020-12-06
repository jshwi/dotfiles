"""
tests.dotfiles_test.conftest
============================
"""
import os
import pathlib
import sys

import dotfiles

# noinspection PyPackageRequirements
import pytest

DOTFILES = ".dotfiles"
CONFIG = ".config"


@pytest.fixture(name="monkeypatch_home", autouse=True)
def fixture_monkeypatch_default(tmpdir, monkeypatch, entry_point):
    """Patch ``os.path.expanduser`` to treat the ``HOME`` shorthand of
    ``~/`` as ``tmpdir``.

    :param tmpdir:      The temporary directory ``pytest`` fixture.
    :param monkeypatch: The monkeypatch ``pytest`` fixture.
    :param entry_point: The "entry point" set for testing.
    """

    def expanduser(path):
        return path.replace("~/.", f"{tmpdir}/.")

    monkeypatch.setattr(os.path, "expanduser", expanduser)
    sys.argv = [entry_point]


@pytest.fixture(name="mock_constants", autouse=True)
def fixture_mock_constants(tmpdir):
    """Run the install process and return it's output stripped of any
    ANSI escaped color codes. The returned output can be used or ignored
    to control the stream of stdout/ stderr.

    :param tmpdir: The temporary directory ``pytest`` fixture.
    """
    _dotfiles = {
        dotfiles.install: {
            "HOME": str(tmpdir),
            "CONFIGDIR": os.path.join(str(tmpdir), CONFIG, __name__),
            "CONFIG": os.path.join(
                str(tmpdir), CONFIG, __name__, __name__ + ".yaml"
            ),
            "SOURCE": os.path.join(str(tmpdir), DOTFILES, "src"),
        },
        dotfiles.mkarchive: {"HOME": str(tmpdir)},
    }
    for module, obj in _dotfiles.items():
        for key, value in obj.items():
            setattr(module, key, value)


@pytest.fixture(name="suffix")
def fixture_suffix():
    """Get the accurate timestamp from ``dotfiles.SUFFIX`` so that there
    is no discrepancy between the test time and the module's time.

    :return: Timestamp to be appended to backed up files.
    """
    return dotfiles.SUFFIX


@pytest.fixture(name="recipient")
def fixture_recipient(tmpdir):
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
