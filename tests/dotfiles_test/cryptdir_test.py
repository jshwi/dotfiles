"""
tests.dotfiles_test.cryptdir_test
=================================
"""
import os
import sys
import unittest.mock

import dotfiles

# noinspection PyPackageRequirements
import pytest


def assert_unencrypted_files(test_dir, tarfile, gpgfile):
    """Assert the files that should exist prior to encrypting the
    target.

    :param test_dir:    The path to the directory to be encrypted.
    :param tarfile:     The path to the compressed ``test_dir``.
    :param gpgfile:     The path to the encrypted ``tarfile``.
    """
    assert os.path.isdir(test_dir)
    assert not os.path.exists(tarfile)
    assert not os.path.exists(gpgfile)


def assert_encrypted_files(test_dir, tarfile, gpgfile):
    """Assert the files that should exist once the target has been
    encrypted.

    :param test_dir:    The path to the directory to be encrypted.
    :param tarfile:     The path to the compressed ``test_dir``.
    :param gpgfile:     The path to the encrypted ``tarfile``.
    """
    assert not os.path.isdir(test_dir)
    assert not os.path.exists(tarfile)
    assert os.path.exists(gpgfile)


def test_under_the_hood(crypt_test_files, recipient):
    """Test out the ``Tar`` class and the ``GPG`` class without running
    the module functions.

    :param crypt_test_files:    Tuple of file, tarred file and encrypted
                                file path-names.
    :param recipient:           Created a mock recipient key that can
                                be used for testing gnupg as well as
                                returning the credentials of that mock
                                user.
    """
    test_dir, tarfile, gpgfile = crypt_test_files
    tar = dotfiles.Tar(test_dir, tarfile)
    tar.compress()
    gpg = dotfiles.GPG(tarfile, gpgfile)
    exit_code = gpg.encrypt(recipient)
    assert exit_code == 0
    assert os.path.exists(gpgfile)


def test_tar_no_file(nocolorcapsys):
    """Test raising of a FileNotFoundError that should be produced when
    attempting to tar a non-existing file.

    :param nocolorcapsys: ``capsys`` with the ANSI codes removed.
    """
    tar = dotfiles.Tar(os.path.join("no_exist_dir", "no_exist_file"))
    with pytest.raises(FileNotFoundError):
        tar.compress()
        assert (
            nocolorcapsys.stderr()
            == "[Errno 2] No such file or directory: 'no_exist_dir'"
        )


def test_encrypt_dir(crypt_test_files, recipient):
    """Test encryption of a directory when using the ``cryptdir``
    module.

    :param crypt_test_files:    Tuple of file, tarred file and encrypted
                                file path-names.
    :param recipient:           Created a mock recipient key that can
                                be used for testing gnupg as well as
                                returning the credentials of that mock
                                user.
    """
    assert_unencrypted_files(*crypt_test_files)
    test_dir, tarfile, gpgfile = crypt_test_files
    argv = [__name__, test_dir, "--recip", recipient]

    with unittest.mock.patch.object(sys, "argv", argv):
        dotfiles.cryptdir.main()

    assert_encrypted_files(test_dir, tarfile, gpgfile)


def test_decrypt_dir(crypt_test_files, recipient):
    """Test decryption of an encrypted dir when using the ``cryptdir``
    module with  the -d/--decrypt option.

    :param crypt_test_files:    Tuple of file, tarred file and encrypted
                                file path-names.
    :param recipient:           Created a mock recipient key that can
                                be used for testing gnupg as well as
                                returning the credentials of that mock
                                user.
    """
    test_encrypt_dir(crypt_test_files, recipient)
    test_dir, tarfile, gpgfile = crypt_test_files
    argv = [__name__, gpgfile, "--decrypt"]

    with unittest.mock.patch.object(sys, "argv", argv):
        dotfiles.cryptdir.main()

    assert_unencrypted_files(test_dir, tarfile, gpgfile)


def test_encrypt_with_no_recipient(nocolorcapsys, crypt_test_files):
    """Test encryption of a directory when using the ``cryptdir``
    module when not also passing the -r/--recipient option which is
    mandatory for encrypting but not the same for decrypting.

    Ensure the correct error message and help options are also
    displayed.

    :param nocolorcapsys:       ``capsys`` with the ANSI codes removed.
    :param crypt_test_files:    Tuple of file, tarred file and encrypted
                                file path-names.
    """
    assert_unencrypted_files(*crypt_test_files)
    test_dir = crypt_test_files[0]
    argv = [__name__, test_dir]

    with unittest.mock.patch.object(sys, "argv", argv):

        with pytest.raises(SystemExit):
            dotfiles.cryptdir.main()

    out = nocolorcapsys.stderr().splitlines()
    assert out[0] == "Cannot encrypt directory without a recipient"
