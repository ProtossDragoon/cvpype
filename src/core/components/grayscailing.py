import cv2

from src.core.components.base import BaseComponent
from src.core.iospec import ComponentIOSpec
from src.applications.visualizer.image import (
    CVImageVisualizer as ImageVisualizer
) # FIXME: Application layer should not be called by core layer
from src.applications.types.image import (
    OpenCVRGBImageType as RGBImageType,
    OpenCVGrayscaledImageType as GrayscaledImageType,
) # FIXME: Application layer should not be called by core layer
from src.utils.component import \
    run_component_with_singular_input_of_ImageType


class GrayscailingComponent(BaseComponent):
    """Converts an RGB image to a grayscaled image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=RGBImageType(),
            allow_copy=False,
            allow_change=False,
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='image',
            data_container=GrayscaledImageType(),
            allow_copy=True,
            allow_change=False,
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
