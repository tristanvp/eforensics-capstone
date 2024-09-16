import pytsk3

class L01ImgInfo(pytsk3.Img_Info):
    def __init__(self, l01_handle):
        self._l01_handle = l01_handle
        super(L01ImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

        # try to initialize volume info (partitions)
        try:
            self._volume_info = pytsk3.Volume_Info(self)
        except Exception as e:
            self._volume_info = None
            print(f"Error accessing volume info for L01 image: {e}")

    def _has_partitions(self):
        # check if volume info exists
        return self._volume_info is not None

    def get_volume_size(self):
        # return the size of the volume
        return self._l01_handle.get_media_size()

    def get_partition_count(self):
        # check if volume info exists and count partitions
        if self._has_partitions():
            try:
                return sum(1 for _ in self._volume_info)
            except Exception as e:
                raise RuntimeError(f"Failed to get partition count for L01 image: {e}")
        return 0
