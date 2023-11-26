# Project-Types
from src.applications.types.image import OpenCVRGBImageType

# Project-Components
from src.core.components.inputs import InputsComponent
from src.core.components.cropping import CroppingComponent
from src.core.components.grayscailing import GrayscailingComponent
from src.core.components.blurring import BilateralBlurringComponent
from src.core.components.edgedetecting import EdgeDetectingComponent
from src.applications.components.linefinding import LineFindingComponent
from src.applications.components.sdvlinevisualization import SDVLineVisualizationComponent

# Project-Pipelines
from src.applications.pipelines.intersection_finding import get_intersection_finding_pipeline


def get_line_tracking_pipeline(
   crop_y: int,
   roi_y: int,
   image_h: int
):
    assert image_h > crop_y
    assert image_h > roi_y
    assert roi_y > crop_y

    inputs = InputsComponent()
    grayscailing = GrayscailingComponent()
    cropping = CroppingComponent(
        y=crop_y
    )
    cropping.change_output_type('image', OpenCVRGBImageType)
    blurring = BilateralBlurringComponent()
    edge_detecting = EdgeDetectingComponent()
    line_finding = LineFindingComponent()
    intersection_finding = get_intersection_finding_pipeline(
        y=(roi_y-crop_y),
        width_min=3,
        width_max=30
    )
    line_visualizing = SDVLineVisualizationComponent(
        y_origin=crop_y
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
