import os
import sys #Imported libraries to find the file

file_header = ""
filepath = r"" #Sample filepath for finding the image file
header = "" #Empty string for the header to be tested against

def jpeg_file(data):
    header = b'\xFF\xD8\xFF\xE0' #define header for a JPEG file
    if data.find(header) != -1: ##searches the data for the jpeg header, if it is not found, output is -1, so if output does not equal -1, the jpeg header was found in the data
        file_header = "JPEG"
        print_file(file_header)
        return file_header
    else:
        pdf_file(data) #if the file isnt a JPEG, check if its a PDF


def pdf_file(data):
    header = b'%PDF' #define header for a PDF file
    if data.find(header) != -1:#same as jpeg, but with the PDF header
        file_header = "PDF"
        print_file(file_header)
        return file_header
    else:
        zip_file(data)

def zip_file(data):
    header = b'\x50\x4B\x03\x04'#define header for zip file
    if data.find(header) != -1:#same as jpeg, but with the ZIP header
        file_header = "ZIP"
        print_file(file_header)
        return file_header
    else:
        print("No valid file header found")#if the header is not found, no valid header is detected so it returns the default file header message

def find_file(filepath):
    with open(filepath, 'rb') as f: #opens the file at the example filepath
        data = f.read() #reads the file and inputs into the variable data
    jpeg_file(data)#Begins checking if data has a Jpeg header

def print_file(file_header): #test for checking if file header is found
    print("The file header is: ")
    print(file_header)
    
    
find_file(filepath) #runs the code to find the file header


    


