# Manages overall file operations
# Defines high level methods to readc data 
# Defines Image class structure

from image_mount import ImageMount
from drive_hash import DriveHash

class Image:

    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type
        self.mount = ImageMount(file_path, file_type)
        self.hashing = DriveHash(file_path)

    def read(self, offset, size):
        return self.mount.read(offset, size)
    
    def close(self):
        self.mount.close()
    
    def get_size(self):
        return self.mount.get_size()

    def md5_hash(self):
        return self.hashing.md5_hash()

    def sha1_hash(self):
        return self.hashing.sha1_hash()
