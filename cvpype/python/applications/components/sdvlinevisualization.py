# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import RGBImageType
from cvpype.python.applications.types.cvline import CVLinesType
from cvpype.python.applications.types.cvcoord import CVCoordinatesType

# Project-Components
from cvpype.python.basic.components.custom import CustomVisualizationComponent

# Project-Visualizers
from cvpype.python.applications.visualizer.sdvline import SDVLineAndEdgePairVisualizer


class SDVLineVisualizationComponent(CustomVisualizationComponent):

    def __init__(
        self,
        y_origin: int,
        roi_y: int,
    ):
        super().__init__(
            inputs=[
                ComponentIOSpec(
                    name='image',
                    data_container=RGBImageType(),
                ),
                ComponentIOSpec(
                    name='lines',
                    data_container=CVLinesType(),
                ),
                ComponentIOSpec(
                    name='intersections',
                    data_container=CVCoordinatesType(),
                )
            ],
            visualizer=SDVLineAndEdgePairVisualizer(
                'SDVLineVisualizationComponent'
            )
        )
        self.visualizer.y_origin = y_origin
        self.visualizer.roi_y = roi_y

    def run(
        self,
        image,
        lines,
        intersections,
    ):
        self.visualize(image, lines, intersections)
