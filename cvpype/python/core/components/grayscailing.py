import cv2

from cvpype.python.core.components.base import BaseComponent
from cvpype.python.core.iospec import ComponentIOSpec
from cvpype.python.core.visualizer.image import ImageVisualizer
from cvpype.python.core.types.image import RGBImageType, GrayscaledImageType
from cvpype.python.utils.component import \
    run_component_with_singular_input_of_ImageType


class GrayscailingComponent(BaseComponent):
    """Converts an RGB image to a grayscaled image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=RGBImageType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='image',
            data_container=GrayscaledImageType(),
        )
    ]
    visualizer = ImageVisualizer(
        name='GrayscailingComponent'
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
    video_path = os.path.join('data', 'project.avi')
    output_path = os.path.join('data', 'project_grayscale.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path, output_path=output_path
    )
