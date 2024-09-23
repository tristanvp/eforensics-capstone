import zipfile

class ZIPImgInfo:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self._zip_file = None
        self.open()  # Open the ZIP file when initializing

    def open(self):
        if not self._zip_file:
            self._zip_file = zipfile.ZipFile(self.zip_path, 'r')

    def close(self):
        if self._zip_file:
            self._zip_file.close()
            self._zip_file = None
