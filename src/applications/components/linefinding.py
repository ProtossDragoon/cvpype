from math import pi

import cv2

from src.core.components.base import BaseComponent
from src.core.iospec import ComponentIOSpec
from src.applications.visualizer.line import (
    CVLineOnCVImageVisualizer as LineOnImageVisualizer
)
from src.applications.types.image import (
    OpenCVEdgeImageType as EdgeImageType,
)
from src.applications.types.line import (
    OpenCVLinesType as LinesType,
)
from src.utils.component import \
    run_component_with_singular_input_of_ImageType


class LineFindingComponent(BaseComponent):
    """Finds lines in an edge-detected image.
    """
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=EdgeImageType(),
            allow_copy=False,
            allow_change=False,
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='lines',
            data_container=LinesType(),
            allow_copy=True,
            allow_change=False,
        )
    ]
    visualizer = LineOnImageVisualizer(
        name='LineFindingComponent'
    )

    def __init__(
        self,
        do_logging: bool = True
    ):
        super().__init__(do_logging)

    def run(
        self,
        image,
        threshold: int = 100,
        minLineLength: int = 10,
        maxLineGap: int = 250,
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
        # Assuming visualize method can also handle line visualization
        self.log(f'found {len(lines)} lines', level='debug')
        self.visualize(image, lines) # TODO: FIX, REMOVE
        return {'lines': lines}


if __name__ == '__main__':
    component = LineFindingComponent()
    import os
    video_path = os.path.join('data', 'project_edge.avi')
    run_component_with_singular_input_of_ImageType(
        component, video_path
    )
