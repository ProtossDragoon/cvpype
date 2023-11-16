import cv2

from src.core.components.base import BaseComponent
from src.core.iospec import ComponentIOSpec
from src.applications.visualizer.image import (
    CVImageVisualizer as ImageVisualizer
)
from src.applications.types.image import (
    OpenCVRGBImageType as RGBImageType,
    OpenCVGrayscaledImageType as GrayscaledImageType,
)
from src.utils.component import \
    run_component_with_singular_input_of_ImageType


class GrayscailingComponent(BaseComponent):
    """Converts an RGB image to a grayscaled image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_type=RGBImageType,
            allow_copy=False,
            allow_change=False,
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='image',
            data_type=GrayscaledImageType,
            allow_copy=True,
            allow_change=False,
        )
    ]
    visualizer = ImageVisualizer(
        name='GrayscailingComponent'
    )

    def __init__(
        self,
        do_logging: bool = False
    ):
        super().__init__(do_logging)

    def run(self, image) -> list:
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.visualize(grayscale_image)
        self.log('completed grayscale transformation.', level='debug')
        return [grayscale_image]


if __name__ == '__main__':
    component = GrayscailingComponent()
    import os
    video_path = os.path.join('data', 'project.avi')
    output_path = os.path.join('data', 'project_grayscale.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path, output_path=output_path
    )
