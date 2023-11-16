from src.core.types.image import ImageType
from src.core.types.line import LinesType
from src.core.visualizer.base import BaseVisualizer
from src.core.visualizer.base import CombinedVisualizer


class LineVisualizer(BaseVisualizer):
    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name)

    def visualize(
        self,
        image: ImageType,
    ):
        raise NotImplementedError


class LineOnImageVisualizer(CombinedVisualizer):
    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name)

    def visualize(
        self,
        image: ImageType,
        lines: LinesType
    ):
        raise NotImplementedError
