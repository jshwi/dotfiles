"""
mkarchive
"""
import argparse
import datetime
import os
import pathlib
import tarfile

HOME = str(pathlib.Path.home())
DATE = datetime.date.today().strftime("%Y/%m/%d")
TIME = datetime.datetime.now().strftime("%H:%M:%S")


class Parser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(prog="mkarchive")
        self._add_arguments()
        self._args = self.parse_args()
        self.path = self._args.path
        self.dest = self._args.dest

    def _add_arguments(self):
        self.add_argument(
            "path", metavar="PATH", action="store", help="path to archive"
        )
        self.add_argument(
            "-d",
            "--dest",
            action="store",
            default=os.path.join(HOME, "Documents", "Archive"),
            help="destination dir for archive",
        )


def mk_tarfile(infile, outfile):
    with tarfile.open(outfile, "w:gz") as tar:
        if os.path.isdir(infile):
            dircontents = [os.path.join(infile, i) for i in os.listdir(infile)]
        else:
            dircontents = [infile]
        for content in dircontents:
            tar.add(content)


class DirInfo:
    def __init__(self, path):
        self.list = path.split(os.sep)[1:]
        self.old = f"/{self.list.pop(0)}"
        self.new = None

    def _build_new_path(self, _dir):
        if self.new is not None:
            return os.path.join(self.new, _dir)
        return _dir

    def collate_info(self):
        for _dir in self.list:
            test_dir = os.path.join(self.old, _dir)
            if os.path.isdir(test_dir):
                self.old = test_dir
            else:
                self.new = self._build_new_path(_dir)

    def get_info(self):
        return self.old, self.new


def main():
    parser = Parser()
    dst_path = os.path.join(parser.dest, DATE)
    infile_dir = os.path.dirname(parser.path)
    infile_name = os.path.basename(parser.path)
    archive_name = f"{TIME}.{infile_name}.tar.gz"
    archive_path = os.path.join(infile_dir, archive_name)
    full_path = os.path.join(dst_path, archive_name)
    dir_info = DirInfo(dst_path)

    dir_info.collate_info()

    old, new = dir_info.get_info()

    if new is not None:
        print(f"Adding {new}/ to {old}")

    pathlib.Path(dst_path).mkdir(parents=True, exist_ok=True)

    print("Making archive")
    mk_tarfile(parser.path, archive_name)
    print(f". created {archive_name}")

    print("Storing archive")
    os.rename(archive_path, full_path)
    print(f". {archive_name} -> {full_path.replace(HOME, '~')}")

    print("Done")


if __name__ == "__main__":
    main()
