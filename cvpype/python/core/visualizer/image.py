# Built-in
from typing import Union

# Third Party
import cv2
import numpy as np

# Project
from cvpype.python.core.iospec import ComponentIOSpec
from cvpype.python.core.visualizer.base import BaseVisualizer
from cvpype.python.core.types.image import ImageType


class ImageVisualizer(BaseVisualizer):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=ImageType(),
        )
    ]

    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name, is_operating)

    def __call__(self, *args, **kwargs):
        ret = super().__call__(*args, **kwargs)
        if self.is_operating:
            self.show(ret)

    def paint(
        self,
        image: ImageType
    ) -> Union[cv2.Mat, np.array]:
        return image.data

    def show(
        self,
        image
    ) -> None:
        cv2.imshow(self.name, image)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyWindow(self.name)
            cv2.waitKey(1)
            self.is_operating = False
