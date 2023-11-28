# Third party
import cv2
import numpy as np

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import RGBImageType
from cvpype.python.applications.types.cvcoord import OpenCVCoordinatesType

# Project-Components
from cvpype.python.basic.components.custom import CustomComponent

# Project-Visualizers
from cvpype.python.applications.visualizer.coord import CoordsHistogramVisualizer


class WidthBasedIntersectionFilteringComponent(CustomComponent):
    inputs = [
        ComponentIOSpec(
            name='intersections',
            data_container=OpenCVCoordinatesType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='intersections',
            data_container=OpenCVCoordinatesType(),
        )
    ]
    visualizer = CoordsHistogramVisualizer(
        name='WidthBasedIntersectionFiltering'
    )

    def __init__(
        self,
        width_min: int = 3,
        width_max: int = 30,
    ):
        super().__init__()
        self.width_min = width_min
        self.width_max = width_max

    def run(
        self,
        intersections,
    ) -> dict:
        valid_pairs = [
            (start_idx, end_idx) for start_idx, end_idx in intersections
            if self.width_min <= end_idx - start_idx <= self.width_max
        ]
        self.log(f'Intersections: {len(valid_pairs)}/{len(intersections)} '
                 f'(#filtered/#input)')
        self.visualize(
            intersections,
            parse_fn=(lambda x1, x2: abs(x1 - x2)),
            parse_history_fn=(lambda li: len(li))
        )
        return {'intersections': valid_pairs}


class ColorBasedIntersectionFilteringComponent(CustomComponent):
    inputs = [
        ComponentIOSpec(
            name='color_image',
            data_container=RGBImageType(),
        ),
        ComponentIOSpec(
            name='valid_pairs',
            data_container=OpenCVCoordinatesType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='filtered_pairs',
            data_container=OpenCVCoordinatesType(),
        )
    ]

    def __init__(
        self,
        y: int,
        black_threshold: int = 230,  # FIXME: manual
    ):
        super().__init__()
        self.y = y
        self.black_threshold = black_threshold

    def run(
        self,
        color_image,
        valid_pairs,
    ) -> dict:
        color_row = color_image[self.y]

        # HSV 공간을 사용하여 분석합니다. 전체 이미지를 변환하는 대신 필요한 행만 변환합니다.
        hsv_row = cv2.cvtColor(np.array([color_row]), cv2.COLOR_BGR2HSV)
        _, _, v_row = cv2.split(hsv_row)

        BIN_COUNT = 256
        hist = cv2.calcHist([hsv_row], [0], None, [BIN_COUNT], [0, 256])

        # 에지 쌍 내부 영역이 검은색인지 확인합니다.
        valid_black_pairs = []
        for start, end in valid_pairs:
            line_section = v_row[start:end] # V 채널을 사용합니다.
            black_pixels = len(np.where(line_section < self.black_threshold)[0])

            if black_pixels / (len(line_section) + 0.1) >= 0.5:
                valid_black_pairs.append((start, end))

        self.log(f'Intersections: {len(valid_black_pairs)}/{len(valid_pairs)} '
                 f'(#filtered/#input)')

        return {'filtered_pairs': valid_black_pairs}


if __name__ == '__main__':
    pass
