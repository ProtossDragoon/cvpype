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


class EdgeDetectingComponent(BaseComponent):
    """Applies edge detection to a grayscaled image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=GrayscaledImageType(),
            allow_copy=False,
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
        name='EdgeDetectingComponent'
    )

    def run(
        self,
        image,
        threshold1: int = 100,
        threshold2: int = 200,
    ) -> dict:
        edge_image = cv2.Canny(
            image,
            threshold1,
            threshold2
        )
        self.visualize(edge_image)
        self.log('completed edge detection operation.', level='debug')
        return {'image': edge_image}


if __name__ == '__main__':
    component = EdgeDetectingComponent()
    import os
    video_path = os.path.join('data', 'project_grayscale.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path,
        output_path=os.path.join('data', 'project_edge.avi')
    )