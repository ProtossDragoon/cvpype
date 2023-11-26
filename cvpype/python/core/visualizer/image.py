from cvpype.python.core.visualizer.base import BaseVisualizer


class ImageVisualizer(BaseVisualizer):
    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name, is_operating)
