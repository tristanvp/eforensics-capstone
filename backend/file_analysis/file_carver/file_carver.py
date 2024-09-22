
from backend.file_analysis.file_carver.jpg_carver import *
from backend.file_analysis.file_carver.pdf_carver import *
from backend.file_analysis.file_carver.zip_carver import *

class FileCarver:
    def __init__(self, filename, output_dir):
        self.filename = filename
        self.output_dir = output_dir

    def carve(self):
        jpg_carve(self.filename, self.output_dir)
        pdf_carve(self.filename, self.output_dir)
        zip_carve(self.filename, self.output_dir)
