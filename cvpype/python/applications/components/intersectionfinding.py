# Third party
import numpy as np

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.basic.types.cvimage import EdgeImageType
from cvpype.python.applications.types.cvcoord import CVCoordinatesType

# Project-Components
from cvpype.python.basic.components.custom import CustomComponent


class IntersectionFindingComponent(CustomComponent):
    inputs = [
        ComponentIOSpec(
            name='edge_image',
            data_container=EdgeImageType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='intersections',
            data_container=CVCoordinatesType(),
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
