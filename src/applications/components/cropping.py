import cv2

from src.core.components.base import BaseComponent
from src.core.iospec import ComponentIOSpec
from src.applications.visualizer.image import (
    CVImageVisualizer as ImageVisualizer
)
from src.applications.types.image import (
    OpenCVImageType as ImageType,
)
from src.utils.component import \
    run_component_with_singular_input_of_ImageType

class CroppingComponent(BaseComponent):
    """Crops the upper side (from 0 to y) of an image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=ImageType(),
            allow_copy=False,
            allow_change=False,
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='image',
            data_container=ImageType(),
            allow_copy=True,
            allow_change=False,
        )
    ]
    visualizer = ImageVisualizer(
        name='CroppingComponent'
    )

    def __init__(
        self,
        y: int = None
    ):
        super().__init__()
        self.y = y

    def run(
        self,
        image
    ) -> dict:
        height = image.shape[0]
        if self.y is None:
            self.y = int(height / 2)
        cropped_image = image[self.y:, :]
        self.visualize(cropped_image)
        self.log('completed cropping operation.', level='debug')
        return {'image': cropped_image}


if __name__ == '__main__':
    component = CroppingComponent()
    import os
    video_path = os.path.join('data', 'project.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path
    )
