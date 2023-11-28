# Third party
import matplotlib.pyplot as plt

# Project-Visualizers
from cvpype.python.core.visualizer.base import BaseVisualizer


class MatPltVisualizer(BaseVisualizer):
    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name, is_operating)
        self.fig = plt.figure()

    def __call__(
        self,
        *args,
        **kwargs
    ):
        super().__call__(*args, **kwargs)
        if self.is_operating:
            self.draw()

    def draw(
        self,
        *args,
        **kwargs
    ) -> None:
        self.fig.canvas.draw()

    def runtime_init(
        self
    ):
        plt.show()
        try:
            self.fig.canvas.set_window_title(self.name)
        except AttributeError:
            self.logger.warning(
                'MacOS cannot set the title of matplotlib window.'
            )
