import dotfiles


def test_color(capsys):
    default_key = dotfiles.Colors("bad key")
    default_key.print("test")
    out = capsys.readouterr()[0].strip()
    assert out == f"\u001b[0;37;40mtest\u001b[0;0m"
