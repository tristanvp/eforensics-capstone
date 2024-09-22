import hashlib, os, json

class DriveHash:
    def __init__(self, file_path, fs_object=None):
        self.file_path = file_path
        self.fs_object = fs_object

    def sha1_hash(self):
        """Calculates the SHA1 hash of a file accessed directly from image."""
        hash_sha1 = hashlib.sha1()
        file_size = self.fs_object.info.meta.size
        read_offset = 0
        buffer_size = 1024 * 1024  # 1 MB buffer

        while read_offset < file_size:
            if file_size - read_offset < buffer_size:
                buffer = self.fs_object.read_random(read_offset, file_size - read_offset)
            else:
                buffer = self.fs_object.read_random(read_offset, buffer_size)
            
            if buffer:
                hash_sha1.update(buffer)
                read_offset += len(buffer)
            else:
                break
        
        return hash_sha1.hexdigest()
    
    def md5_hash(self):
        """Calculates the MD5 hash of a file accessed directly from image."""
        hash_md5 = hashlib.md5()
        file_size = self.fs_object.info.meta.size
        read_offset = 0
        buffer_size = 1024 * 1024  # 1 MB buffer

        while read_offset < file_size:
            if file_size - read_offset < buffer_size:
                buffer = self.fs_object.read_random(read_offset, file_size - read_offset)
            else:
                buffer = self.fs_object.read_random(read_offset, buffer_size)
            
            if buffer:
                hash_md5.update(buffer)
                read_offset += len(buffer)
            else:
                break
        
        return hash_md5.hexdigest()
    
    def direct_md5_hash(self):
        """Calculates the MD5 hash of a file accessed directly from system."""
        hasher = hashlib.md5()
        with open(self.file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def direct_sha1_hash(self):
        """Calculates the SHA1 hash of a file accessed directly from system."""
        hasher = hashlib.sha1()
        with open(self.file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def save_hash_to_file(self, partition=0, start_offset=None, output_dir='output', output_filename='hashes.txt'):
        # Create a dictionary to store the file details
        if self.fs_object == None:
            md5_hash = self.direct_md5_hash
            sha1_hash = self.direct_sha1_hash
        else:
            md5_hash = self.md5_hash
            sha1_hash = self.sha1_hash
            
        file_details = {
            "Partition": partition,
            "File": self.file_path,
            "Start Offset": start_offset,
            "MD5 Hash": md5_hash,
            "SHA1 Hash": sha1_hash
        }

        # Convert the dictionary to a JSON object
        json_output = json.dumps(file_details, indent=4)
        if not (os.path.exists(output_dir)):
            os.makedirs(output_dir)
            
        with open(os.path.join(output_dir, output_filename), "a") as hash_file:
            hash_file.write(json_output)