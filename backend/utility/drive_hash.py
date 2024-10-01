import hashlib, os, json, pytsk3
from definitions import ROOT_DIR

class DriveHash:
    def __init__(self, file_path: list[str] | str, fs_object: list[pytsk3.File] | pytsk3.File = None, partitions_index: list[int] = list[0]):
        if type(file_path) != list and type(fs_object) != list:
            self.file_path = [file_path]
            self.fs_object = [fs_object]
        else:    
            self.file_path = file_path
            self.fs_object = fs_object
            
        self.partitions_index = partitions_index

    def sha1_hash(self, fs_object: pytsk3.File):
        """Calculates the SHA1 hash of a file accessed directly from image."""
        hash_sha1 = hashlib.sha1()
        file_size = fs_object.info.meta.size
        read_offset = 0
        buffer_size = 1024 * 1024  # 1 MB buffer

        while read_offset < file_size:
            if file_size - read_offset < buffer_size:
                buffer = fs_object.read_random(read_offset, file_size - read_offset)
            else:
                buffer = fs_object.read_random(read_offset, buffer_size)
            
            if buffer:
                hash_sha1.update(buffer)
                read_offset += len(buffer)
            else:
                break
        
        return hash_sha1.hexdigest()
    
    def md5_hash(self, fs_object: pytsk3.File):
        """Calculates the MD5 hash of a file accessed directly from image."""
        hash_md5 = hashlib.md5()
        file_size = fs_object.info.meta.size
        read_offset = 0
        buffer_size = 1024 * 1024  # 1 MB buffer

        while read_offset < file_size:
            if file_size - read_offset < buffer_size:
                buffer = fs_object.read_random(read_offset, file_size - read_offset)
            else:
                buffer = fs_object.read_random(read_offset, buffer_size)
            
            if buffer:
                hash_md5.update(buffer)
                read_offset += len(buffer)
            else:
                break
        
        return hash_md5.hexdigest()
    
    def direct_md5_hash(self, file_path: str):
        """Calculates the MD5 hash of a file accessed directly from system."""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def direct_sha1_hash(self, file_path: str):
        """Calculates the SHA1 hash of a file accessed directly from system."""
        hasher = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def save_hash_to_file(self, start_offset=None, output_dir='output', output_filename='hashes.txt'):
        # Create a dictionary to store the file details
        fs_obj_filepath_index_list = list(zip(self.fs_object, self.file_path, self.partitions_index)) 
        is_direct_hash = False
        all_hashes = []  # Store all hashes here

        for fs_obj_filepath_index in fs_obj_filepath_index_list:
            fs_object = fs_obj_filepath_index[0]
            file_path = fs_obj_filepath_index[1]
            partition_index = fs_obj_filepath_index[2]
            
            if fs_object == None:
                md5_hash = self.direct_md5_hash(file_path)
                sha1_hash = self.direct_sha1_hash(file_path)
                is_direct_hash = True
            else:
                md5_hash = self.md5_hash(fs_object)
                sha1_hash = self.sha1_hash(fs_object)
            
            if is_direct_hash:
                file_details = {
                    "File": file_path,
                    "Start Offset": start_offset,
                    "MD5 Hash": md5_hash,
                    "SHA1 Hash": sha1_hash
                }
            else:
                file_details = {
                    "Partition": partition_index,
                    "File": file_path,
                    "Start Offset": start_offset,
                    "MD5 Hash": md5_hash,
                    "SHA1 Hash": sha1_hash
                }
            all_hashes.append(file_details) 

        # Convert the dictionary to a JSON object
        output_dir = f"{ROOT_DIR}/{output_dir}"
        if not (os.path.exists(output_dir)):
            os.makedirs(output_dir)
            
        with open(os.path.join(output_dir, output_filename), "w") as hash_file:
            # Convert the dictionary to a JSON string
            json.dump(all_hashes, hash_file, indent=4)
            hash_file.write("\n")