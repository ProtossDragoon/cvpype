import cv2

from src.core.components.base import BaseComponent
from src.core.iospec import ComponentIOSpec
from src.applications.visualizer.image import (
    CVImageVisualizer as ImageVisualizer
)
from src.applications.types.image import (
    OpenCVGrayscaledImageType as GrayscaledImageType,
)
from src.utils.component import \
    run_component_with_singular_input_of_ImageType

class CroppingComponent(BaseComponent):
    """Crops the lower half of a grayscaled image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_type=GrayscaledImageType(),
            allow_copy=False,
            allow_change=False,
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='image',
            data_type=GrayscaledImageType(),
            allow_copy=True,
            allow_change=False,
        )
    ]
    visualizer = ImageVisualizer(
        name='CroppingComponent'
    )

    def __init__(
        self,
        do_logging: bool = True
    ):
        super().__init__(do_logging)

    def run(self, image, **kwargs) -> list:
        height = image.shape[0]
        cropped_image = image[int(height / 2):, :]
        self.visualize(cropped_image)
        self.log('completed cropping operation.', level='debug')
        return [cropped_image]


if __name__ == '__main__':
    component = CroppingComponent()
    import os
    video_path = os.path.join('data', 'project.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path
    )
