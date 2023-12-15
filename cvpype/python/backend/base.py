# Built-in
import logging
from abc import ABC
from abc import abstractmethod
from threading import Lock, Thread

# Third party
import imutils


class BaseStreamer(ABC):
    def __set_logger(
        self,
    ):
        self.logger = logging.getLogger(
            f'{self.__class__.__name__}'
        )
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(
            f'(%(asctime)s)[%(levelname)s]:%(module)s.%(name)s: %(message)s',
            datefmt='%Y/%m/%d-%H:%M:%S',
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def __init__(
        self, /, *,
        width: int | None = None,
        height: int | None = None,
    ):
        """! Video stream with a specified width and height

        @param width The `width` parameter is an optional integer that represents the width of the video
        stream. If no value is provided, it defaults to `None`. If you set `width` to None,
        width value will be set by the original width of the stream on run-time.
        @param height The `height` parameter is an optional integer that represents the desired height of
        the video stream. If no value is provided, it defaults to `None`. If you set `height` to None,
        height value will be set by the original width of the stream on run-time.
        """
        self.__set_logger()
        self._output_frame_locker = Lock()
        self._output_frame = None
        self.width = width
        self.height = height

    @abstractmethod
    def read_from_stream(
        self
    ) -> None:
        """ This function write value on `self.output_frame`.
        """
        raise NotImplementedError

    def open(
        self
    ) -> None:
        thread = Thread(target=self.read_from_stream, daemon=True)
        thread.start()

    @abstractmethod
    def close(
        self
    ) -> None:
        raise NotImplementedError

    @property
    def output_frame(
        self
    ):
        with self._output_frame_locker:
            return self._output_frame

    @output_frame.setter
    def output_frame(
        self,
        img
    ):
        img = imutils.resize(img, width=self.width, height=self.height)
        with self._output_frame_locker:
            if (not self.height) or (not self.width):
                self.height, self.width = img.shape[0:2]
            self._output_frame = img.copy()
