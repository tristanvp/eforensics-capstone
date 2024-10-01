from backend.file_analysis.file_carver.jpg_carver import *
from backend.file_analysis.file_carver.pdf_carver import *
from backend.file_analysis.file_carver.zip_carver import *
from backend.file_analysis.file_carver.utils import *

# file carving is performed on the unallocated space of the forensic image

class FileCarver:
    def __init__(self, filenames: list, output_dir: str):
        self.filenames = filenames # refer to the file containing data of the unallocated space
        self.output_dir = output_dir
        self.carved_files = []

    def carve(self):
        carvers = [pdf_carve, jpg_carve, zip_carve]
        for filename in self.filenames:
            print(f"[+] Performing file carving on {filename}")
            for carve in carvers:
                carved_files = carve(filename, self.output_dir)
                if carved_files:
                    self.carved_files.extend(carved_files)

        return metadata_carved_files(self.carved_files)
        
        
