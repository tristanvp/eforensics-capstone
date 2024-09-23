import struct, re
from backend.file_analysis.file_carver.utils import *

def find_zip_signatures(data):
    # ZIP local file header signature (PK\x03\x04)
    local_file_header_signature = b'\x50\x4B\x03\x04'
    # Central directory file header signature (PK\x01\x02)
    central_dir_header_signature = b'\x50\x4B\x01\x02'
    # End of central directory signature (PK\x05\x06)
    end_central_dir_signature = b'\x50\x4B\x05\x06'
    
    # Find all occurrences of the local file header signature
    local_file_headers = [m.start() for m in re.finditer(local_file_header_signature, data)]
    
    # Find all occurrences of the central directory file header signature
    central_dir_headers = [m.start() for m in re.finditer(central_dir_header_signature, data)]
    
    # Find all occurrences of the end of central directory signature
    end_central_dirs = [m.start() for m in re.finditer(end_central_dir_signature, data)]
    
    return local_file_headers, central_dir_headers, end_central_dirs

def extract_zip_files(data, local_file_headers, end_central_dirs):
    zip_files = []
    offsets = []
    
    for start in local_file_headers:
        # Attempt to find the nearest end of central directory signature after this header
        end = min((e for e in end_central_dirs if e > start), default=None)
        if end:
            # Include the size of the End of Central Directory Record
            end += struct.calcsize('<IHHHHIIH')
            zip_files.append(data[start:end])
            offsets.append(start)
    
    return zip_files, offsets

def zip_carve(filename, output_dir):
    print("Starting ZIP Carving: ")
    data = read_file(filename)
    local_file_headers, _, end_central_dirs = find_zip_signatures(data)
    
    if not local_file_headers or not end_central_dirs:
        print("No ZIP files found.")
        return

    zip_files, starting_offsets = extract_zip_files(data, local_file_headers, end_central_dirs)

    for i, zip_file in enumerate(zip_files):
        starting_offset = starting_offsets[i]
        save_carved_file(zip_file, output_dir, starting_offset, "zip")