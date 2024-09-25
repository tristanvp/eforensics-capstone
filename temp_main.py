# to be integrated into main.py

from backend.file_analysis.renamed_file_finder import RenamedFileFinder
from backend.utility.report_generator import ReportGenerator

if __name__ == "__main__":
    # v Test image file for renamed files, to be replaced by filesystem.py's given image file 
    image_file = r'C:\Users\txvpa\OneDrive - Swinburne University\University\2024_Semester2\Swinburne\COS40006_ComputingTechnologyProjectB\forensics_testfiles\8-jpeg-search\8-jpeg-search.dd'
    template_path = r'backend\\utility\\template_eforensics_analysis_report.docx' # Report template document
    output_path = r'backend\\utility\\test.docx' # Report output path

    # Run RenamedFileFinder to find files with mismatched extensions
    renamed_file_finder = RenamedFileFinder(image_file)
    renamed_files = renamed_file_finder.run()

    # Prepare docxtpl context for the report generator
    context = {
        'investigated_device': "Gilbert's 256 terabyte hard drive",  # Temporary static title
        'renamed_files': renamed_files  # Renamed files
    }

    # Generate report
    report_generator = ReportGenerator(template_path, output_path)
    report_generator.generate_report(context)

    # Output success message (yippee)
    print("Report generation complete.")
