import os

class FileSearcher:
    def __init__(self, mount_point):
        # Initialises the FileSearcher with the mount point
        self.mount_point = mount_point

    def search_keyword(self, root_dir, keyword):
        # Searches for a given keyword in all files, later to implement dictionary once cuncurrent works
        matches = []  # List that stores the file paths that contain the keyword

        # Iterates through the directories
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    # Attempts to open and read each file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        if keyword in file.read():  # Checks if the keyword is present
                            matches.append(file_path)  # Adds the file path to matches if keyword is found
                except (UnicodeDecodeError, ValueError):
                    # If UTF-8 reading fails, attempt to read the file as a binary
                    try:
                        with open(file_path, 'rb') as file:
                            if keyword.encode('utf-8') in file.read():  # Check if keyword is present
                                matches.append(file_path)  # Adds the file path to matches if keyword is found
                    except Exception as e:
                        print(f"[-] Could not read file {file_path}: {e}")

        return matches
