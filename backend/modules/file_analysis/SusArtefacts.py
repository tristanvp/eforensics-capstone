import pytsk3
import hashlib
import time
from dd_image import DDImgInfo  # Import DDImgInfo from the external module

def return_file_properties(fs_object, file_number):
    try:
        file_properties = {
            "no": file_number,
            "name": fs_object.info.name.name.decode('utf-8'),
            "path": fs_object.info.meta.addr,  # Inode number as a substitute for path in a disk image
            "created": time.ctime(fs_object.info.meta.crtime),
            "accessed": time.ctime(fs_object.info.meta.atime),
            "modified": time.ctime(fs_object.info.meta.mtime),
            "bytes": fs_object.info.meta.size,
            "md5": None
        }

        # MD5 hash calculation
        md5_hash = hashlib.md5()
        file_size = fs_object.info.meta.size

        if file_size > 0:
            file_content = fs_object.read_random(0, file_size)
            md5_hash.update(file_content)
            file_properties["md5"] = md5_hash.hexdigest()

        return file_properties
    except Exception as e:
        print(f"Error retrieving properties for file: {fs_object.info.name.name.decode('utf-8')}, Error: {str(e)}")
        return None

def list_suspicious_files(img_info, partition_start, suspicious_types):
    file_system = pytsk3.FS_Info(img_info, offset=partition_start)
    directory = file_system.open_dir("/")
    suspicious_files = []
    file_number = 1

    for fs_object in directory:
        if fs_object.info.name.name.decode('utf-8').lower().endswith(tuple(suspicious_types)):
            file_properties = return_file_properties(fs_object, file_number)
            if file_properties:
                suspicious_files.append(file_properties)
                file_number += 1

    return suspicious_files

# Path to the .dd file
image_file = "D:\TestDrives\lab3\lab3.dd"

# Define suspicious file types
suspicious_types = ['.exe', '.dll', '.bat', '.ps1', '.sh']

# Load the image using the DDImgInfo class from dd_image.py
img_info = DDImgInfo(image_file)

# You might need to adjust the partition_start depending on your image. Usually, it's 0 for the first partition.
partition_start = 32256  # Start of the partition (offset)

# Find and list suspicious files with their properties
suspicious_files_and_properties = list_suspicious_files(img_info, partition_start, suspicious_types)

# Print the results
print("Suspicious Files and Properties:")
for file_info in suspicious_files_and_properties:
    print(file_info)
