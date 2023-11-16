from src.core.types.image import ImageType


class CVImageType(ImageType):
    pass


class OpenCVGrayscaledImageType(CVImageType):
    pass


class OpenCVRGBImageType(CVImageType):
    pass


class OpenCVEdgeImageType(OpenCVGrayscaledImageType):
    pass
