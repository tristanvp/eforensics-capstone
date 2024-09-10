import pytsk3
import os

class DMGImgInfo(pytsk3.Img_Info):
    def __init__(self, dmg_handle):
        self._dmg_handle = dmg_handle
        super(DMGImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._dmg_handle.close()

    def read(self, offset, size):
        self._dmg_handle.seek(offset)
        return self._dmg_handle.read(size)

    def get_size(self):
        return os.path.getsize(self._dmg_handle)
