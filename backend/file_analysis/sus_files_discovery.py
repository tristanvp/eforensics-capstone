from backend.utility.filesystem import FileSystem
import os, struct, datetime

class SusFilesDiscovery:
    def __init__(self, fs: FileSystem):
        self.fs = fs
    
    def run(self):
        self.recurse_dollar_i_files()
        self.recurse_interesting_extension_files()

    def recurse_interesting_extension_files(self):
        interesting_file_extensions = ['.config', '.exe', '.db', '.sqlite', '.sqlite3', '.log', '.xml', '.tmp', '.dmp', '.txt', '.sh']
        interesting_extension_files = []
        for ext in interesting_file_extensions:
            interesting_files = self.fs.recurse_files(ext, logic="endswith")
            if (interesting_files):
                interesting_extension_files.append(interesting_files)
        print(interesting_extension_files) 
        return interesting_extension_files
        
    def recurse_dollar_i_files(self):
        dollar_i_files = self.fs.recurse_files("$I", path='/$Recycle.bin', logic="startswith")
        if dollar_i_files is not None:
            return self.process_dollar_i(self.fs, dollar_i_files)
        else:
            print("No $I files found")
            
    def process_dollar_i(self, dollar_i_files: list):
        processed_files = []
        for dollar_i in dollar_i_files:
            # Interpret file metadata
            file_attribs = self.validate_dollar_i(dollar_i[3])
            if file_attribs is None:
                continue # Invalid $I file
            file_attribs['dollar_i_file'] = os.path.join(
                '/$Recycle.bin', dollar_i[2][1:])
            # Get the $R file
            recycle_file_path = os.path.join(
                '/$Recycle.bin',
                dollar_i[1].rsplit("/", 1)[0][1:]
            )
            dollar_r_files = self.fs.recurse_files(
                "$R" + dollar_i[0][2:],
                path=recycle_file_path, logic="startswith"
            )
            if dollar_r_files is None:
                dollar_r_dir = os.path.join(recycle_file_path,
                                            "$R" + dollar_i[1][2:])
                dollar_r_dirs = self.fs.query_directory(dollar_r_dir)
                if dollar_r_dirs is None:
                    file_attribs['dollar_r_file'] = "Not Found"
                    file_attribs['is_directory'] = 'Unknown'
                else:
                    file_attribs['dollar_r_file'] = dollar_r_dir
                    file_attribs['is_directory'] = True
            else:
                dollar_r = [os.path.join(recycle_file_path, r[1][1:])
                            for r in dollar_r_files]
                file_attribs['dollar_r_file'] = ";".join(dollar_r)
                file_attribs['is_directory'] = False
            processed_files.append(file_attribs)
        return processed_files

    def sizeof_fmt(self, num, suffix='B'):
        # From https://stackoverflow.com/a/1094933/3194812
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def parse_windows_filetime(self, date_value):
        microseconds = float(date_value) / 10
        ts = datetime.datetime(1601, 1, 1) + datetime.timedelta(
            microseconds=microseconds)
        return ts.strftime('%Y-%m-%d %H:%M:%S.%f')

    def validate_dollar_i(self, file_obj):
        if file_obj.read_random(0, 8) != '\x01\x00\x00\x00\x00\x00\x00\x00':
            return None # Invalid file
        raw_file_size = struct.unpack('<q', file_obj.read_random(8, 8))
        raw_deleted_time = struct.unpack('<q', file_obj.read_random(16, 8))
        raw_file_path = file_obj.read_random(24, 520) # assumes this disk is prior to Windows 10: https://medium.com/@thismanera/windows-recycle-bin-forensics-a2998c9a4d3e
        file_size = self.sizeof_fmt(raw_file_size[0])
        deleted_time = self.parse_windows_filetime(raw_deleted_time[0])
        file_path = raw_file_path.decode("utf16").strip("\x00")
        return {'file_size': file_size, 'file_path': file_path,
                'deleted_time': deleted_time}
