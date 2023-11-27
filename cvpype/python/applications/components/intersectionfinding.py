# Third party
import numpy as np

# Project-Types
from cvpype.python.core.types.image import EdgeImageType
from cvpype.python.applications.types.coord import (
    OpenCVCoordinatesType as CoordinatesType
)

# Project-Components
from cvpype.python.core.components.base import BaseComponent

from cvpype.python.core.iospec import ComponentIOSpec


class IntersectionFindingComponent(BaseComponent):
    inputs = [
        ComponentIOSpec(
            name='edge_image',
            data_container=EdgeImageType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='intersections',
            data_container=CoordinatesType(),
        )
    ]

    def __init__(
        self,
        y: int,
    ):
        super().__init__()
        self.y = y

    def run(
        self,
        edge_image,
    ) -> dict:
        EDGE_INTENSITY_THRESH = 255
        edge_row = edge_image[self.y]
        edge_idx = np.where(edge_row >= EDGE_INTENSITY_THRESH)[0]
        if len(edge_idx) <= 1:
            return {'intersections': []}
        edge_pairs = [
            (edge_idx[i], edge_idx[i + 1])
            for i in range(len(edge_idx) - 1)
        ]
        return {'intersections': edge_pairs}
