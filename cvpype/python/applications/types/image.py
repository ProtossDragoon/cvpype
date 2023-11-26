# Third party
import cv2
import numpy as np

# Project
from cvpype.python.core.types.image import ImageType


class OpenCVImageType(ImageType):
    data_type = (cv2.Mat, np.ndarray)


class OpenCVGrayscaledImageType(OpenCVImageType):
    pass


class OpenCVRGBImageType(OpenCVImageType):
    pass


class OpenCVEdgeImageType(OpenCVGrayscaledImageType):
    pass


class OpenCVHSVImageType(OpenCVImageType):
    pass
