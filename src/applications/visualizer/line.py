# Third Party
import cv2

# Project
from src.core.iospec import ComponentIOSpec
from src.applications.types.image import OpenCVImageType
from src.applications.types.line import OpenCVLinesType
from src.core.visualizer.line import LineOnImageVisualizer


class CVLineOnCVImageVisualizer(LineOnImageVisualizer):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=OpenCVImageType(),
            allow_copy=True,
            allow_change=False,
        ),
        ComponentIOSpec(
            name='lines',
            data_container=OpenCVLinesType(),
            allow_copy=False,
            allow_change=False,
        )
    ]

    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name, is_operating)

    def visualize(
        self,
        image: OpenCVImageType,
        lines: OpenCVLinesType
    ):
        v_image = cv2.cvtColor(image.data, cv2.COLOR_GRAY2BGR)
        for line in lines.data:
            for x1, y1, x2, y2 in line:
                cv2.line(
                    v_image,
                    (x1, y1), (x2, y2),
                    (0, 0, 255), 2
                )
        cv2.imshow(self.name, v_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow(self.name)
            cv2.waitKey(1)
            self.is_operating = False
