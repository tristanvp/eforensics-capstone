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

    def _has_partitions(self):
        # ZIP files do not have partitions, so return False
        return False

    def get_volume_size(self):
        # Return the total size of the ZIP file
        if self._zip_file:
            return sum(info.file_size for info in self._zip_file.infolist())
        return 0

    def get_partition_count(self):
        # ZIP files do not have partitions, so return 0
        return 0
