import os
import sys
from docxtpl import DocxTemplate

class ReportGenerator:
    def __init__(self, template_path, output_path):
        # Initialize the ReportGenerator with the template path and output path.
        self.template_path = template_path
        self.output_path = output_path

    def generate_report(self, context):
        # General method to generate a report using a given context (hidden files, renamed files, etc.).
        try:
            # Load the template
            document = DocxTemplate(self.template_path)

            # Render the document using the provided context
            document.render(context)

            # Save the new document
            document.save(self.output_path)
            print(f"Document saved successfully: {self.output_path}")
        except Exception as e:
            print(f"Error while rendering or saving the document: {e}")
