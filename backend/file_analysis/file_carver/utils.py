import os
from backend.utility.drive_hash import DriveHash
from datetime import datetime
import json
from definitions import ROOT_DIR

# Save the carved file to the output directory.
def save_carved_file(carved_data, output_dir, start_offset, output_filetype):
    output_dir = f"{ROOT_DIR}/{output_dir}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"Recovered_{start_offset}.{output_filetype}"
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "wb") as f:
        f.write(carved_data)
    DriveHash(file_path).save_hash_to_file(start_offset, output_dir, output_filename="carved_file_hashes.json")
    print(f"Carved {output_filetype} saved as {filename} with size {os.path.getsize(f'{output_dir}/' + filename)} bytes.") 
    return f'{output_dir}/' + filename
    
# this function reads a binary file and stores its data for further use
def read_file(filename):
    if os.path.isfile(filename):
        with open(filename, "rb") as binary_file:
            data = binary_file.read()
        return data
    else:
        print("File not found")
        exit()

def get_file_metadata(file_path):
    try:
        file_stat = os.stat(file_path)
        return {
            'filename': os.path.basename(file_path),
            'inode': file_stat.st_ino,
            'path': os.path.abspath(file_path),
            'created_day': datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'accessed_day': datetime.fromtimestamp(file_stat.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified_day': datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
    except FileNotFoundError:
        return None

def metadata_carved_files(carved_files):
    # Simulate the carving process, which gives us the carved file paths
    carved_files_metadata = []

    # Loop through the list of carved files to capture metadata
    for file_path in carved_files:
        file_metadata = get_file_metadata(file_path)
        if file_metadata:
            carved_files_metadata.append(file_metadata)
    return carved_files_metadata