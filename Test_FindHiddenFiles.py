'''
Design an automated eForensics system that will conduct an eForensics analysis against a
mounted drive (static analysis) and generate a report with the discovery of hidden,
deleted, renamed, and/or carved files
'''

import os
import platform

def list_hidden_files(directory):
    hidden_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if is_hidden(full_path):
                hidden_files.append(full_path)

    # Calculate the maximum length of the file paths
    max_length = max(len(os.path.basename(file_path)) for file_path in hidden_files)

    # Print the numbered bullet list with aligned file paths
    for i, file_path in enumerate(hidden_files, start=1):
        file_name = os.path.basename(file_path)
        print(f"{i}) {file_name.ljust(max_length)} \t{file_path}")

    if len(hidden_files) == 0:
        print("Directory Clear")

def is_hidden(filepath):
    if platform.system() == "Windows":
        if os.path.basename(filepath).startswith("."): # Wrote this one because Windows still hides from searches when they have a '.' as a filename prefix
            return True
        try:
            attrs = os.stat(filepath).st_file_attributes
            return bool(attrs & 2)  # Check if hidden attribute is set
        except AttributeError:
            return False
    # Hidden file checker if run on non Unix based OS
    else:
        return os.path.basename(filepath).startswith(".")

directory_to_search = r"C:\Users\txvpa\OneDrive\Desktop"
list_hidden_files(directory_to_search)