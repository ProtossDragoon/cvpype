# Project-Types
from cvpype.python.applications.types.image import OpenCVRGBImageType

# Project-Components
from cvpype.python.core.components.inputs import InputsComponent
from cvpype.python.core.components.cropping import CroppingComponent
from cvpype.python.core.components.grayscailing import GrayscailingComponent
from cvpype.python.core.components.blurring import BilateralBlurringComponent
from cvpype.python.core.components.edgedetecting import EdgeDetectingComponent
from cvpype.python.applications.components.linefinding import LineFindingComponent
from cvpype.python.applications.components.sdvlinevisualization import SDVLineVisualizationComponent

# Project-Pipelines
from cvpype.python.applications.pipelines.intersection_finding import get_intersection_finding_pipeline


def get_line_tracking_pipeline(
   crop_y: int,
   crop_y_end: int,
   roi_y: int,
   image_h: int
):
    assert crop_y < roi_y < crop_y_end <= image_h

    inputs = InputsComponent()
    grayscailing = GrayscailingComponent()
    cropping = CroppingComponent(
        y=crop_y,
        y_end=crop_y_end,
    )
    cropping.change_output_type('image', OpenCVRGBImageType)
    blurring = BilateralBlurringComponent()
    edge_detecting = EdgeDetectingComponent()
    line_finding = LineFindingComponent()
    intersection_finding = get_intersection_finding_pipeline(
        roi_y=(roi_y-crop_y),
        width_min=10,
        width_max=50,
    )
    line_visualizing = SDVLineVisualizationComponent(
        y_origin=crop_y,
        roi_y=roi_y,
    )

    def fn(color_image):
        color_image = inputs(color_image)
        cropped_color_image = cropping(color_image)
        cropped_gray_image = grayscailing(cropped_color_image)
        cropped_blurred_gray_image = blurring(cropped_gray_image)
        cropped_edge_image = edge_detecting(cropped_blurred_gray_image)
        lines = line_finding(cropped_edge_image)
        intersections = intersection_finding(
            cropped_color_image,
            cropped_edge_image
        )
        line_visualizing(
            color_image,
            lines,
            intersections
        )
        return intersections

    return fn
