import logging
import os

import cv2

from src.utils import loggerutil
from src.application.line_fitting import single_image_pipeline

loggerutil.set_basic_config(logging.INFO)
logger = logging.getLogger(__name__)


def run_pipeline(
    image_path: os.PathLike,
    component_output_save_dir: os.PathLike
) -> None:
    original_image = cv2.imread(str(image_path))
    if original_image is None:
        logger.error(f"No image found at path {image_path}")
        raise FileNotFoundError(f"No image found at path {image_path}")
    logger.info(f"Image loaded from {image_path}")

    processed_img = single_image_pipeline(
        original_image,
        save_component_output=True,
        component_output_save_dir=component_output_save_dir
    )
    cv2.imshow('Processed Image', processed_img)
    cv2.waitKey(0)


if __name__ == '__main__':
    for i in range(20):
        image_path = os.path.join('data', 'sampled', '20', f'{i}.png')
        save_dir = os.path.join('data', 'output', '20', f'{i}')
        run_pipeline(image_path, save_dir)
    cv2.destroyAllWindows()
