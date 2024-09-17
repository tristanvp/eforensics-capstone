import pytsk3

class L01ImgInfo(pytsk3.Img_Info):
    def __init__(self, l01_handle):
        self._l01_handle = l01_handle
        super(L01ImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        # Close the L01 handle
        self._l01_handle.close()

    def read(self, offset, size):
        # Seek and read from the L01 handle
        self._l01_handle.seek(offset)
        return self._l01_handle.read(size)

    def get_size(self):
        # Get the media size from the L01 handle
        return self._l01_handle.get_media_size()
