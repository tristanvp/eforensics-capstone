import os
import sys
from docxtpl import DocxTemplate

class ReportGenerator:
    def __init__(self, template_path, output_path):
        # Initialise ReportGenerator class with template and output path
        self.template_path = template_path
        self.output_path = output_path

    def generate_report(self, context):
        # Generates report using given context dictionary in main
        try:
            document = DocxTemplate(self.template_path)
            document.render(context)
            document.save(self.output_path)
            print(f"Document saved successfully: {self.output_path}")
        except Exception as e:
            print(f"Error while rendering or saving the document: {e}")
