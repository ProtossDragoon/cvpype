# Built-in
from math import pi

# Third party
import cv2

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import EdgeImageType
from cvpype.python.applications.types.cvline import CVLinesType

# Project-Components
from cvpype.python.basic.components.custom import CustomComponent

# Project-Visualizers
from cvpype.python.applications.visualizer.line import (
    CVLineOnImageVisualizer as LineOnImageVisualizer
)

# Project-Utils
from cvpype.python.utils.component import \
    run_component_with_singular_input_of_ImageType


class LineFindingComponent(CustomComponent):
    """Finds lines in an edge-detected image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=EdgeImageType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='lines',
            data_container=CVLinesType(),
        )
    ]
    visualizer = LineOnImageVisualizer(
        name='LineFindingComponent'
    )

    def run(
        self,
        image,
        threshold: int = 40,
        minLineLength: int = 10,
        maxLineGap: int = 100,
    ) -> dict:
        lines = cv2.HoughLinesP(
            image,
            rho=1,
            theta=pi/180,
            threshold=threshold,
            minLineLength=minLineLength,
            maxLineGap=maxLineGap
        )
        if lines is None:
            lines = []
        self.log(f'found {len(lines)} lines', level='debug')
        self.visualize(image, lines)
        return {'lines': lines}


if __name__ == '__main__':
    component = LineFindingComponent()
    import os
    video_path = os.path.join('data', 'project_edge.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path
    )
