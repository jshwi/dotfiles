"""
mkarchive
"""
import argparse
import os
import pathlib

from . import HOME, DATE, TIME, Tar


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
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "path", metavar="PATH", action="store", help="path to archive"
    )
    parser.add_argument(
        "-d",
        "--dest",
        action="store",
        default=os.path.join(HOME, "Documents", "Archive"),
        help="destination dir for archive",
    )
    args = parser.parse_args()
    dst_path = os.path.join(args.dest, DATE)
    infile_dir = os.path.dirname(args.path)
    infile_name = os.path.basename(args.path)
    archive_name = f"{TIME}.{infile_name}.tar.gz"
    archive_path = os.path.join(infile_dir, archive_name)
    full_path = os.path.join(dst_path, archive_name)
    dir_info = DirInfo(dst_path)
    tarobj = Tar(args.path, archive_name)

    dir_info.collate_info()

    old, new = dir_info.get_info()

    if new is not None:
        print(f"Adding {new}/ to {old}")

    pathlib.Path(dst_path).mkdir(parents=True, exist_ok=True)

    print("Making archive")
    tarobj.compress()
    print(f". created {archive_name}")

    print("Storing archive")
    os.rename(archive_path, full_path)
    print(f". {archive_name} -> {full_path.replace(HOME, '~')}")

    print("Done")
