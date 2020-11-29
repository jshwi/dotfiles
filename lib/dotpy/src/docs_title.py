import argparse

from . import classy, env


class EditTitle(classy.TextIO):
    """Take the ``path`` and ``replace`` argument from the commandline
    and reformat the README whilst returning the original title to
    the parent process.

    :param path:    Path to the ``README.rst`` file.
    :param replace: String to replace the readme title with.
    """

    def __init__(self, path, replace):
        super().__init__(path)
        self.path = path
        self.replace = replace
        self.underline = len(replace) * "="
        self.title = None

    def read_file(self):
        """Read the ``README.rst`` file. Keep the original title.

        Replace the original title and underline with the new
        ``replace provided``.
        """
        self.title = self.lines[0]
        self.lines[0] = self.replace
        self.lines[1] = self.underline

    def replace_title(self):
        """Read, save the old title as an instance attribute, replace
        and write.
        """
        self.read_file()
        self.write()


def docs_title():
    """Replace the <PACKAGENAME> title in ``README.rst`` with README
    for rendering ``Sphinx`` documentation links.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--replace", action="store", help="replacement title"
    )
    args = parser.parse_args()
    edit = EditTitle(env.READMEPATH, args.replace)
    edit.replace_title()
    print(edit.title)
