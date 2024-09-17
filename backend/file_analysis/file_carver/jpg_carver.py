import os
from supporters import supporter

def find_jpeg_headers(data, markers):
    """Find all occurrences of JPEG markers in the data.

    Args:
        data (bytes): The binary data to search.
        markers (list): List of JPEG markers to look for.

    Returns:
        list of int: List of offsets where markers were found.
    """
    offsets = []
    for marker in markers:
        offset = 0
        while offset < len(data):
            offset = data.find(marker, offset)
            if offset == -1:
                break
            offsets.append(offset)
            offset += 2  # Move past this marker
    return offsets


def predict_cluster_size(data, cluster_sizes, markers):
    """Predict cluster size using JPEG header matching.

    Args:
        data (bytes): The binary data to search.
        cluster_sizes (list): List of cluster sizes to test.
        markers (list): List of JPEG markers to look for.

    Returns:
        dict: Dictionary with cluster sizes and detailed info about offsets.
    """
    results = {size: [] for size in cluster_sizes}
    offsets = find_jpeg_headers(data, markers)

    for size in cluster_sizes:
        for offset in offsets:
            det_value = offset % size
            if det_value == 0:
                results[size].append(offset)
    return results

# this function takes written arguments and carves the files based on input
def detect_files(data, filename, sof, eof, sof_mem_bytes, eof_mem_bytes, output_file_type, output_dir, offsets):
    with open(filename, "rb") as binary_file:
        sof_stack = list()  # stack to store SOFs
        file_byte = binary_file.read(1)
        memory_counter = 0  # points to current memory location
        while file_byte:
            file_byte = binary_file.read(1)
            memory_counter += 1
            probable_sof = data[memory_counter:memory_counter + sof_mem_bytes]
            probable_eof = data[memory_counter:memory_counter + eof_mem_bytes]
            if probable_sof == sof:
                sof_stack.append(memory_counter)
            if probable_eof == eof:
                if len(sof_stack) != 0 and sof_stack[-1] < memory_counter:
                    # offsets arg is the possible starting offset of the sector containing jpg file
                    # one sector - one file
                    # this checks whether the found starting offsets are in the likely starting offsets list
                    if offsets is not None:
                        if sof_stack[-1] not in offsets:
                            sof_stack.pop()
                            continue
                    file_data = data[sof_stack[-1]:memory_counter + eof_mem_bytes]
                    supporter.save_carved_file(file_data, output_dir, sof_stack[-1], output_file_type)
                    sof_stack.pop()

def detect_jpeg_files(data, filename, offsets, output_dir):
    sof = b'\xff\xd8\xff'
    eof = b'\xff\xd9'
    sof_mem_bytes = 3
    eof_mem_bytes = 2
    output_file_type = "jpg"
    detect_files(data, filename, sof, eof, sof_mem_bytes, eof_mem_bytes, output_file_type, output_dir, offsets)


# this function reads a binary file and stores its data for further use
def read_file(filename):
    if os.path.isfile(filename):
        with open(filename, "rb") as binary_file:
            data = binary_file.read()
        return data
    else:
        print("File not found")
        exit()


def jpg_carve(filename, output_dir):
    data = read_file(filename)
    cluster_sizes = [512, 1024, 2048, 4096, 8192]
    markers = [b'\xFF\xD8', b'\xFF\xE0', b'\xFF\xE1',
        b'\xFF\xE2', b'\xFF\xC4', b'\xFF\xDB']
    results = predict_cluster_size(data, cluster_sizes, markers)
    possible_starting_offsets = []
    for value in results.values():
        possible_starting_offsets += value
    print(possible_starting_offsets)
    detect_jpeg_files(data, filename, possible_starting_offsets, output_dir)