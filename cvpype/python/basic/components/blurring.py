# Third party
import cv2

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import GrayscaledImageType, EdgeImageType

# Project-Visualizers
from cvpype.python.basic.visualizer.image import ImageVisualizer

# Project-Components
from cvpype.python.core.components.base import IOBaseComponent

# Project-Utils
from cvpype.python.utils.component import \
    run_component_with_singular_input_of_ImageType


class BilateralBlurringComponent(IOBaseComponent):
    """Applies bilateral Gaussian blurring to a grayscaled image.
    """

    def __init__(
        self
    ):
        super().__init__(
            inputs=[
                ComponentIOSpec(
                    name='image',
                    data_container=GrayscaledImageType(),
                )
            ],
            outputs=[
                ComponentIOSpec(
                    name='image',
                    data_container=EdgeImageType(),
                )],
            visualizer=ImageVisualizer(
                name='BilateralBlurringComponent'
            )
        )

    def run(
        self,
        image,
        sigma_color: int = 10,
        sigma_space: int = 10
    ) -> dict:
        """
        The function applies bilateral Gaussian blurring to an image and returns the blurred image.

        @param image The input image that you want to apply bilateral Gaussian blurring to.
        @param sigma_color The sigma_color parameter controls the color similarity between neighboring
        pixels. A higher value will result in more colors being considered similar, resulting in a smoother
        image. Conversely, a lower value will result in less colors being considered similar, resulting in a
        more detailed image.
        @param sigma_space The sigma_space parameter in the bilateral filter function determines the spatial
        extent of the filter. It controls how much the pixels farther away from the central pixel influence
        the blurring. A higher value of sigma_space will result in a larger spatial neighborhood being
        considered for blurring, leading to a more extensive blurring

        @return a dictionary with the key 'image', which is the name of the defined output component spec,
        and the value being the blurred image.
        """
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
