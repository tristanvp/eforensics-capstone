import pytsk3
from datetime import datetime
from backend.utility.drive_hash import DriveHash

class UndeletedFileFinder:
    def __init__(self, fs_obj_list: list[pytsk3.File], filenames: list[str], filepaths: list[str]):
        self.fs_obj_list = fs_obj_list
        self.filenames = filenames
        self.filepaths = filepaths

    def find_undeleted_files(self):
        undeleted_files = []
        undeleted_files_counter = 0
        fs_obj_filename_filepath_list = list(zip(self.fs_obj_list, self.filenames, self.filepaths))
        for fs_obj_filename_filepath in fs_obj_filename_filepath_list:
            fs_obj = fs_obj_filename_filepath[0]
            filename = fs_obj_filename_filepath[1]
            filepath = fs_obj_filename_filepath[2]
            # check if the fs object contains the 'unallocated' flag 
            if fs_obj.info.name.flags & pytsk3.TSK_FS_NAME_FLAG_UNALLOC:
                created_time = datetime.fromtimestamp(fs_obj.info.meta.crtime).isoformat()
                last_accessed_time = datetime.fromtimestamp(fs_obj.info.meta.atime).isoformat()
                last_modified_time = datetime.fromtimestamp(fs_obj.info.meta.mtime).isoformat()
                file_size_bytes = fs_obj.info.meta.size
                inode_number = fs_obj.info.meta.addr
                md5 = DriveHash(filename, fs_obj).md5_hash()  
                file_properties = {
                    "no": undeleted_files_counter,
                    "name": fs_obj.info.name.name.decode('utf-8'),
                    "path": filepath,
                    "created": created_time,
                    "accessed": last_accessed_time,
                    "modified": last_modified_time,
                    "bytes": file_size_bytes,
                    "inode": inode_number,
                    "md5": md5,
                }
                undeleted_files.append(file_properties)
                undeleted_files_counter += 1
        return undeleted_files
