import pytsk3
import pyewf
import zipfile
import os

from base.dd_image import DDImgInfo
from base.dmg_image import DMGImgInfo
from base.l01_image import L01ImgInfo
from base.zip_image import ZIPImgInfo
from base.ewf_image import EWFImgInfo


# import all supporting classes here.


# Handles mounting specifics through abstracted image classes

class ImageMount:
    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type
        self.handle = self._create_handle(file_path, file_type)

    def _create_handle(self, file_path, file_type):
        # Factory method that instantiates the correct handler based on the file type. Acts as a controller to 'image.py'
        if file_type == 'DD':
            dd_handle = open(file_path, 'rb')
            return DDImgInfo(dd_handle)
        elif file_type == 'E01':
            ewf_handle = pyewf.handle(file_path)
            return EWFImgInfo(ewf_handle)
        elif file_type == 'DMG':
            dmg_handle = open(file_path, 'rb')
            return DMGImgInfo(dmg_handle)
        elif file_type == 'L01':
            l01_handle = pyewf.handle(file_path)
            return L01ImgInfo(l01_handle)
        elif file_type == 'ZIP':
            return ZIPImgInfo(file_path)
        else:
            raise ValueError("Unsupported file type")

    def read(self, offset, size):
        return self.handle.read(offset, size)

    def close(self):
        if self.handle:
            self.handle.close()

    def get_size(self):
        return self.handle.get_size()
