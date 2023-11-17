# Third Party
import cv2

# Projects
from src.core.iospec import ComponentIOSpec
from src.applications.types.image import CVImageType
from src.core.visualizer.image import ImageVisualizer


class CVImageVisualizer(ImageVisualizer):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_type=CVImageType(),
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
        image: CVImageType
    ):
        if self.is_operating:
            cv2.imshow(self.name, image.data)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyWindow(self.name)
                cv2.waitKey(1)
                self.is_operating = False
