import hashlib
import os

def save_hash_to_file(file, start_offset=0):
    hash_file = hashlib.md5()
    
    # Calculate MD5 hash
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_file.update(chunk)
    hash_of_file = hash_file.hexdigest()  # create a hash

    # Ensure the output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Write hash to file
    hash_file_path = os.path.join(output_dir, "hash.txt")
    with open(hash_file_path, "a") as hash_file:
        hash_file.write(f"File: {file}\n")
        hash_file.write(f"Start Offset: {start_offset}\n")
        hash_file.write(f"MD5 Hash: {hash_of_file}\n\n") 