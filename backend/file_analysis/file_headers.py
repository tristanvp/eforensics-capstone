import pytsk3

class FileHeaderDetector:
    def __init__(self, fs_obj_list: list[pytsk3.File], filepaths: list[str]):
        self.fs_obj_list = fs_obj_list
        self.filepaths = filepaths
        self.file_info_list = []  # List to store file info dictionaries

    def detect_header(self, data):
        """
        Detects the file header by checking common file signatures.
        Returns the file type if matched, otherwise returns 'Unknown'.
        """
        file_signatures = [
            (b'\xFF\xD8\xFF\xE0', 'JPEG'),       # JPEG Header
            (b'%PDF', 'PDF'),                    # PDF Header
            (b'\x50\x4B\x03\x04', 'ZIP'),        # ZIP Header
            (b'\x7B\x5C\x72\x74\x66\x31', 'RTF'),  # RTF Header
            (b'\x72\x65\x67\x66', 'DAT'),        # DAT Header
            (b'\x4D\x5A', 'DLL'),                # DLL Header
            (b'\xFF\xD8\xFF\xDB', 'JPEG'),       # JPEG File Interchange Format
            (b'\x42\x4D', 'BMP'),                # BMP Image
            (b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', 'PNG'),  # PNG Image
            (b'\x47\x49\x46\x38\x39\x61', 'GIF89a'),        # GIF Image 89a
            (b'\x47\x49\x46\x38\x37\x61', 'GIF87a'),        # GIF Image 87a
            (b'\x25\x21\x50\x53', 'PostScript'), # PostScript File
            (b'\x50\x4B\x03\x04', 'JAR'),        # JAR File (Java Archive)
            (b'\x25\x50\x44\x46', 'PDF'),        # PDF Document
            (b'\x37\x7A\xBC\xAF\x27\x1C', '7-Zip'),  # 7-Zip Compressed File
            (b'\x1F\x8B', 'GZIP'),               # GZIP Compressed File
            (b'\x4D\x54\x68\x64', 'MIDI'),       # MIDI Sound File
            (b'\x00\x01\x42\x44', 'PalmDB'),     # Palm Desktop To Do Archive
            (b'\x0D\x0A', 'PalmDB'),             # Palm Desktop Calendar Archive
            (b'\x42\x41\x43\x4B\x4D\x49\x4B\x45', 'Amiga Backup Disk'),  # AmiBack Backup
            (b'\x49\x49\x2A\x00', 'TIFF (little endian)'),  # TIFF Image (little endian)
            (b'\x4D\x4D\x00\x2A', 'TIFF (big endian)'),     # TIFF Image (big endian)
            (b'\xFF\xFB', 'MP3 (MPEG Audio)'),   # MP3 File
            (b'\x52\x49\x46\x46', 'AVI/WAV'),    # RIFF Container (AVI or WAV)
            (b'\x49\x44\x33', 'MP3 with ID3v2'), # MP3 with ID3v2 Tag
            (b'\x42\x5A\x68', 'BZ2'),            # BZip2 Compressed File
            (b'\x7F\x45\x4C\x46', 'ELF'),        # ELF Executable (Unix-based systems)
            (b'\x1A\x45\xDF\xA3', 'Matroska'),   # Matroska Video File
            (b'\x50\x4B\x05\x06', 'ZIP (spanned)'), # ZIP Spanned Archive
            (b'\x50\x4B\x07\x08', 'ZIP (spanned)'), # ZIP Spanned Archive (alt)
            (b'\x1F\xA0', 'TAR.Z'),              # TAR with LZH Compression
            (b'\x31\xBE\x00\x00', 'IMAP Email'), # IMAP Email File
            (b'\xFF\xD9', 'JPEG Trailer'),       # JPEG Trailer
            (b'\x4F\x67\x67\x53', 'OGG'),        # OGG Multimedia File
            (b'\x52\x41\x52\x21\x1A\x07', 'RAR'),  # RAR Archive
            (b'\x41\x43\x01\x00', 'DWG'),        # AutoCAD Drawing File
            (b'\x00\x01\x00\x00', 'ICO'),        # ICO (Windows Icon)
            (b'\x46\x4F\x52\x4D', 'AIFF/IFF'),   # AIFF or IFF Format
            (b'\x4D\x5A\x90\x00', 'EXE'),        # DOS EXE File
        ]

        for signature, file_type in file_signatures:
            if data.startswith(signature):
                return file_type

        return 'Unknown'

    def scan_files_for_headers(self):
        """
        Scans through the list of fs_objects (pytsk3.File),
        reads the file content, checks the file header, and stores the result
        as a list of dictionaries with id (counter), name, and header.
        """
        fs_object_filepath_list = list(zip(self.fs_obj_list, self.filepaths))
        counter = 0  # Initialize the counter
        for fs_object_filepath in fs_object_filepath_list:
            fs_object = fs_object_filepath[0]
            filepath = fs_object_filepath[1]
            if fs_object.info.meta and fs_object.info.meta.size > 0:
                try:
                    # Read the file content
                    data = fs_object.read_random(0, min(fs_object.info.meta.size, 512))  # Read the first 512 bytes
                    print(f"Data of {filepath}: ", data, "\n")
                    # Detect the file header
                    file_header = self.detect_header(data)

                    # Append the file info as a dictionary
                    self.file_info_list.append({
                        'no': counter,
                        'name': filepath,
                        'header': file_header
                    })
                    
                    # Increment the counter
                    counter += 1

                except IOError:
                    print(f"Could not read file: {fs_object.info.name.name}")
                except Exception as e:
                    print(f"Error processing file {fs_object.info.name.name}: {str(e)}")

        return self.file_info_list  # Return the list of dictionaries with file info
