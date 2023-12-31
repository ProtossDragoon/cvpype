# Third Party
import cv2

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import RGBImageType
from cvpype.python.applications.types.cvline import CVLinesType
from cvpype.python.applications.types.cvcoord import CVCoordinatesType

# Project-Visualizers
from cvpype.python.basic.visualizer.image import ImageVisualizer


class SDVLineAndEdgePairVisualizer(ImageVisualizer):
    inputs = [
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
    ]

    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name, is_operating)
        self.y_origin = 0
        self.roi_y = 0

    def paint(
        self,
        image: RGBImageType,
        lines: CVLinesType,
        intersections: CVCoordinatesType
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
        return v_image
