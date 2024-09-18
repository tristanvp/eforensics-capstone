import os
import sys
from docxtpl import DocxTemplate

# Importing the collected files to display in the report 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Allows lateral directory imports
from file_analysis.hidden_files import hidden_files_and_properties

# Load the template
template_path = r'backend\\utility\\template_eforensics_analysis_report.docx'
document = DocxTemplate(template_path)

# Define data to export using a dictionary
context = {
    'investigated_device': "Jim's 256 terabyte hard drive", # Investigated device name can be replaced by a dynamic variable assuming Foren6 will employ custom user input

    'hidden_files': hidden_files_and_properties # Rows for each table to be generated through a list of dictionaries 
    # Insert further evidence to display here
}

try:
    # Render the document
    document.render(context)

    # Save the new document
    output_path = r'backend\\utility\\test.docx'
    document.save(output_path)
    print(f"Document saved successfully: {output_path}")
except Exception as e:
    print(f"Error while rendering or saving the document: {e}")

