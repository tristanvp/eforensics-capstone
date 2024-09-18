# backlog: add return file properties function and ability to read images using filesystem.py

import os
import io
import pytsk3
import filetype
import pathlib

# Function to open the disk image and traverse its file system
def open_image(image_file):
    # Open the disk image
    img = pytsk3.Img_Info(image_file)
    
    # Open the file system
    fs = pytsk3.FS_Info(img)
    
    # Get the root directory
    root_dir = fs.open_dir(path="/")
    
    return fs, root_dir

# Fallback file signature guessing for specific file types
def fallback_filetype(file_data, file_name):
    ext = os.path.splitext(file_name)[1].lower()
    if ext == ".jpg":
        return "image/jpeg"
    elif ext == ".rtf":
        return "application/rtf"
    elif ext == ".log":
        return "text/plain"
    elif ext == ".ini":
        return "text/plain"
    elif ext == ".dat":
        return "application/octet-stream"
    elif ext == ".dll":
        return "application/x-msdownload"
    return None

# Function to check the file signature vs file extension
def check_file_signature(entry, file_name, file_path, mismatched_files):
    try:
        # Read the file content from the image directly
        file_data = entry.read_random(0, entry.info.meta.size)

        # Use filetype to guess file signature
        kind = filetype.guess(io.BytesIO(file_data))
        
        if kind is None:
            kind = fallback_filetype(file_data, file_name)
            if kind is None:
                return  # Skip if unable to guess
            mime = kind
        else:
            mime = kind.mime

        # Get the file extension
        file_ext = os.path.splitext(file_name)[1].lower()
        true_ext = mime.split('/')[-1]

        # Compare extension with the guessed type
        if not file_ext.endswith(true_ext):
            mismatched_files.append({
                'file_name': file_name,
                'directory': file_path,
                'file_ext': file_ext,
                'true_ext': true_ext
            })
    
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")

# Function to traverse the directory and process each file
def traverse_directory(fs, directory, current_path="", visited_inodes=set(), mismatched_files=[]):
    for entry in directory:
        if not hasattr(entry, "info") or not hasattr(entry.info, "name") or not entry.info.name.name:
            continue

        file_name = entry.info.name.name.decode("utf-8")

        # Skip special files (like $MFT, $Bitmap, etc.)
        if file_name.startswith("$"):
            continue

        # Ensure entry has metadata before accessing it
        if entry.info.meta is None:
            continue

        # Check if we've already visited this inode (avoid infinite loops)
        inode = entry.info.meta.addr
        if inode in visited_inodes:
            continue
        visited_inodes.add(inode)

        # Build the current file path
        file_path = os.path.join(current_path, file_name)

        # Check if it's a regular file
        if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG:
            check_file_signature(entry, file_name, file_path, mismatched_files)

        # If it's a directory, recursively traverse it
        elif entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
            try:
                sub_directory = entry.as_directory()
                traverse_directory(fs, sub_directory, file_path, visited_inodes, mismatched_files)
            except IOError as e:
                print(f"Cannot open directory {file_name}: {e}")

    return mismatched_files

# Main function to execute the script
if __name__ == "__main__":
    # This is a test image v
    image_file = r'C:\Users\txvpa\OneDrive - Swinburne University\University\2024_Semester2\Swinburne\COS40006_ComputingTechnologyProjectB\forensics_testfiles\8-jpeg-search\8-jpeg-search.dd'
    fs, root_dir = open_image(image_file)
    mismatched_files = traverse_directory(fs, root_dir)

    # Output the list of files which has an extension that does not match its file signature
    print("\nMismatched Files:")
    for idx, file in enumerate(mismatched_files, 1):
        print(f"{idx}. File: {file['file_name']} | Directory: {file['directory']} | "
              f"Extension: {file['file_ext']} | True Extension: .{file['true_ext']}")