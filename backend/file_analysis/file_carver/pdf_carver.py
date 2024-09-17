import os, sys, hashlib
from supporters import supporter

"""
link to the research: https://eudl.eu/pdf/10.1007/978-3-642-19513-6_12
"""

def find_pdf_header(data):
    """Find the PDF header signature (%PDF) and return the offset."""
    header_signature = b'%PDF'
    offset = data.find(header_signature)
    return offset

def check_pdf_version(data, offset):
    """Check the PDF version number at the specified offset."""
    version_number = data[offset + 5:offset + 8]  # Extract version number from file offset 6-8
    try:
        version_float = float(version_number.decode('utf-8'))
        return version_float
    except ValueError:
        return None

def is_linearized(data, offset):
    """Check if the PDF is linearized by searching for the 'Linearized' string."""
    linearized_str = b'Linearized'
    return data[offset:offset + 1024].find(linearized_str) != -1  # Search within the first few bytes

def extract_length_from_linearized(data, offset):
    """Extract the length of the file if it is linearized."""
    l_tag = b'/L '
    l_offset = data.find(l_tag, offset)
    if l_offset != -1:
        length_start = l_offset + len(l_tag)
        length_end = data.find(b'/', length_start)  # Find the end of the length value
        length_str = data[length_start:length_end].decode('utf-8').strip()
        try:
            return int(length_str)
        except ValueError:
            return None
    return None

def find_pdf_footer(data, start_offset):
    """Search for the footer signature (%%EOF) from the start offset."""
    footer_signature = b'%%EOF'
    footer_offset = data.find(footer_signature, start_offset)
    return footer_offset

def detect_pdf_files(data, output_dir, user_specified_size=1000000):
    """Carve the PDF file based on the algorithm steps."""
    header_offset = find_pdf_header(data)
    if header_offset == -1:
        print("PDF header not found.")
        return

    version_number = check_pdf_version(data, header_offset)
    if version_number is None or version_number <= 1.1:
        print(f"Unsupported or invalid PDF version: {version_number}")
        return

    print(f"PDF version: {version_number}")

    if is_linearized(data, header_offset):
        print("Linearized PDF detected.")
        file_size = extract_length_from_linearized(data, header_offset)
        if file_size:
            print(f"Carving linearized PDF of size {file_size} bytes.")
            carved_data = data[header_offset:header_offset + file_size]
            supporter.save_carved_file(carved_data, output_dir, header_offset, 'pdf')
            return
        else:
            print("Unable to determine file size from linearized data.")

    print("Searching for footer signature...")
    footer_offset = find_pdf_footer(data, header_offset)
    if footer_offset == -1:
        print("PDF footer not found. Searching until user-specified file size is reached.")
        if user_specified_size:
            carved_data = data[header_offset:header_offset + user_specified_size]
            supporter.save_carved_file(carved_data, output_dir, header_offset, 'pdf')
        else:
            print("No user-specified size provided.")
    else:
        carved_data = data[header_offset:footer_offset + len(b'%%EOF')]
        supporter.save_carved_file(carved_data, output_dir, header_offset, 'pdf')

# Example usage
def pdf_carve(filename, output_dir):
    with open(filename, 'rb') as f:
        data = f.read()
    detect_pdf_files(data, output_dir)
