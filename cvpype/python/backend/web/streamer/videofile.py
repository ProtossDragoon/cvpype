# Built-in
import time

# Third party
import cv2
import imutils

# Project
from cvpype.python.backend.web.streamer.base import BaseWebStreamer


class VideofileWebStreamer(BaseWebStreamer):
    def __init__(
        self,
        video_path: str,
        width: int | None = None,
        height: int | None = None,
        playback_speed: float = 1.0,
        replay: bool = True
    ):
        super().__init__(width=width, height=height)
        self.video_path = video_path
        self.cap = cv2.VideoCapture(str(self.video_path))
        if not self.cap.isOpened():
            self.logger.error(f"Cannot open video at path {self.video_path}")
            raise FileNotFoundError(f"Cannot open video at path {self.video_path}")
        self.logger.info(f"Video loaded from {self.video_path}")
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.delay = int((1.0 / self.fps) * 1000 / playback_speed)
        self.replay = replay

    def read_from_stream(self):
        while self.cap.isOpened():
            # TODO: Should be benchmarked in the parent classes
            # NOTE: 이 연산들은 매우 무거운 편임.
            # 여기가 더 무거워지면, push_to_browser 이 아무리 빨라도
            # 화면을 제대로 출력하지 못하는 문제가 발생함.
            ret, frame = self.cap.read()
            if not ret:
                if self.replay:
                    self.logger.info(f'Replay video `{self.video_path}`')
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                break
            frame = imutils.resize(frame, width=self.width, height=self.height)
            self.output_frame = frame
            try:
                cv2.waitKey(self.delay)
            except:
                # FIXME: dirty
                # NOTE: https://github.com/opencv/opencv/issues/22602
                time.sleep(self.delay)
        self.logger.warning('Broken pipe')

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
        self.cap.release()
