# Built-in
import time
from threading import Lock

# Third party
import cv2

# Project
from cvpype.python.backend.web.streamer.base import BaseWebStreamer


class RealtimeImageWebStreamer(BaseWebStreamer):
    def __init__(
        self,
        width: int | None = None,
        height: int | None = None,
    ):
        super().__init__(width=width, height=height)
        self.temp_frame = None
        self.temp_frame_lock = Lock()

    def read_from_stream(self):
        # FIXME: dirty api, not safe
        while True:
            time.sleep(0.05)
            with self.temp_frame_lock:
                self.output_frame = self.temp_frame

    def __call__(self, frame):
        # FIXME: dirty api
        with self.temp_frame_lock:
            self.temp_frame = frame

    def push_to_browser(self):
        while True:
            # TODO: Should be benchmarked in the parent classes
            if self.output_frame is not None:
                (ok, encoded_frame) = cv2.imencode(
                    ext=".jpg",
                    img=self.output_frame
                )
                if not ok:
                    continue
                yield(
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encoded_frame) + b'\r\n'
                )

    def close(
        self
    ):
        pass
