# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import ImageType

# Project-Visualizers
from cvpype.python.basic.visualizer.image import ImageVisualizer

# Project-Components
from cvpype.python.core.components.base import BaseComponent

# Project-Utils
from cvpype.python.utils.component import \
    run_component_with_singular_input_of_ImageType


class CroppingComponent(BaseComponent):
    """Crops the upper side (from 0 to y) of an image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=ImageType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='image',
            data_container=ImageType(),
        )
    ]
    visualizer = ImageVisualizer(
        name='CroppingComponent'
    )

    def __init__(
        self,
        y: int = None,
        y_end: int = None,
        x: int = None,
        x_end: int = None,
    ):
        super().__init__()
        self.y = y
        self.y_end = y_end
        self.x = x
        self.x_end = x_end

    def run(
        self,
        image
    ) -> dict:
        height, width = image.shape[0], image.shape[1]
        if self.y is None:
            self.y = int(height / 2)
        if self.y_end is None:
            self.y_end = int(height)
        if self.x is None:
            self.x = 0
        if self.x_end is None:
            self.x_end = int(width)
        cropped_image = image[self.y:self.y_end, self.x:self.x_end]
        self.visualize(cropped_image)
        self.log('completed cropping operation.', level='debug')
        return {'image': cropped_image}


if __name__ == '__main__':
    component = CroppingComponent()
    import os
    video_path = os.path.join('data', 'project.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path
    )
