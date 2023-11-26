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
        plt.show()
        try:
            self.fig.canvas.set_window_title(self.name)
        except AttributeError:
            self.logger.warning(
                'MacOS cannot set the title of matplotlib window.'
            )

    # FIXME: Dirty api
    def xbound_proper_min(
        self,
        li: list
    ):
        return min(li)

    # FIXME: Dirty api
    def ybound_proper_min(
        self,
        li: list
    ):
        return 0

    # FIXME: Dirty api
    def xbound_proper_max(
        self,
        li: list
    ):
        return max(li)

    # FIXME: Dirty api
    def ybound_proper_max(
        self,
        li: list
    ):
        return len(li)
