# Third Party
import cv2

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import ImageType
from cvpype.python.applications.types.cvline import OpenCVLinesType

# Project-Visualizers
from cvpype.python.basic.visualizer.image import ImageVisualizer


class CVLineOnCVImageVisualizer(ImageVisualizer):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=ImageType(),
        ),
        ComponentIOSpec(
            name='lines',
            data_container=OpenCVLinesType(),
        )
    ]

    def paint(
        self,
        image: ImageType,
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
        return v_image
