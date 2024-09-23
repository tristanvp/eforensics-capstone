import os
from backend.utility.drive_hash import DriveHash

# Save the carved file to the output directory.
def save_carved_file(carved_data, output_dir, start_offset, output_filetype):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"Recovered_{start_offset}.{output_filetype}"
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "wb") as f:
        f.write(carved_data)
    DriveHash(file_path).save_hash_to_file(start_offset, output_dir, output_filename="carved_file_hashes.txt")
    print(f"Carved {output_filetype} saved as {filename} with size {os.path.getsize(f'{output_dir}/' + filename)} bytes.")
    
# this function reads a binary file and stores its data for further use
def read_file(filename):
    if os.path.isfile(filename):
        with open(filename, "rb") as binary_file:
            data = binary_file.read()
        return data
    else:
        print("File not found")
        exit()