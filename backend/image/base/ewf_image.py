import pytsk3

# Same as DD, added partion logic to abstract away from parent

class EWFImgInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(EWFImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def _parse_partitions(self):
        """Detect and return a list of partitions for the EWF image."""
        partition_table = pytsk3.Volume_Info(self)
        partitions = []
        for partition in partition_table:
            if partition.len > 0:
                partitions.append({
                    "index": partition.addr,
                    "start": partition.start,
                    "length": partition.len,
                    "description": partition.desc.decode('utf-8'),
                })
        return partitions

    def get_partitions(self):
        return self.partitions

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)
    
    def get_size(self):
        return self._ewf_handle.get_media_size()
