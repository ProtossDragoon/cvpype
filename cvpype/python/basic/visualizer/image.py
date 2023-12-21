# Built-in
from typing import Union

# Third Party
import cv2
import numpy as np

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import ImageType

# Project-Visualizers
from cvpype.python.core.visualizer.base import BaseVisualizer

# Project-Outputstream
from cvpype.python.backend.web.streamer.rtimage import RealtimeImageWebStreamer # FIXME


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
        self.web_streaming = False  # FIXME: dirty

    # FIXME: dirty
    def set_web_streamer(
        self,
        streamer: RealtimeImageWebStreamer
    ):
        self.web_streamer = streamer
        self.web_streaming = True
        self.is_threading = True

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
        # FIXME: dirty
        if self.web_streaming:
            self.web_streamer(image)
        else:
            if not self.is_threading:
                # https://github.com/opencv/opencv/issues/22602
                cv2.imshow(self.name, image) # FIXME: imshow == kind of outputstream
                if cv2.waitKey(1) == ord('q'):
                    self.off()

    def off(
        self
    ) -> None:
        cv2.destroyWindow(self.name)
        cv2.waitKey(1)
        super().off()
