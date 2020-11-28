import os
import tarfile


class Tar:
    def __init__(self, file, archive):
        self.file = file
        self.archive = archive

    def _compress_dir(self, tar):
        dircontents = [
            os.path.join(self.file, i) for i in os.listdir(self.file)
        ]

        for content in dircontents:
            tar.add(content)

    def compress(self):
        with tarfile.open(self.archive, "w:gz") as tar:

            if os.path.isdir(self.file):
                self._compress_dir(tar)

            elif os.path.isfile(self.file):
                tar.add(self.file)

    def extract(self):
        with tarfile.open(self.archive) as tar:
            tar.extractall()
