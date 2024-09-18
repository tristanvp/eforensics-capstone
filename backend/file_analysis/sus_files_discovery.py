import os
import hashlib
import time
import struct
import datetime
from backend.utility.filesystem import FileSystem  

class SusFilesDiscovery:
    def __init__(self, fs: FileSystem):
        self.fs = fs
        self.suspicious_types = ['.exe', '.config', '.db', '.log', '.sqlite', '.sh']
        self.suspicious_files = []

    def run(self):
        # Main method to run file discovery methods
        suspicious_files = self.list_suspicious_files()
        recycle_bin_files = self.recurse_dollar_i_files()  # Process $I and $R files in the Recycle Bin
        return suspicious_files + recycle_bin_files

    def list_suspicious_files(self):
        # Search for files with suspicious extensions
        self.recurse_directory()
        return self.suspicious_files

    def recurse_directory(self):
        # Recurse through file system and find files with suspicious extensions
        file_number = 1
        for fs_object in self.fs.recurse_files(path='/'):
            if fs_object.info.name.name.decode('utf-8').lower().endswith(tuple(self.suspicious_types)):
                file_properties = self.get_file_properties(fs_object, file_number)
                if file_properties:
                    self.suspicious_files.append(file_properties)
                    file_number += 1

    def get_file_properties(self, fs_object, file_number):
        # Return file properties including MD5 hash
        try:
            file_properties = {
                "no": file_number,
                "name": fs_object.info.name.name.decode('utf-8'),
                "path": fs_object.info.meta.addr,  # Inode number as a substitute for path in a disk image
                "created": time.ctime(fs_object.info.meta.crtime),
                "accessed": time.ctime(fs_object.info.meta.atime),
                "modified": time.ctime(fs_object.info.meta.mtime),
                "bytes": fs_object.info.meta.size,
                "md5": None
            }

            # MD5 hash calculation
            md5_hash = hashlib.md5()
            file_size = fs_object.info.meta.size

            if file_size > 0:
                file_content = fs_object.read_random(0, file_size)
                md5_hash.update(file_content)
                file_properties["md5"] = md5_hash.hexdigest()

            return file_properties
        except Exception as e:
            print(f"Error retrieving properties for file: {fs_object.info.name.name.decode('utf-8')}, Error: {str(e)}")
            return None

    def recurse_dollar_i_files(self):
        # Search for $I files in the Recycle Bin
        dollar_i_files = self.fs.recurse_files("$I", path='/$Recycle.bin', logic="startswith")
        if dollar_i_files is not None:
            return self.process_dollar_i(dollar_i_files)
        else:
            print("No $I files found")

    def process_dollar_i(self, dollar_i_files: list):
        # Process the found $I files
        processed_files = []
        for dollar_i in dollar_i_files:
            file_attribs = self.validate_dollar_i(dollar_i[3])  # Validate $I file structure
            if file_attribs is None:
                continue  # Invalid $I file, skip to the next one
            file_attribs['dollar_i_file'] = os.path.join('/$Recycle.bin', dollar_i[2][1:])
            
            # Get the $R file path
            recycle_file_path = os.path.join('/$Recycle.bin', dollar_i[1].rsplit("/", 1)[0][1:])
            dollar_r_files = self.fs.recurse_files("$R" + dollar_i[0][2:], path=recycle_file_path, logic="startswith")
            
            if dollar_r_files is None:
                dollar_r_dir = os.path.join(recycle_file_path, "$R" + dollar_i[1][2:])
                dollar_r_dirs = self.fs.query_directory(dollar_r_dir)
                if dollar_r_dirs is None:
                    file_attribs['dollar_r_file'] = "Not Found"
                    file_attribs['is_directory'] = 'Unknown'
                else:
                    file_attribs['dollar_r_file'] = dollar_r_dir
                    file_attribs['is_directory'] = True
            else:
                dollar_r = [os.path.join(recycle_file_path, r[1][1:]) for r in dollar_r_files]
                file_attribs['dollar_r_file'] = ";".join(dollar_r)
                file_attribs['is_directory'] = False
            
            processed_files.append(file_attribs)
        return processed_files

    def sizeof_fmt(self, num, suffix='B'):
        # Format file sizes into human-readable form (e.g., KB, MB)
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def parse_windows_filetime(self, date_value):
        # Convert Windows filetime format into human-readable date
        microseconds = float(date_value) / 10
        ts = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=microseconds)
        return ts.strftime('%Y-%m-%d %H:%M:%S.%f')

    def validate_dollar_i(self, file_obj):
        # Validate and extract attributes from $I file
        if file_obj.read_random(0, 8) != '\x01\x00\x00\x00\x00\x00\x00\x00':
            return None  # Invalid $I file
        raw_file_size = struct.unpack('<q', file_obj.read_random(8, 8))
        raw_deleted_time = struct.unpack('<q', file_obj.read_random(16, 8))
        raw_file_path = file_obj.read_random(24, 520)  # Extract file path (before Windows 10 format)
        file_size = self.sizeof_fmt(raw_file_size[0])
        deleted_time = self.parse_windows_filetime(raw_deleted_time[0])
        file_path = raw_file_path.decode("utf16").strip("\x00")
        return {'file_size': file_size, 'file_path': file_path, 'deleted_time': deleted_time}
