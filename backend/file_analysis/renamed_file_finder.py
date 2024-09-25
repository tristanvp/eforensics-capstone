import os
import io
import pytsk3
import filetype
from .metadata_extractor import MetadataExtractor

class RenamedFileFinder:
    def __init__(self, image_file):
        self.image_file = image_file
        self.file_counter = 1  # Global file counter for numbering

    # Function to open the disk image and go through its file system
    def open_image(self):
        img = pytsk3.Img_Info(self.image_file)
        fs = pytsk3.FS_Info(img)
        root_dir = fs.open_dir(path="/")
        return fs, root_dir

    # Fallback file signature guessing for specific file types
    def fallback_filetype(self, file_data, file_name):
        ext = os.path.splitext(file_name)[1].lower()
        if ext == ".jpg":
            return "image/jpeg"
        elif ext == ".rtf":
            return "application/rtf"
        elif ext == ".log":
            return "text/plain"
        elif ext == ".ini":
            return "text/plain"
        elif ext == ".dat":
            return "application/octet-stream"
        elif ext == ".dll":
            return "application/x-msdownload"
        return None

    # Function to check the file signature vs file extension
    def check_file_signature(self, entry, file_name, file_path):
        try:
            file_data = entry.read_random(0, entry.info.meta.size)

            kind = filetype.guess(io.BytesIO(file_data))
            if kind is None:
                kind = self.fallback_filetype(file_data, file_name)
                if kind is None:
                    return None  # Skip if unable to guess
                mime = kind
            else:
                mime = kind.mime

            file_ext = os.path.splitext(file_name)[1].lower()
            true_ext = mime.split('/')[-1]

            # Return mismatched file details if extension doesn't match
            if not file_ext.endswith(true_ext):
                return {
                    'file_name': file_name,
                    'file_path': file_path,
                    'file_ext': file_ext,
                    'true_ext': true_ext
                }

        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
            return None

    # Function to traverse the directory and process each file
    def traverse_directory(self, fs, directory, current_path="", visited_inodes=set(), renamed_files=[]):
        for entry in directory:
            if not hasattr(entry, "info") or not hasattr(entry.info, "name") or not entry.info.name.name:
                continue

            file_name = entry.info.name.name.decode("utf-8")

            # Skip special files (like $MFT, $Bitmap, etc.)
            if file_name.startswith("$"):
                continue

            if entry.info.meta is None:
                continue

            inode = entry.info.meta.addr
            if inode in visited_inodes:
                continue
            visited_inodes.add(inode)

            file_path = os.path.join(current_path, file_name)

            if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG:
                mismatched_file = self.check_file_signature(entry, file_name, file_path)
                if mismatched_file:
                    # Instantiate the MetadataExtractor class to extract metadata
                    file_obj = MetadataExtractor(entry, file_path, self.file_counter)
                    file_metadata = file_obj.extract_metadata(true_extension=mismatched_file['true_ext'])
                    if file_metadata:
                        renamed_files.append(file_metadata)
                    self.file_counter += 1  # Increment global file number

            elif entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                try:
                    sub_directory = entry.as_directory()
                    self.traverse_directory(fs, sub_directory, file_path, visited_inodes, renamed_files)
                except IOError as e:
                    print(f"Cannot open directory {file_name}: {e}")

        return renamed_files

    # Run function to start the process
    def run(self):
        fs, root_dir = self.open_image()
        renamed_files = self.traverse_directory(fs, root_dir)

        return renamed_files
