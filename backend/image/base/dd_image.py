import pytsk3

class DDImgInfo:
    def __init__(self, file_path):
        try:
            # initialize the image file
            self._image = pytsk3.Img_Info(file_path)
            print("successfully initialized dd image.")
            
            # check for partitions
            self._volume_info = None  # default to None in case no partitions are found
            if self._has_partitions():
                # try to access volume_info if partitions exist
                try:
                    self._volume_info = pytsk3.Volume_Info(self._image)
                    print("successfully accessed volume information.")
                except Exception as e:
                    print(f"error accessing volume info: {e}")
            else:
                print("no partitions found in the image file.")
                
        except Exception as e:
            raise RuntimeError(f"failed to initialize image: {e}")
    
    def _has_partitions(self):
        # check if the image contains partitions by attempting to read partition data
        try:
            partitions = pytsk3.Volume_Info(self._image)
            for _ in partitions:  # try to iterate over partitions
                return True  # if any partition is found, return true
        except Exception as e:
            print(f"error while checking for partitions: {e}")
        return False  # no partitions found
    
    def get_volume_info(self):
        # return the volume_info object if partitions exist and volume info is accessible
        return self._volume_info
    
    def get_partition_count(self):
        # count the number of partitions in the image file if volume_info is available
        if self._volume_info:
            try:
                partitions = self._volume_info
                partition_count = sum(1 for _ in partitions)
                return partition_count
            except Exception as e:
                raise RuntimeError(f"failed to get partition count: {e}")
        return 0
