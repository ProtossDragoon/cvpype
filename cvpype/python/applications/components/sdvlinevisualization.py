# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.core.types.output import NoOutput # FIXME: Core layer should not be used in application layer
from cvpype.python.basic.types.cvimage import RGBImageType
from cvpype.python.applications.types.cvline import OpenCVLinesType
from cvpype.python.applications.types.cvcoord import OpenCVCoordinatesType

# Project-Components
from cvpype.python.basic.components.custom import CustomComponent

# Project-Visualizers
from cvpype.python.applications.visualizer.sdvline import SDVLineAndEdgePairVisualizer


class SDVLineVisualizationComponent(CustomComponent):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=RGBImageType(),
        ),
        ComponentIOSpec(
            name='lines',
            data_container=OpenCVLinesType(),
        ),
        ComponentIOSpec(
            name='intersections',
            data_container=OpenCVCoordinatesType(),
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
