import pytsk3
import threading


class ThreadSafeImgInfo(pytsk3.Img_Info):
    def __init__(self, filename):
        # Initialise the file and lock threads
        self._file = open(filename, "rb")
        self._lock = threading.Lock()
        super(ThreadSafeImgInfo, self).__init__(filename)

    def close(self):
        # Closes file
        with self._lock:
            self._file.close()

class PartitionExplorer:
    def __init__(self, img_info):
        self.img_info = img_info
        self.vol_info = pytsk3.Volume_Info(img_info)

    def list_partitions(self):
        partitions = []
        print("Partitions found:")
        for partition in self.vol_info:
            if partition.len > 2048:  # Skip overly small partitions
                partitions.append({
                    'start': partition.start,
                    'len': partition.len,
                    'desc': partition.desc
                })
                print(f"Description: {partition.desc}, Start: {partition.start}, Length: {partition.len}")
        return partitions

class FileSystemTraversal:
    def __init__(self, img_info, offset):
        self.fs_info = None
        # Attempts to open filesystem at marked offset, otherwise errors out.
        try:
            self.fs_info = pytsk3.FS_Info(img_info, offset=offset)
            print(f"Filesystem opened at offset {offset}")
        except Exception as e:
            print(f"Error: Unable to open the filesystem at offset {offset}: {e}")

    def traverse_files(self, keywords):
        # navigate files, chatgpt wrote
        if not self.fs_info:
            print("No filesystem to traverse.")
            return
        self.keywords = keywords
        print(f"Traversing files for keywords: {', '.join(self.keywords)}")
        root_dir = self.fs_info.open_dir(path="/")
        self.traverse_directory(root_dir)

    def traverse_directory(self, directory, parent_path="/"):
        # navigate directory, chatgpt wrote
        for entry in directory:
            if entry.info.name.name in [b'.', b'..']:
                continue
            try:
                file_path = f"{parent_path}/{entry.info.name.name.decode('utf-8')}"
                if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                    sub_directory = entry.as_directory()
                    self.traverse_directory(sub_directory, parent_path=file_path)
                else:
                    self.search_in_file(entry, file_path)
            except Exception as e:
                print(f"Error processing {entry.info.name.name}: {e}")

    def search_in_file(self, file_entry, file_path):
        #
        #
        #
        try:
            file_size = file_entry.info.meta.size
            offset = 0
            chunk_size = 1024 * 1024  # 1MB Chunk size, limits memory for every search
            found = False

            # Loops through each chunk, and breaks once found is true
            while offset < file_size and not found:
                size_to_read = min(chunk_size, file_size - offset)
                data = file_entry.read_random(offset, size_to_read) # Reads chunk

                if data: # If chunk contains data
                    for keyword in self.keywords:
                        if keyword.encode('utf-8') in data:
                            print(f"Keyword '{keyword}' found in file: {file_path}") #Logs keyword and location in cli, to move to array.
                            found = True
                            break

                offset += size_to_read

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

class GrepKeyword:
    def __init__(self, img_info, partition_offset, keywords):
        # Initialises the filesystem at marked partition offset
        self.fs_traversal = FileSystemTraversal(img_info, partition_offset)
        self.keywords = keywords

    def search(self):
        # Logs keywords in the cli
        self.fs_traversal.traverse_files(self.keywords)
        print(f"Searching for keywords: {', '.join(self.keywords)}")

def search_keywords(image_path, keywords):
    # Creates the required objects
    img_info = ThreadSafeImgInfo(image_path)
    partition_explorer = PartitionExplorer(img_info)
    # Lists image partitions
    partitions = partition_explorer.list_partitions()

    for partition in partitions:
        partition_desc = partition['desc'].decode('utf-8').lower() # Read to mitigate error with Microsoft partition
        partition_start = partition['start']
        partition_offset = partition_start * 512  # Converts start sector to byte offset
        print(f"Partition offset: {partition_offset}") # Logs basic partition offset for the the iteration

        # Skips Microsoft partition for error mitigation and logs which partition to the cli
        if 'microsoft reserved partition' in partition_desc:
            print(f"Skipping Microsoft reserved partition at offset {partition_offset}.")
            continue

        # Creates the GrepKeyword object
        grep = GrepKeyword(img_info, partition_offset, keywords)
        
        # For every partition in image, initiates the search function.
        grep.search()

    img_info.close()
