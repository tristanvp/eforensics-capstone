import os
import io
import pytsk3
import filetype
from .metadata_extractor import MetadataExtractor
from backend.utility.filesystem import FileSystem

class RenamedFileFinder:
    def __init__(self, fs: FileSystem):
        self.fs = fs
        self.file_counter = 1  # Global file counter for table formatting

    # Fallback file signature guessing for specific file types
    def fallback_filetype(self, file_data, file_name):
        ext = os.path.splitext(file_name)[1].lower()
        # Return the appropriate MIME type for the known extensions
        fallback_mime_types = {
            ".jpg": "image/jpeg",
            ".log": "text/plain",
            ".ini": "text/plain",
            ".rtf": "application/rtf",
            ".dat": "application/octet-stream",
            ".dll": "application/x-msdownload"
        }
        return fallback_mime_types.get(ext, None)

    # Check file signature and compare it to the file extension
    def check_file_signature(self, entry, file_name):
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

            # Return true extension if there is a mismatch
            if not file_ext.endswith(true_ext):
                return true_ext

        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
            return None

    # Traverse directory and collect metadata for mismatched files
    def traverse_directory(self, fs, directory, current_path="", visited_inodes=set(), renamed_files=[]):
        for entry in directory:
            if not hasattr(entry, "info") or not hasattr(entry.info, "name") or not entry.info.name.name:
                continue

            file_name = entry.info.name.name.decode("utf-8")

            # Skip special files (like $MFT, $Bitmap, etc.)
            if file_name.startswith("$") or entry.info.meta is None:
                continue

            inode = entry.info.meta.addr
            if inode in visited_inodes:
                continue
            visited_inodes.add(inode)

            file_path = os.path.join(current_path, file_name)

            # If its a regular file, check the signature
            if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG:
                true_extension = self.check_file_signature(entry, file_name)
                if true_extension:
                    # Extract metadata for report prep 
                    file_metadata = MetadataExtractor(entry, file_path, self.file_counter).extract_metadata(true_extension=true_extension)
                    if file_metadata:
                        renamed_files.append(file_metadata)
                    self.file_counter += 1

            # If its a directory, recurse into it
            elif entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                try:
                    sub_directory = entry.as_directory()
                    self.traverse_directory(fs, sub_directory, file_path, visited_inodes, renamed_files)
                except IOError as e:
                    print(f"Cannot open directory {file_name}: {e}")

        return renamed_files

    # Run function to start the process
    def run(self):
        fs, root_directory = self.open_image()
        renamed_files = self.traverse_directory(fs, root_directory)
        return renamed_files
