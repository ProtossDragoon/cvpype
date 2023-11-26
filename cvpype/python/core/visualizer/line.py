from cvpype.python.core.types.image import ImageType
from cvpype.python.core.types.line import LinesType
from cvpype.python.core.visualizer.base import BaseVisualizer
from cvpype.python.core.visualizer.base import CombinedVisualizer


class LineVisualizer(BaseVisualizer):
    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name)


class LineOnImageVisualizer(CombinedVisualizer):
    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name)
