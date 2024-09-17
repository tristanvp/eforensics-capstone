# file_analysis.py

from base.keyword import Keyword
# from modules.ile_analysis.carved_file import CarvedFileAnalysis
# from modules.file_analysis.file_headers import FileHeadersAnalysis
# from modules.file_analysis.deleted_file import DeletedFileAnalysis
# from modules.file_analysis.renamed_file import RenamedFileAnalysis
# from modules.file_analysis.eventTimeline.eventTimeline import TimelineAnalysis

class FileAnalysis:
    def __init__(self, image):
        self.image = image
        self.results = {}

    def perform_analysis(self):
        # Create instances of analysis classes and run them
        analyses = [
            CarvedFileAnalysis(self.image),
            FileHeadersAnalysis(self.image),
            KeywordSearchAnalysis(self.image, "example_keyword"),
            RenamedFileAnalysis(self.image),
            TimelineAnalysis(self.image),
            DeletedFileAnalysis(self.image)
        ]
        
        for analysis in analyses:
            self.results.update(analysis.analyze())

    def get_results(self):
        return self.results
