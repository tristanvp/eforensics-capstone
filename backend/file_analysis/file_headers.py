import os
import sys

"""
Imported required libraries to find the file
"""

class fileHeader:

    def __init__(self):
        self.header = "" #Empty string for the header to be tested against
        self.filepath = r"" #Sample filepath for finding the image file
        self.file_header = "" #Empty string for the file header to be found

    def run(self, filepath):
        self.find_file(filepath) #runs the code to find the file header

    def jpeg_file(self, data):
        header = b'\xFF\xD8\xFF\xE0' #define header for a JPEG file
        if data.find(header) != -1: #searches the data for the jpeg header, if it is not found, output is -1, so if output does not equal -1, the jpeg header was found in the data
            self.file_header = "JPEG"
        else:
            self.pdf_file(data) #if the file isnt a JPEG, check if its a PDF

    def pdf_file(self, data):
        header = b'%PDF' #define header for a PDF file
        if data.find(header) != -1: #same as jpeg, but with the PDF header
            self.file_header = "PDF"
        else:
            self.zip_file(data)

    def zip_file(self, data):
        header = b'\x50\x4B\x03\x04' #define header for zip file
        if data.find(header) != -1: #same as jpeg, but with the ZIP header
            self.file_header = "ZIP"
        else:
            self.file_header = "No valid file header found" #if the header is not found, no valid header is detected so it returns the default file header message

    def find_file(self, filepath):
        with open(filepath, 'rb') as f: #opens the file at the example filepath
            data = f.read() #reads the file and inputs into the variable data
        self.jpeg_file(data) #Begins checking if data has a Jpeg header
      
    return self.file_header #return the file header for the rest of the system
