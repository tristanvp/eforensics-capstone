import os
import io
import pytsk3
import filetype
from datetime import datetime
from backend.utility.drive_hash import DriveHash
from backend.utility.filesystem import FileSystem

class RenamedFileFinder:
    def __init__(self, fs_obj_list: list[pytsk3.File], filenames: list[str], filepaths: list[str]):
        self.fs_obj_list = fs_obj_list
        self.filenames = filenames
        self.filepaths = filepaths

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
            if entry.info.meta.size > 0:
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

                if not file_ext.endswith(true_ext):
                    return true_ext
            else:
                print(f"[!] File {file_name} has size 0, skipping.")
                return None

        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
            return None
        
    def find_renamed_files(self):
        renamed_files = []
        renamed_files_counter = 0
        fs_obj_filename_filepath_list = list(zip(self.fs_obj_list, self.filenames, self.filepaths))
        for fs_obj_filename_filepath in fs_obj_filename_filepath_list:
            fs_obj = fs_obj_filename_filepath[0]
            filename = fs_obj_filename_filepath[1]
            filepath = fs_obj_filename_filepath[2]
            true_extension = self.check_file_signature(fs_obj, filename)
            if true_extension:
                created_time = datetime.fromtimestamp(fs_obj.info.meta.crtime).isoformat()
                last_accessed_time = datetime.fromtimestamp(fs_obj.info.meta.atime).isoformat()
                last_modified_time = datetime.fromtimestamp(fs_obj.info.meta.mtime).isoformat()
                file_size_bytes = fs_obj.info.meta.size
                inode_number = fs_obj.info.meta.addr
                md5 = DriveHash(filename, fs_obj).md5_hash(fs_obj)
                file_properties = {
                    "no": renamed_files_counter,  # Added file number for sequential order
                    "name": filename,
                    "path": filepath,
                    "created": created_time,
                    "accessed": last_accessed_time,
                    "modified": last_modified_time,
                    "bytes": file_size_bytes,
                    "inode": inode_number,
                    "md5": md5,
                    "true_extension": true_extension  # Add true extension to metadata
                }
                renamed_files.append(file_properties)
                renamed_files_counter += 1
                
        return renamed_files
    