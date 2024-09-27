import os

class SimpleFileSearcher:
    def __init__(self, mount_point):
        self.mount_point = mount_point

    def search_keyword(self, root_dir, keyword):
        matches = []
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        if keyword in file.read():
                            matches.append(file_path)
                except (UnicodeDecodeError, ValueError):
                    try:
                        with open(file_path, 'rb') as file:
                            if keyword.encode('utf-8') in file.read():
                                matches.append(file_path)
                    except Exception as e:
                        print(f"[-] Could not read file {file_path}: {e}")
        return matches
