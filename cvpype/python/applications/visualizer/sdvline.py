# Third Party
import cv2

# Project
from cvpype.python.core.iospec import ComponentIOSpec
from cvpype.python.applications.types.image import OpenCVRGBImageType
from cvpype.python.applications.types.line import OpenCVLinesType
from cvpype.python.applications.types.coord import OpenCVCoordinatesType
from cvpype.python.core.visualizer.base import BaseVisualizer


class SDVLineAndEdgePairVisualizer(BaseVisualizer):
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
        self.roi_y = 0

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
        palette = [
            (0, 255, 0),
            (50, 200, 0),
            (100, 150, 0),
            (150, 100, 0),
            (200, 50, 0)
        ]
        for i, pair in enumerate(intersections.data, 1):
            x1, x2 = pair
            y = self.roi_y
            cv2.drawMarker(
                v_image,
                (x1, y),
                palette[len(palette) % i],
                markerType=cv2.MARKER_CROSS,
                markerSize=10,
                thickness=2,
                line_type=cv2.LINE_AA
            )
            cv2.drawMarker(
                v_image,
                (x2, y),
                palette[len(palette) % i],
                markerType=cv2.MARKER_CROSS,
                markerSize=10,
                thickness=2,
                line_type=cv2.LINE_AA
            )
            cv2.putText(
                v_image,
                f"({abs(x1-x2)})",
                (x1, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
        cv2.imshow(self.name, v_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow(self.name)
            cv2.waitKey(1)
            self.is_operating = False
