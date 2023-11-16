import cv2

from src.core.types.image import ImageType
from src.core.visualizer.base import BaseVisualizer


class ImageVisualizer(BaseVisualizer):
    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name, is_operating)

    def visualize(
        self,
        image: ImageType
    ):
        raise NotImplementedError
