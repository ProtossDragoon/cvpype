from cvpype.python.core.iospec import ComponentIOSpec
from cvpype.python.core.types.output import NoOutput

from cvpype.python.core.components.base import BaseComponent
from cvpype.python.applications.types.image import OpenCVRGBImageType as RGBImageType
from cvpype.python.applications.types.line import OpenCVLinesType as LinesType
from cvpype.python.applications.types.coord import OpenCVCoordinatesType as CoordinatesType

from cvpype.python.applications.visualizer.sdvline import SDVLineVisualizer


class SDVLineVisualizationComponent(BaseComponent):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=RGBImageType(),
            allow_copy=False,
            allow_change=False,
        ),
        ComponentIOSpec(
            name='lines',
            data_container=LinesType(),
            allow_copy=True,
            allow_change=False,
        ),
        ComponentIOSpec(
            name='intersections',
            data_container=CoordinatesType(),
            allow_copy=True,
            allow_change=False,
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='NoOutput',
            data_container=NoOutput(),
            allow_copy=False,
            allow_change=False
        )
    ]
    visualizer = SDVLineVisualizer(
        'SDVLineVisualizationComponent'
    )

    def __init__(
        self,
        y_origin: int,
    ):
        super().__init__()
        self.visualizer.y_origin = y_origin

    def run(
        self,
        image,
        lines,
        intersections,
    ):
        self.visualize(image, lines, intersections)
