# Built-in
import os
import logging
import argparse

# Third party
import cv2

# Project
from src.utils import loggerutil

# Project-Pipelines
from src.applications.pipelines.line_tracking import get_line_tracking_pipeline


loggerutil.set_basic_config(logging.INFO)
logger = logging.getLogger(__name__)


def run_pipeline(
    video_path: os.PathLike,
    playback_speed: float = 1.0,
) -> None:
    pipe = get_line_tracking_pipeline(
        crop_y=300,
        roi_y=400,
        image_h=480
    )
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        logger.error(f"Cannot open video at path {video_path}")
        raise FileNotFoundError(f"Cannot open video at path {video_path}")
    logger.info(f"Video loaded from {video_path}")

    # Determine the delay based on
    # the original video's FPS and the playback speed
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int((1.0 / fps) * 1000 / playback_speed)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        pipe(frame)
        cv2.waitKey(delay)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run pipeline on a video.')
    parser.add_argument('video_path', type=str, help='Path to the video file.')
    args = parser.parse_args()
    run_pipeline(args.video_path)

