import logging
import os

import cv2

from src.utils import loggerutil
from src.application.line_fitting import single_image_pipeline

loggerutil.set_basic_config(logging.INFO)
logger = logging.getLogger(__name__)


def run_pipeline(
    video_path: os.PathLike,
    playback_speed: float = 1.0,
) -> None:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        logger.error(f"Cannot open video at path {video_path}")
        raise FileNotFoundError(f"Cannot open video at path {video_path}")
    logger.info(f"Video loaded from {video_path}")

    # Determine the delay
    # based on the original video's FPS
    # and the playback speed
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int((1.0 / fps) * 1000 / playback_speed)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Raw', frame)

        processed_frame = single_image_pipeline(frame)
        cv2.imshow('Processed', processed_frame)

        # Press 'q' to quit
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path = os.path.join('data', 'project.avi')
    playback_speed = 2.0
    run_pipeline(video_path, playback_speed)
