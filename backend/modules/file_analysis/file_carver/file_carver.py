import jpg_carver, pdf_carver, zip_carver
import sys


class FileCarver:
    def __init__(self, filename, output_dir):
        self.filename = filename
        self.output_dir = output_dir

    def jpg_carve(self):
       jpg_carver.jpg_carve(self.filename, self.output_dir) 
    
    def pdf_carve(self):
        pdf_carver.pdf_carve(self.filename, self.output_dir)

    def zip_carve(self):
        zip_carver.zip_carve(self.filename, self.output_dir)
    
    def carve(self):
        jpg_carver.jpg_carve(self.filename, self.output_dir)
        pdf_carver.pdf_carve(self.filename, self.output_dir)
        zip_carver.zip_carve(self.filename, self.output_dir)
