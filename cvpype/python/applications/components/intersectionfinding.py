import numpy as np

from cvpype.python.core.components.base import BaseComponent
from cvpype.python.core.iospec import ComponentIOSpec
from cvpype.python.applications.types.image import (
    OpenCVEdgeImageType as EdgeImageType
)
from cvpype.python.applications.types.coord import (
    OpenCVCoordinatesType as CoordinatesType
)


class IntersectionFindingComponent(BaseComponent):
    inputs = [
        ComponentIOSpec(
            name='edge_image',
            data_container=EdgeImageType(),
            allow_copy=False,
            allow_change=False,
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='intersections',
            data_container=CoordinatesType(),
            allow_copy=True,
            allow_change=False,
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
