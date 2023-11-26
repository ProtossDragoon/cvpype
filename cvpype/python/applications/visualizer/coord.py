# Built-in
from typing import Callable
from collections import deque

# Third Party
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Project
from cvpype.python.core.iospec import ComponentIOSpec
from cvpype.python.core.types.image import ImageType
from cvpype.python.core.types.coord import CoordinatesType
from cvpype.python.applications.types.coord import OpenCVCoordinatesType
from cvpype.python.core.visualizer.image import ImageVisualizer
from cvpype.python.core.visualizer.matplt import MatPltVisualizer


class CVCoordsOnCVImageVisualizer(ImageVisualizer):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=ImageType(),
            allow_copy=True,
            allow_change=False,
        ),
        ComponentIOSpec(
            name='coordinates',
            data_container=OpenCVCoordinatesType(),
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

    def paint(
        self,
        image: ImageType,
        coords: OpenCVCoordinatesType
    ):
        v_image = cv2.cvtColor(image.data, cv2.COLOR_GRAY2BGR)
        for coord in coords.data:
            cv2.drawMarker(
                v_image, coord,
                markerType=cv2.MARKER_CROSS,
                color=(0, 0, 255),
                markerSize=10,
                thickness=2
            )
            cv2.putText(
                v_image, f"{coord}", coord,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(0, 0, 255),
                thickness=1
            )
        return v_image


class CoordsHistogramVisualizer(MatPltVisualizer):
    inputs = [
        ComponentIOSpec(
            name='coordinates',
            data_container=CoordinatesType(),
            allow_copy=False,
            allow_change=False,
        )
    ]

    def __init__(
        self,
        name: str,
        is_operating: bool = True,
        histogram_min_x: int = None,
        histogram_max_x: int = None,
        histogram_min_y: int = None,
        histogram_max_y: int = None,
        history_maxlen: int = 100,
    ) -> None:
        super().__init__(name, is_operating)
        self.histogram_min_x = histogram_min_x
        self.histogram_max_x = histogram_max_x
        self.histogram_min_y = histogram_min_y
        self.histogram_max_y = histogram_max_y
        self.ax_hist = plt.subplot(211)
        self.ax_hist.grid()
        self.ax_line = plt.subplot(212)
        self.ax_line.grid()
        self.n_bins = 30
        self.history_maxlen = history_maxlen
        self.hist, = self.ax_hist.plot(
            np.arange(self.n_bins,),
            np.zeros((self.n_bins,)),
            c='lightblue', alpha=0.5
        )
        self.line, = self.ax_line.plot(
            np.arange(self.history_maxlen,),
            np.zeros((self.history_maxlen,)),
            '-o', c='salmon', alpha=0.5
        )
        self.ax_line.set_xlim(0, self.history_maxlen)
        self.history = deque(
            [0] * self.history_maxlen,
            maxlen=self.history_maxlen
        )
        plt.ion()

    def paint(
        self,
        coords: CoordinatesType,
        parse_fn: Callable,
        parse_history_fn: Callable,
    ):
        li = [parse_fn(*coord) for coord in coords.data]
        if not li:
            return
        self.history.append(parse_history_fn(li))

        # histogram
        # FIXME: dirty api
        if self.histogram_min_x:
            histogram_min_x = self.histogram_min_x
        else:
            histogram_min_x = self.xbound_proper_min(li)
        if self.histogram_max_x:
            histogram_max_x = self.histogram_max_x
        else:
            histogram_max_x = self.xbound_proper_max(li)

        if self.histogram_min_y:
            histogram_min_y = self.histogram_min_y
        else:
            histogram_min_y = self.ybound_proper_min(li)
        if self.histogram_max_x:
            histogram_max_y = self.histogram_max_y
        else:
            histogram_max_y = self.ybound_proper_max(li)

        x_hist = np.linspace(
            histogram_min_x,
            histogram_max_x,
            self.n_bins
        )
        y_hist, _ = np.histogram(
            li, bins=np.linspace(
                histogram_min_x,
                histogram_max_x,
                self.n_bins+1
            )
        )
        self.hist.set_xdata(x_hist)
        self.ax_hist.set_xlim(
            histogram_min_x,
            histogram_max_x
        )
        self.hist.set_ydata(y_hist)
        self.ax_hist.set_ylim(
            histogram_min_y,
            histogram_max_y
        )

        # line
        self.line.set_ydata(self.history)
        self.ax_line.set_ylim(0, max(self.history) * 2) #FIXME: slow
