import os
import time
import hashlib

class MetadataExtractor:
    def __init__(self, entry, filepath, file_number):
        self.entry = entry
        self.filepath = filepath
        self.file_number = file_number

    def extract_metadata(self, true_extension=None):
        try:
            # Get file metadata from pytsk3 entry
            created_time = time.ctime(self.entry.info.meta.crtime)
            last_accessed_time = time.ctime(self.entry.info.meta.atime)
            last_modified_time = time.ctime(self.entry.info.meta.mtime)
            file_size_bytes = self.entry.info.meta.size
            inode_number = self.entry.info.meta.addr

            # MD5 hash calculation
            md5_hash = hashlib.md5()
            file_data = self.entry.read_random(0, self.entry.info.meta.size)
            md5_hash.update(file_data)
            file_md5 = md5_hash.hexdigest()

            # Create a dictionary with file properties
            file_properties = {
                "no": self.file_number,  # Added file number for sequential order
                "name": os.path.basename(self.filepath),
                "path": os.path.abspath(self.filepath),
                "created": created_time,
                "accessed": last_accessed_time,
                "modified": last_modified_time,
                "bytes": file_size_bytes,
                "inode": inode_number,
                "md5": file_md5,
                "true_extension": true_extension  # Add true extension to metadata
            }

            return file_properties

        except Exception as e:
            print(f"Error extracting properties for {self.filepath}: {e}")
            return None
