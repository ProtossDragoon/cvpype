import cv2

from cvpype.python.core.components.base import BaseComponent
from cvpype.python.core.iospec import ComponentIOSpec
from cvpype.python.core.visualizer.image import ImageVisualizer
from cvpype.python.core.types.image import GrayscaledImageType, EdgeImageType
from cvpype.python.utils.component import \
    run_component_with_singular_input_of_ImageType


class EdgeDetectingComponent(BaseComponent):
    """Applies edge detection to a grayscaled image.
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
