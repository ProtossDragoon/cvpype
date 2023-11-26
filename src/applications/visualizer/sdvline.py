# Third Party
import cv2

# Project
from src.core.iospec import ComponentIOSpec
from src.applications.types.image import OpenCVRGBImageType
from src.applications.types.line import OpenCVLinesType
from src.applications.types.coord import OpenCVCoordinatesType
from src.core.visualizer.base import BaseVisualizer


class SDVLineVisualizer(BaseVisualizer):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=OpenCVRGBImageType(),
            allow_copy=True,
            allow_change=False,
        ),
        ComponentIOSpec(
            name='lines',
            data_container=OpenCVLinesType(),
            allow_copy=False,
            allow_change=False,
        ),
        ComponentIOSpec(
            name='intersections',
            data_container=OpenCVCoordinatesType(),
            allow_copy=True,
            allow_change=False,
        )
    ]

    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name, is_operating)
        self.y_origin = 0

    def visualize(
        self,
        image: OpenCVRGBImageType,
        lines: OpenCVLinesType,
        intersections: OpenCVCoordinatesType
    ):
        v_image = image.data
        for line in lines.data:
            for x1, y1, x2, y2 in line:
                y1 += self.y_origin
                y2 += self.y_origin
                cv2.line(
                    v_image,
                    (x1, y1), (x2, y2),
                    (0, 0, 255), 2
                )
        for coord in intersections.data:
            cv2.drawMarker(
                v_image,
                tuple(coord),
                (0, 255, 0),
                markerType=cv2.MARKER_CROSS,
                markerSize=10,
                thickness=2,
                line_type=cv2.LINE_AA
            )
        cv2.imshow(self.name, v_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow(self.name)
            cv2.waitKey(1)
            self.is_operating = False
