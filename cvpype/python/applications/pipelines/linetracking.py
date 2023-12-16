# Project-Types
from cvpype.python.basic.types.cvimage import RGBImageType

# Project-Components
from cvpype.python.basic.components.inputs import InputsComponent
from cvpype.python.basic.components.cropping import CroppingComponent
from cvpype.python.basic.components.grayscailing import GrayscailingComponent
from cvpype.python.basic.components.blurring import BilateralBlurringComponent
from cvpype.python.basic.components.edgedetecting import EdgeDetectingComponent
from cvpype.python.applications.components.linefinding import LineFindingComponent
from cvpype.python.applications.components.sdvlinevisualization import SDVLineVisualizationComponent

# Project-Pipelines
from cvpype.python.basic.pipelines.custom import CustomPipeline
from cvpype.python.applications.pipelines.intersection import IntersectionPipeline


class LineTrackingPipeline(CustomPipeline):
    def __init__(
        self,
        crop_y: int,
        crop_y_end: int,
        roi_y: int,
        image_h: int
    ) -> None:
        super().__init__()
        self.crop_y = crop_y
        self.crop_y_end = crop_y_end
        self.roi_y = roi_y
        self.image_h = image_h

        self.inputs = InputsComponent()
        self.grayscailing = GrayscailingComponent()
        self.cropping = CroppingComponent(
            y=crop_y,
            y_end=crop_y_end,
        )
        self.cropping.change_output_type('image', RGBImageType)
        self.blurring = BilateralBlurringComponent()
        self.edge_detecting = EdgeDetectingComponent()
        self.line_finding = LineFindingComponent()
        self.intersection_pipeline = IntersectionPipeline(
            roi_y=(self.roi_y-self.crop_y),
            width_min=10,
            width_max=50,
        )
        self.line_visualizing = SDVLineVisualizationComponent(
            y_origin=crop_y,
            roi_y=roi_y,
        )

    def is_valid(
        self
    ):
        assert (
            self.crop_y <
            self.roi_y <
            self.crop_y_end <=
            self.image_h
        )

    def run(
        self,
        color_image
    ):
        color_image = self.inputs(color_image)
        cropped_color_image = self.cropping(color_image)
        cropped_gray_image = self.grayscailing(cropped_color_image)
        cropped_blurred_gray_image = self.blurring(cropped_gray_image)
        cropped_edge_image = self.edge_detecting(cropped_blurred_gray_image)
        lines = self.line_finding(cropped_edge_image)
        intersections = self.intersection_pipeline.run(
            cropped_color_image,
            cropped_edge_image
        )
        self.line_visualizing(
            color_image,
            lines,
            intersections
        )
        return intersections
