import cv2

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import RGBImageType, GrayscaledImageType

# Project-Visualizers
from cvpype.python.basic.visualizer.image import ImageVisualizer

# Project-Components
from cvpype.python.core.components.base import IOBaseComponent

# Project-Utils
from cvpype.python.utils.component import \
    run_component_with_singular_input_of_ImageType


class GrayscailingComponent(IOBaseComponent):
    """Converts an RGB image to a grayscaled image.
    """

    def __init__(
        self
    ):
        super().__init__(
            inputs = [
                ComponentIOSpec(
                    name='image',
                    data_container=RGBImageType(),
                )
            ],
            outputs = [
                ComponentIOSpec(
                    name='image',
                    data_container=GrayscaledImageType(),
                )
            ],
            visualizer = ImageVisualizer(
                name='GrayscailingComponent'
            )
        )

    def run(
        self,
        image
    ) -> dict:
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.visualize(grayscale_image)
        self.log('completed grayscale transformation.', level='debug')
        return {'image': grayscale_image}


if __name__ == '__main__':
    component = GrayscailingComponent()
    import os
    video_path = os.path.join('data', 'sample.avi')
    output_path = os.path.join('data', 'sample_grayscale.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path, output_path=output_path
    )
