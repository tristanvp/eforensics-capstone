from docxtpl import DocxTemplate
from Test_FindHiddenFiles import hidden_files_and_properties

# Load the template
template_path = 'Template_eForensicsAnalysisReport.docx'
document = DocxTemplate(template_path)

# Define data to export using a dictionary
context = {
    'investigated_device': "Jim's 256 terabyte hard drive", # Investigated device name can be replaced by a dynamic variable assuming Foren6 will employ custom user input

    'rows_hidden': hidden_files_and_properties # Rows for each table to be generated through a list of dictionaries 
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