# Built-in
import time

# Third party
import cv2
import imutils
from imutils.video import VideoStream

# Project
from cvpype.python.backend.web.streamer.base import BaseWebStreamer


class CameraWebStreamer(BaseWebStreamer):
    def __init__(
        self,
        width: int | None = None,
        height: int | None = None,
        src: int = 0,
    ):
        super().__init__(width=width, height=height)
        self.video_stream = VideoStream(src=src).start()
        time.sleep(3.0)

    def read_from_stream(self):
        while True:
            # TODO: Should be benchmarked in the parent classes
            # NOTE: 이 연산들은 매우 무거운 편임.
            # 여기가 더 무거워지면, push_to_browser 이 아무리 빨라도
            # 화면을 제대로 출력하지 못하는 문제가 발생함.
            frame = self.video_stream.read()
            frame = imutils.resize(frame, width=self.width, height=self.height)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.output_frame = frame_gray

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
        self.video_stream.stop()
