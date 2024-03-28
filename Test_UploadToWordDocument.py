from docxtpl import DocxTemplate
from Test_FindHiddenFiles import hidden_files_and_properties

# Load the template
template_path = 'Template_eForensicsAnalysisReport.docx'
document = DocxTemplate(template_path)

# Verify the content of hidden_files
# print(hidden_files)  # Check if it contains valid data

# Define data to export using a dictionary
context = {
    'investigated_device': "Jim's 256 terabyte hard drive",
    'rows_hidden': hidden_files_and_properties  # Assuming hidden_files is a list of dictionaries
}

try:
    # Render the document
    document.render(context)

    # Save the new document
    output_path = 'test.docx'
    document.save(output_path)
    print(f"Document saved successfully: {output_path}")
except Exception as e:
    print(f"Error while rendering or saving the document: {e}")
