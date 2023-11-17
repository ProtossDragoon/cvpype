import cv2

from src.core.components.base import BaseComponent
from src.core.iospec import ComponentIOSpec
from src.applications.visualizer.image import (
    CVImageVisualizer as ImageVisualizer
)
from src.applications.types.image import (
    OpenCVGrayscaledImageType as GrayscaledImageType,
    OpenCVEdgeImageType as EdgeImageType
)
from src.utils.component import \
    run_component_with_singular_input_of_ImageType


class BlurringComponent(BaseComponent):
    """Applies bilateral Gaussian blurring to a grayscaled image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_type=GrayscaledImageType(),
            allow_copy=True,
            allow_change=False,
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='image',
            data_type=EdgeImageType(),
            allow_copy=True,
            allow_change=False,
        )
    ]
    visualizer = ImageVisualizer(
        name='BlurringComponent'
    )

    def __init__(
        self,
        do_logging: bool = True
    ):
        super().__init__(do_logging)

    def run(
        self,
        image,
        sigma_color: int = 10,
        sigma_space: int = 10
    ) -> list:
        blurred_image = cv2.bilateralFilter(
            image, -1,
            sigma_color,
            sigma_space
        )
        self.visualize(blurred_image)
        self.log('completed bilateral Gaussian blurring operation.', level='debug')
        return [blurred_image]


if __name__ == '__main__':
    component = BlurringComponent()
    import os
    video_path = os.path.join('data', 'project_grayscale.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path,
        output_path=os.path.join('data', 'project_blurred.avi')
    )
