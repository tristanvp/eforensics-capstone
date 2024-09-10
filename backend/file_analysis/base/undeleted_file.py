## Not sure who was assigned this so ill just have a crack
## Searches for files that have been marked as deleted, but still present on disk

import pytsk3

class UndeletedFiles:
    def __init__(self, image):
        # Initializes with an image object that contains the filesystem data. Image will be passed from 'image.py'
        self.image = image

    def find_undeleted_files(self):
        # List to store undeleted files
        undeleted_files = []

        # Access the filesystem
        fs_info = self.image.mount.handle.fs_info

        # Traverse directories to find undeleted files
        for directory in fs_info.open_dir(path='/'):
            for entry in directory:
                # Check if the entry is a file and not marked as deleted
                if entry.info.name.name and not entry.info.meta.deleted:
                    file_info = {
                        'name': entry.info.name.name.decode('utf-8'),
                        'inode': entry.info.meta.addr,
                        'size': entry.info.meta.size
                    }
                    undeleted_files.append(file_info)

        return undeleted_files

    def print_undeleted_files(self):
        # Prints the list of undeleted files.
        undeleted_files = self.find_undeleted_files()
        print("Undeleted Files:")
        for file in undeleted_files:
            print(f"Name: {file['name']}, Inode: {file['inode']}, Size: {file['size']} bytes")

