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

    def jpeg_file(self, data):
        header = b'\xFF\xD8\xFF\xE0' #define header for a JPEG file
        if data.find(header) != -1: #searches the data for the jpeg header, if it is not found, output is -1, so if output does not equal -1, the jpeg header was found in the data
            self.file_header = "JPEG"
        else:
            self.pdf_file(data) #if the file isnt a JPEG, check if its a PDF

    def pdf_file(self, data):
        header = b'%PDF' #define header for a PDF file
        if data.find(header) != -1: #same as above, but with the PDF header
            self.file_header = "PDF"
        else:
            self.zip_file(data)

    def zip_file(self, data):
        header = b'\x50\x4B\x03\x04' #define header for zip file
        if data.find(header) != -1: #same as above, but with the ZIP header
            self.file_header = "ZIP"
        else:
            self.rtf_file(data) #if the header is not found, check for log file header
    def rtf_file(self, data):
        header = b'\x7B\x5C\x72\x74\x66\x31' #define header for rtf file
        if data.find(header) != -1: #same as above, but with the rtf header
            self.file_header = "RTF"
        else:
            self.dat_file(data) #if the header is not found, search for dat file header
    def dat_file(self, data):
        header = b'\x72\x65\x67\x66' #define header for dat file
        if data.find(header) != -1: #same as above, but with the dat header
            self.file_header = "DAT"
        else:
            self.dll_file(data) #if the header is not found, search for dll file header
    
    def dll_file(self, data):
        header = b'\x4D\x5A' #define header for dll file
        if data.find(header) != -1: #same as above, but with the dll header
            self.file_header = "DLL"
        else:
            self.file_header = "No valid file header found" #if the header is not found, no valid header is detected so it returns the default file header message

    def run(self, filepath):
        with open(filepath, 'rb') as f: #opens the file at the example filepath
            data = f.read() #reads the file and inputs into the variable data
        self.jpeg_file(data) #Begins checking if data has a Jpeg header
    
    def get_file_header(self):
        return self.file_header #return the file header for the rest of the system