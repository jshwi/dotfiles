import os
import sys
import unittest.mock

import dotfiles

# noinspection PyPackageRequirements
import pytest


def assert_unencrypted_files(test_dir, tarfile, gpgfile):
    assert os.path.isdir(test_dir)
    assert not os.path.exists(tarfile)
    assert not os.path.exists(gpgfile)


def assert_encrypted_files(test_dir, tarfile, gpgfile):
    assert not os.path.isdir(test_dir)
    assert not os.path.exists(tarfile)
    assert os.path.exists(gpgfile)


def test_under_the_hood(crypt_test_files, recipient):
    test_dir, tarfile, gpgfile = crypt_test_files
    tar = dotfiles.Tar(test_dir, tarfile)
    tar.compress()
    gpg = dotfiles.GPG(tarfile, gpgfile)
    exit_code = gpg.encrypt(recipient)
    assert exit_code == 0
    assert os.path.exists(gpgfile)


def test_tar_no_file(nocolorcapsys):
    tar = dotfiles.Tar(os.path.join("no_exist_dir", "no_exist_file"))
    with pytest.raises(FileNotFoundError):
        tar.compress()
        assert (
            nocolorcapsys.stderr()
            == "[Errno 2] No such file or directory: 'no_exist_dir'"
        )


def test_encrypt_dir(crypt_test_files, recipient):
    assert_unencrypted_files(*crypt_test_files)
    test_dir, tarfile, gpgfile = crypt_test_files
    argv = [__name__, test_dir, "--recip", recipient]

    with unittest.mock.patch.object(sys, "argv", argv):
        dotfiles.cryptdir.main()

    assert_encrypted_files(test_dir, tarfile, gpgfile)


def test_decrypt_dir(crypt_test_files, recipient):
    test_encrypt_dir(crypt_test_files, recipient)
    test_dir, tarfile, gpgfile = crypt_test_files
    argv = [__name__, gpgfile, "--decrypt"]

    with unittest.mock.patch.object(sys, "argv", argv):
        dotfiles.cryptdir.main()

    assert_unencrypted_files(test_dir, tarfile, gpgfile)


def test_encrypt_with_no_recipient(nocolorcapsys, crypt_test_files):
    assert_unencrypted_files(*crypt_test_files)
    test_dir = crypt_test_files[0]
    argv = [__name__, test_dir]

    with unittest.mock.patch.object(sys, "argv", argv):

        with pytest.raises(SystemExit):
            dotfiles.cryptdir.main()

    out = nocolorcapsys.stderr().splitlines()
    assert out[0] == "Cannot encrypt directory without a recipient"
