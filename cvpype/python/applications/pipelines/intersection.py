# Project-Components
from cvpype.python.basic.components.inputs import InputsComponent
from cvpype.python.applications.components.intersectionfinding import IntersectionFindingComponent
from cvpype.python.applications.components.intersectionfiltering import (
    WidthBasedIntersectionFilteringComponent,
    ColorBasedIntersectionFilteringComponent
)

# Project-Pipelines
from cvpype.python.basic.pipelines.custom import CustomPipeline


class IntersectionPipeline(CustomPipeline):
    def __init__(
        self,
        roi_y: int,
        width_min: int,
        width_max: int,
    ) -> None:
        super().__init__()
        self.roi_y = roi_y
        self.width_min = width_min
        self.width_max = width_max

        self.inputs = InputsComponent()
        self.intersection_finding = IntersectionFindingComponent(
            y=self.roi_y
        )
        self.width_based_filtering = WidthBasedIntersectionFilteringComponent(
            width_min=self.width_min,
            width_max=self.width_max
        )
        self.color_based_filtering = ColorBasedIntersectionFilteringComponent(
            y=self.roi_y
        )

    def run(
        self,
        color_image,
        edge_image
    ):
        color_image, edge_image = self.inputs(color_image, edge_image)
        intersections = self.intersection_finding(edge_image)
        intersections = self.width_based_filtering(intersections)
        # intersections = color_based_filtering(color_image, intersections)
        return intersections
