import pytsk3
import os

# DDImage base class
# Added partion logic to abstract away from parent, 

class DDImgInfo(pytsk3.Img_Info):
    def __init__(self, dd_handle):
        self._dd_handle = dd_handle
        super(DDImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def _parse_partitions(self):
        #Detect and return a list of partitions for the raw DD image.
        partition_table = pytsk3.Volume_Info(self)
        partitions = []
        for partition in partition_table:
            if partition.len > 0:  # Valid partition
                partitions.append({
                    "index": partition.addr,
                    "start": partition.start,
                    "length": partition.len,
                    "description": partition.desc.decode('utf-8'),
                })

        return partitions
    
    def get_partitions(self):
        # Return partition data 
        return self.partitions
    
    def close(self):
        self._dd_file.close()

    def read(self, offset, size):
        self._dd_file.seek(offset)
        return self._dd_file.read(size)
    
    def get_size(self):
        return os.path.getsize(self._dd_handle.name) 
