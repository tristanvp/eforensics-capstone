import pytsk3
from base.dd_image import DDImgInfo
from base.ewf_image import EWFImgInfo
from base.l01_image import L01ImgInfo
from base.zip_image import ZIPImgInfo

class ImageFactory:
    def __init__(self, file_path, file_type):
        self.file_path = file_path
        # store file type and initialize the image based on type
        self.file_type = file_type
        self.image = self._create_image(file_path, file_type)

    def _create_image(self, file_path, file_type):
        # create the appropriate image type based on the file type
        if file_type == 'DD':
            return DDImgInfo(file_path)
        elif file_type == 'E01':
            return EWFImgInfo(file_path)
        elif file_type == 'L01':
            return L01ImgInfo(file_path)
        elif file_type == 'ZIP':
            return ZIPImgInfo(file_path)
        else:
            raise ValueError("unsupported file type")

    def get_partitions(self):
        # check if the image class has a get_partition_count method
        if hasattr(self.image, 'get_partition_count'):
            # return the partition count using the appropriate method from the image class
            return self.image.get_partition_count()
        else:
            raise NotImplementedError("partition function not implemented for this image type")

class ImageHandler:
    def __init__(self, file_path, file_type):
        # initialize the image factory with the provided file path and type
        self.image_factory = ImageFactory(file_path, file_type)

    def get_partitions(self):
        # return partitions from the image factory
        return self.image_factory.get_partitions()
