import cv2

from cvpype.python.core.components.base import BaseComponent
from cvpype.python.core.iospec import ComponentIOSpec
from cvpype.python.applications.visualizer.image import (
    CVImageVisualizer as ImageVisualizer
) # FIXME: Application layer should not be called by core layer
from cvpype.python.applications.types.image import (
    OpenCVGrayscaledImageType as GrayscaledImageType,
    OpenCVEdgeImageType as EdgeImageType
) # FIXME: Application layer should not be called by core layer
from cvpype.python.utils.component import \
    run_component_with_singular_input_of_ImageType


class BilateralBlurringComponent(BaseComponent):
    """Applies bilateral Gaussian blurring to a grayscaled image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=GrayscaledImageType(),
            allow_copy=True,
            allow_change=False,
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='image',
            data_container=EdgeImageType(),
            allow_copy=True,
            allow_change=False,
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
    video_path = os.path.join('data', 'project_grayscale.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path,
        output_path=os.path.join('data', 'project_blurred.avi')
    )
