import re
import time

class Keyword:
    def __init__(self, words, files):
        self.words = words
        self.files = files
        self.marked_files = []

    def compile_pattern(self):
        # Compile the words into a single regex pattern without word boundaries
        self.pattern = re.compile('|'.join(map(re.escape, self.words)))

    def search_files(self):
        self.compile_pattern()
        for file in self.files:
            #try:
                with open(file, 'r') as f:
                    content = f.read()
                    # Search for the pattern in the file content
                    if self.pattern.search(content):
                        self.marked_files.append(file)
            #except Exception as e:
                #print(f"Error reading {file}: {e}")

    def get_marked_files(self):
        return self.marked_files

    @staticmethod
    def measure_execution_time(function, *args):
        start_time = time.time()
        function(*args)
        end_time = time.time()
        return end_time - start_time