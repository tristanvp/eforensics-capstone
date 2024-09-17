import jpg_carver, pdf_carver, zip_carver

class FileCarver:
    def __init__(self, filename, output_dir):
        self.filename = filename
        self.output_dir = output_dir

    def carve(self):
        jpg_carver.jpg_carve(self.filename, self.output_dir)
        pdf_carver.pdf_carve(self.filename, self.output_dir)
        zip_carver.zip_carve(self.filename, self.output_dir)
