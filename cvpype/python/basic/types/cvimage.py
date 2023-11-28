# Third party
import cv2
import numpy as np

# Project-Types
from cvpype.python.core.types.base import BaseType


class ImageType(BaseType):
    data_type = (cv2.Mat, np.ndarray)


class GrayscaledImageType(ImageType):
    pass


class RGBImageType(ImageType):
    pass


class EdgeImageType(GrayscaledImageType):
    pass


class HSVImageType(ImageType):
    pass
