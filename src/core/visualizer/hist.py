# Third party
import matplotlib.pyplot as plt

# Project
from src.core.visualizer.base import BaseVisualizer


class HistogramVisualizer(BaseVisualizer):
    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name, is_operating)
        self.fig = plt.figure()

    def runtime_init(
        self
    ):
        try:
            self.fig.canvas.set_window_title(self.name)
        except AttributeError:
            # FIXME: via logger
            print("MacOS cannot set the title of matplotlib window.")
