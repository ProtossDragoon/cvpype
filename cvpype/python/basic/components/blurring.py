# Third party
import cv2

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import GrayscaledImageType, EdgeImageType

# Project-Visualizers
from cvpype.python.basic.visualizer.image import ImageVisualizer

# Project-Components
from cvpype.python.core.components.base import BaseComponent

# Project-Utils
from cvpype.python.utils.component import \
    run_component_with_singular_input_of_ImageType


class BilateralBlurringComponent(BaseComponent):
    """Applies bilateral Gaussian blurring to a grayscaled image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=GrayscaledImageType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='image',
            data_container=EdgeImageType(),
        )
    ]
    visualizer = ImageVisualizer(
        name='BilateralBlurringComponent'
    )

    def run(
        self,
        image,
        sigma_color: int = 10,
        sigma_space: int = 10
    ) -> dict:
        blurred_image = cv2.bilateralFilter(
            image, -1,
            sigma_color,
            sigma_space
        )
        self.visualize(blurred_image)
        self.log('completed bilateral Gaussian blurring operation.', level='debug')
        return {'image': blurred_image}


if __name__ == '__main__':
    component = BilateralBlurringComponent()
    import os
    video_path = os.path.join('data', 'sample_grayscale.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path,
        output_path=os.path.join('data', 'sample_blur.avi')
    )
