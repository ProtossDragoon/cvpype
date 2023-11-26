# Third Party
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Project
from cvpype.python.core.iospec import ComponentIOSpec
from cvpype.python.core.types.image import (
    ImageType,
    RGBImageType,
    HSVImageType,
    GrayscaledImageType
)
from cvpype.python.core.visualizer.matplt import MatPltVisualizer


class CVRGBImageHistogramVisualizer(MatPltVisualizer):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=RGBImageType(),
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
        lw = 3
        alpha = 0.5
        self.bins = 255
        self.fig, self.ax = plt.subplots()
        self.line_r, = self.ax.plot(
            np.arange(self.bins),
            np.zeros((self.bins,)),
            c='r', lw=lw, alpha=alpha, label='Red'
        )
        self.line_g, = self.ax.plot(
            np.arange(self.bins),
            np.zeros((self.bins,)),
            c='g', lw=lw, alpha=alpha, label='Green'
        )
        self.line_b, = self.ax.plot(
            np.arange(self.bins),
            np.zeros((self.bins,)),
            c='b', lw=lw, alpha=alpha, label='Blue'
        )
        self.ax.set_xlim(0, self.bins-1)
        self.ax.set_ylim(0, 1)
        self.ax.legend()
        plt.ion()

    def paint(
        self,
        image: ImageType
    ):
        (b, g, r) = cv2.split(image)
        n_pixels = np.prod(image.shape[:2])
        histogram_r = cv2.calcHist([r], [0], None, [self.bins], [0, 255]) / n_pixels
        histogram_g = cv2.calcHist([g], [0], None, [self.bins], [0, 255]) / n_pixels
        histogram_b = cv2.calcHist([b], [0], None, [self.bins], [0, 255]) / n_pixels
        self.line_r.set_ydata(histogram_r)
        self.line_g.set_ydata(histogram_g)
        self.line_b.set_ydata(histogram_b)


class CVGrayScaledImageHistogramVisualizer(MatPltVisualizer):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=GrayscaledImageType(),
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
        lw = 3
        self.bins = 255
        self.fig, self.ax = plt.subplots()
        self.line_gray, = self.ax.plot(
            np.arange(self.bins),
            np.zeros((self.bins, 1)),
            c='k', lw=lw, label='intensity'
        )
        self.ax.set_xlim(0, self.bins-1)
        self.ax.set_ylim(0, 1)
        self.ax.legend()
        plt.ion()

    def paint(
        self,
        image: ImageType
    ):
        n_pixels = np.prod(image.shape[:2])
        histogram = cv2.calcHist([image], [0], None, [self.bins], [0, 255]) / n_pixels
        self.line_gray.set_ydata(histogram)


class CVHSVImageHistogramVisualizer(MatPltVisualizer):
    inputs = [
        ComponentIOSpec(
            name='image',
            data_container=ImageType(),
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
        lw = 3
        alpha = 0.5
        self.bins = 255
        self.fig, self.ax = plt.subplots()
        self.line_h, = self.ax.plot(
            np.arange(self.bins,),
            np.zeros((self.bins,)),
            c='y', lw=lw, alpha=alpha, label='H'
        )
        self.line_s, = self.ax.plot(
            np.arange(self.bins),
            np.zeros((self.bins,)),
            c='r', lw=lw, alpha=alpha, label='S'
        )
        self.line_v, = self.ax.plot(
            np.arange(self.bins),
            np.zeros((self.bins,)),
            c='k', lw=lw, alpha=alpha, label='V'
        )
        self.ax.set_xlim(0, self.bins-1)
        self.ax.set_ylim(0, 1)
        self.ax.legend()
        plt.ion()

    def paint(
        self,
        image: ImageType
    ):
        (h, s, v) = cv2.split(image)
        n_pixels = np.prod(image.shape[:2])
        histogram_h = cv2.calcHist([h], [0], None, [self.bins], [0, 255]) / n_pixels
        histogram_s = cv2.calcHist([s], [0], None, [self.bins], [0, 255]) / n_pixels
        histogram_v = cv2.calcHist([v], [0], None, [self.bins], [0, 255]) / n_pixels
        self.lineH.set_ydata(histogram_h)
        self.lineS.set_ydata(histogram_s)
        self.lineV.set_ydata(histogram_v)
