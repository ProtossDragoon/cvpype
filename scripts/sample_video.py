import os
import argparse
import logging

import cv2


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


def sample_video(
    n: int,
    video_path: os.PathLike,
    save_dir: os.PathLike,
):
    """비디오를 불러와 n개의 프레임을 등간격 샘플링합니다.
    샘플링 결과물은 `save_dir/{n}` 디렉토리에 {i}.png 형태로 저장됩니다.

    Args:
        n (int): 샘플 갯수
        video_path (os.PathLike): 비디오의 경로
        save_dir (os.PathLike, optional): 디렉토리 `n`을 생성할 경로
    """
    # Check if the video file exists
    if not os.path.exists(video_path):
        logging.error(f"Video file not found: {video_path}")
        return

    # Determine the directory to save the images
    save_subdir = os.path.join(save_dir, str(n))

    # Check if the save_subdir already exists and contains the same number of files as n
    if os.path.exists(save_subdir):
        existing_files = os.listdir(save_subdir)
        if len(existing_files) == n:
            raise Exception(f"The directory '{save_subdir}' already exists "
                             "and contains the same number of files as 'n'. "
                             "Aborting to prevent overwriting data.")

    os.makedirs(save_subdir, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_count < n:
        raise ValueError("Number of frames to sample is greater than"
                         " the total number of frames in the video.")

    # Calculate frame sampling interval
    frame_interval = frame_count // n

    logger.info(f"Total frames in the video: {frame_count}")
    logger.info(f"Frame sampling interval: {frame_interval}")

    # Initialize variables
    frame_number = 0
    sample_number = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break  # End of video

        if frame_number % frame_interval == 0:
            # Save the sampled frame as an image
            save_path = os.path.join(save_subdir, f"{sample_number}.png")
            cv2.imwrite(save_path, frame)
            sample_number += 1

        frame_number += 1

        if sample_number >= n:
            break  # Reached the desired number of samples

    # Release the video capture object
    cap.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sample frames from a video.")
    parser.add_argument("n", type=int, help="Number of frames to sample")
    parser.add_argument("video_path", type=str, help="Path to the video file")
    parser.add_argument("--save_dir", type=str, help="Directory to save sampled images")

    args = parser.parse_args()
    sample_video(args.n, args.video_path, args.save_dir)
