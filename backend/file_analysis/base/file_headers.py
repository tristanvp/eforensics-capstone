# OOP Uplift on Ronan's work
# 

class FileHeaders:
    def __init__(self, filepath):
        # Initializes the FileHeaders object with a file path.
        self.filepath = filepath
        self.file_header = ""  # Holds the detected file header type.

    def read_file(self):
        # Reads the content of the file specified by filepath.
        with open(self.filepath, 'rb') as file:
            return file.read()

    def detect_file_header(self):
        # Detects the file header type based on known file signatures.
        # Updates the file_header attribute with the detected file type.
        data = self.read_file()

        if self.is_jpeg(data):
            self.file_header = "JPEG"
        elif self.is_pdf(data):
            self.file_header = "PDF"
        elif self.is_zip(data):
            self.file_header = "ZIP"
        else:
            self.file_header = "Unknown"

        self.print_file_header()

    def is_jpeg(self, data):
        # Checks if the file data matches the JPEG file header signature.
        jpeg_header = b'\xFF\xD8\xFF\xE0'
        return data.startswith(jpeg_header)

    def is_pdf(self, data):
        pdf_header = b'%PDF'
        return data.startswith(pdf_header)

    def is_zip(self, data):
        # Checks if the file data matches the ZIP file header signature.
        zip_header = b'\x50\x4B\x03\x04'
        return data.startswith(zip_header)


        