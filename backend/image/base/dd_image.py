import pytsk3
import os

class DDImgInfo(pytsk3.Img_Info):
    def __init__(self, dd_handle):
        self._dd_handle = dd_handle
        super(DDImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._dd_file.close()

    def read(self, offset, size):
        self._dd_file.seek(offset)
        return self._dd_file.read(size)
    
    def get_size(self):
        return self._dd_file.get_media_size() 