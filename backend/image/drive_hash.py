import hashlib

class DriveHash:
    def __init__(self, file_path):
        self.file_path = file_path

    def md5_hash(self):
        hasher = hashlib.md5()
        with open(self.file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def sha1_hash(self):
        hasher = hashlib.sha1()
        with open(self.file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
