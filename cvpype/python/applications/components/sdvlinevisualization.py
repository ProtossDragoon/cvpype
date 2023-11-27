# Project-Types
from cvpype.python.core.types.output import NoOutput
from cvpype.python.core.types.image import RGBImageType
from cvpype.python.applications.types.line import OpenCVLinesType as LinesType
from cvpype.python.applications.types.coord import OpenCVCoordinatesType as CoordinatesType

# Project-Components
from cvpype.python.core.components.base import BaseComponent

# Project-Visualizers
from cvpype.python.applications.visualizer.sdvline import SDVLineAndEdgePairVisualizer

from cvpype.python.core.iospec import ComponentIOSpec


class SDVLineVisualizationComponent(BaseComponent):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=RGBImageType(),
        ),
        ComponentIOSpec(
            name='lines',
            data_container=LinesType(),
        ),
        ComponentIOSpec(
            name='intersections',
            data_container=CoordinatesType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='NoOutput',
            data_container=NoOutput(),
        )
    ]
    visualizer = SDVLineAndEdgePairVisualizer(
        'SDVLineVisualizationComponent'
    )

    def __init__(
        self,
        y_origin: int,
        roi_y: int,
    ):
        super().__init__()
        self.visualizer.y_origin = y_origin
        self.visualizer.roi_y = roi_y

    def run(
        self,
        image,
        lines,
        intersections,
    ):
        self.visualize(image, lines, intersections)
