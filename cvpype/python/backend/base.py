# Built-in
import logging
from abc import ABC
from abc import abstractmethod
from threading import Lock, Thread

# Third party
import imutils


# TODO: divide into input stream abstract class and output stream abstract class.
# TODO: refactor with producer-consumer structured threading.
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
        self.SIGNAL_NOTREADY = 'NOTREADY'
        self.__set_logger()
        self._output_frame_locker = Lock()
        self._output_frame = self.SIGNAL_NOTREADY
        self.width = width
        self.height = height

    @abstractmethod
    def read_from_stream(
        self
    ) -> None:
        """ This function writes value on `self.output_frame`.
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

    @property
    def is_ready(
        self
    ):
        with self._output_frame_locker:
            return self._output_frame is not self.SIGNAL_NOTREADY

    @output_frame.setter
    def output_frame(
        self,
        img
    ):
        if img is None:
            self.logger.warning(
                'Trying to set `output_frame` to None. Ignore this frame. '
                'Check something is trying to set `output_frame` before '
                'running `read_from_stream`, or implementation of `read_from_stream`. '
            )
            return
        img = imutils.resize(img, width=self.width, height=self.height)
        with self._output_frame_locker:
            if (not self.height) or (not self.width):
                self.height, self.width = img.shape[0:2]
            self._output_frame = img.copy()
