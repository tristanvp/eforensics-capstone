import hashlib, os

# this function creates a hash of a given file and stores it in hash.txt along with the starting offset
def save_hash_to_file(recovered_file, start_offset):
    hash_recovered_file = hashlib.md5()
    with open(os.path.join("output", recovered_file), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_recovered_file.update(chunk)
    hash_of_file = hash_recovered_file.hexdigest()  # create a hash
    with open(os.path.join("output", "hash.txt"), "a") as hash_file:
        hash_file.write(f"File: {recovered_file}\n")
        hash_file.write(f"Start Offset: {start_offset}\n")
        hash_file.write(f"MD5 Hash: {hash_of_file}\n\n") 

# Save the carved file to the output directory.
def save_carved_file(carved_data, output_dir, start_offset, output_filetype):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"Recovered_{start_offset}.{output_filetype}"
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "wb") as f:
        f.write(carved_data)
    save_hash_to_file(filename, start_offset)
    print(f"Carved {output_filetype} saved as {filename} with size {os.path.getsize(f'{output_dir}/' + filename)} bytes.")