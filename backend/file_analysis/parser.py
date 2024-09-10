# parser.py

from docxtpl import DocxTemplate

class Parser:
    def __init__(self, result):
        self.result = result

    def to_pdf(self, output_path):
        # Implement PDF generation logic
        # Placeholder for now
        pass

    def to_word(self, template_path, output_path):
        try:
            # Load the template
            document = DocxTemplate(template_path)

            # Define data to export using a dictionary
            context = {
                'investigated_device': "Jim's 256 terabyte hard drive",  # Replace with actual device name
                'rows_hidden': self.result.get('carved_files', [])  # Example context; adjust based on result structure
            }

            # Render the document
            document.render(context)

            # Save the new document
            document.save(output_path)
            print(f"Document saved successfully: {output_path}")
        except Exception as e:
            print(f"Error while rendering or saving the document: {e}")
