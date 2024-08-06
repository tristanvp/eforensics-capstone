import os
import platform
import time
import hashlib
import pprint

def is_hidden(filepath):
    if platform.system() == "Windows":
        if os.path.basename(filepath).startswith("."):
            return True
        try:
            attrs = os.stat(filepath).st_file_attributes
            return bool(attrs & 2)  # Check if hidden attribute is set
        except AttributeError:
            return False
    # Hidden file checker if run on non-Unix based OS
    else:
        return os.path.basename(filepath).startswith(".")

def list_hidden_files(directory):
    hidden_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if is_hidden(full_path):
                hidden_files.append(full_path)

    # If no hidden files are found, print message
    if len(hidden_files) == 0:
        print("Directory Clear")
    return hidden_files

def return_file_properties(file_path):
    try:
        # Get file attributes
        file_stat = os.stat(file_path)

        # Extract relevant information
        file_number = len(hidden_files_and_properties) + 1
        file_name = os.path.basename(file_path)
        file_full_path = os.path.abspath(file_path)
        created_time = time.ctime(file_stat.st_ctime)
        last_accessed_time = time.ctime(file_stat.st_atime)
        last_modified_time = time.ctime(file_stat.st_mtime)
        file_size_bytes = file_stat.st_size
        inode_number = file_stat.st_ino

        # MD5 hash calculation
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)
        file_md5 = md5_hash.hexdigest()

        # Create a dictionary with file properties
        file_properties = {
            "no": file_number,
            "name": file_name,
            "path": file_full_path,
            "created": created_time,
            "accessed": last_accessed_time,
            "modified": last_modified_time,
            "bytes": file_size_bytes,
            "inode": inode_number,
            "md5": file_md5
        }
        return file_properties
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

# Compilation of list of discovered hidden files according to given directory 
directory_to_search = r"C:\Users\txvpa\OneDrive\Desktop" # Can be swapped out to a dynamic variable
hidden_files_and_properties = []
hidden_files = list_hidden_files(directory_to_search)
for i in hidden_files:
    hidden_files_and_properties.append(return_file_properties(i))

# File output testing 
pprint.pprint(hidden_files_and_properties)