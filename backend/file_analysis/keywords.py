import pytsk3, time
from backend.utility.drive_hash import DriveHash

class GrepKeyword:
    def __init__(self, fs_obj_list: list[pytsk3.File], filepaths: list[str], keywords: list[str]):
        self.fs_obj_list = fs_obj_list
        self.filepaths = filepaths
        self.keywords = keywords
        self.counter = 0  # Initialize the counter at the class level
    
    # Function to check for ADS in a file entry and return a list of stream attributes
    def check_for_ads(self, fs_object):
        ads_attributes = []  # To store the alternate data stream attributes (ADS)
        for attr in fs_object:
            if attr.info.type == pytsk3.TSK_FS_ATTR_TYPE_NTFS_DATA:
                stream_name = attr.info.name
                # Only collect ADS (skip the main $DATA stream)
                if stream_name and stream_name != "$DATA":
                    ads_attributes.append(attr)
        return ads_attributes

    def search(self):
        print(f"Searching for keywords: {', '.join(self.keywords)}")
        fs_obj_filepath_list = list(zip(self.fs_obj_list, self.filepaths))

        # Accumulating the results in a list
        found_files = []

        for fs_obj_filepath in fs_obj_filepath_list:
            fs_obj = fs_obj_filepath[0]
            filepath = fs_obj_filepath[1]
            # Get the result for each file
            result = self.search_in_file(file_entry=fs_obj, file_path=filepath)
            if result:
                found_files.extend(result)

        # Return the accumulated results
        return found_files

    def search_in_file(self, file_entry: pytsk3.File, file_path: str):
        keys_included_files = []
        try:
            # Search in the main file stream first
            main_stream_results = self.read_stream(file_entry, file_path)
            if main_stream_results:
                keys_included_files.extend(main_stream_results)

            # Check for ADS and search in each of them
            ads_attributes = self.check_for_ads(file_entry)
            for ads_attribute in ads_attributes:
                # Read the ADS data using file_entry.read_random for the ADS
                ads_stream_results = self.read_stream(file_entry, file_path, ads_attribute)
                if ads_stream_results:
                    keys_included_files.extend(ads_stream_results)

        except Exception as e:
            print(f"[-] Error reading file {file_path}: {e}")

        return keys_included_files

    def read_stream(self, file_entry: pytsk3.File, file_path: str, ads_attribute=None):
        keys_included_files = []
        try:
            # Handle the main data stream or ADS stream
            stream_name = file_path
            if ads_attribute:
                stream_name += f":{(ads_attribute.info.name).decode()}"

            # Determine the size of the stream to read
            if ads_attribute:
                file_size = ads_attribute.info.size
            else:
                file_size = file_entry.info.meta.size

            offset = 0
            chunk_size = 1024 * 1024  # 1MB Chunk size, limits memory for every search

            # Loops through each chunk
            while offset < file_size:
                size_to_read = min(chunk_size, file_size - offset)

                # Read from the main stream or the ADS
                if ads_attribute:
                    data = file_entry.read_random(offset, size_to_read, ads_attribute.info.type, ads_attribute.info.id)
                else:
                    data = file_entry.read_random(offset, size_to_read)  # Main stream

                if data:  # If chunk contains data
                    for keyword in self.keywords:
                        if keyword.encode('utf-8') in data:
                            print(f"Keyword '{keyword}' found in stream: {stream_name}")
                            created_time = time.ctime(file_entry.info.meta.crtime)
                            last_accessed_time = time.ctime(file_entry.info.meta.atime)
                            last_modified_time = time.ctime(file_entry.info.meta.mtime)
                            file_size_bytes = file_entry.info.meta.size
                            inode_number = file_entry.info.meta.addr
                            md5 = DriveHash(stream_name, file_entry).md5_hash(file_entry)

                            # Use the class-level counter for sequential numbering
                            keys_included_files.append(
                                {
                                    "no": self.counter,  # Use the global counter
                                    "name": stream_name,
                                    "path": stream_name,
                                    "created": created_time,
                                    "accessed": last_accessed_time,
                                    "modified": last_modified_time,
                                    "bytes": file_size_bytes,
                                    "inode": inode_number,
                                    "md5": md5
                                }
                            )
                            self.counter += 1  # Increment the counter for each match
                offset += size_to_read

            return keys_included_files
        except Exception as e:
            print(f"Error reading stream {stream_name}: {e}")
            return None
