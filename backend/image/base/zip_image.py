import zipfile
import io

class ZIPImgInfo:
    def __init__(self, zip_path):
        self._zip_file = zipfile.ZipFile(zip_path, 'r')

    def close(self):
        self._zip_file.close()

    def read(self, file_name):
        with self._zip_file.open(file_name) as file:
            return file.read()

    def get_size(self, file_name):
        return self._zip_file.getinfo(file_name).file_size
