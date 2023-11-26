# Built-in
import os
import logging
import argparse

# Third party
import cv2

# Project
from cvpype.python.utils import loggerutil

# Project-Pipelines
from cvpype.python.applications.pipelines.line_tracking import get_line_tracking_pipeline


loggerutil.set_basic_config(logging.INFO)
logger = logging.getLogger(__name__)


def run_pipeline(
    image_path: os.PathLike,
) -> None:
    pipe = get_line_tracking_pipeline(
        crop_y=300,
        roi_y=400,
        image_h=480
    )
    image = cv2.imread(str(image_path))
    if image is None:
        logger.error(f"Cannot open image at path {image_path}")
        raise FileNotFoundError(f"Cannot open image at path {image_path}")
    logger.info(f"Image loaded from {image_path}")

    pipe(image)
    cv2.waitKey(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run pipeline on an image.')
    parser.add_argument('image_path', type=str, help='Path to the image file.')
    args = parser.parse_args()
    run_pipeline(args.image_path)
