import logging
import os

import cv2
import numpy as np
import matplotlib.pyplot as plt

# loggerutil.set_basic_config(logging.DEBUG)
logger = logging.getLogger(__name__)


def get_line_center_between_edge_pipeline(
    color_image: cv2.Mat,  # NOTE: ReadOnly
    edge_image: cv2.Mat,  # NOTE: ReadOnly
    width_min: int,
    width_max: int,
    k: int,
    save_component_output: bool = False,
    component_output_save_dir: os.PathLike = '',
    nan: int = -1,
) -> int:
    """에지 정보를 가진 영상과 y=`k`의 교점의 좌표를 바탕으로
    두께가 `width_min` 이상이고 `width_max` 이하인 검은선을 찾아
    선의 중심 x좌표를 반환합니다. 선을 찾지 못했다면 `nan` 값을 반환합니다.

    선을 찾는 작동원리는 다음과 같습니다.
    예를 들어 y=k 에서 에지 영상이 아래와 같이 나타난다면,
        [ 0, 0, 255, 0, 255, 0, 0, 255, 0, 0]
    1. 에지 쌍을 만들며 선 간격의 경우의 수를 모두 리스트업합니다.
       경우의수1: s_idx = 2, e_idx = 4, width = 2
       경우의수2: s_idx = 2, e_idx = 7, width = 5
       경우의수3: s_idx = 4, e_idx = 7, width = 3
       만약 에지가 1개 이하로 존재한다면 `nan`값을 반환합니다.
    2. 선 간격이 width_min 이상, width_max 인 것들만을 가져옵니다.
       만약 `width_min=3`, `width_max=5` 이라면
       경우의수2, 경우의수3을 제외하고 나머지는 버립니다.
       남은 경우의 수가 없다면 `nan`값을 반환합니다.
    3. 선의 색상은 검정색임을 가정했으므로, 다양한 광학적 조건 속에서
       검정색의 기준을 찾아내기 위해 컬러 영상에서 y=k 영역을 추출한 후
       히스토그램 분석을 이용합니다.
    4. 찾아낸 검정색의 기준을 이용해 남아 있는 경우의 수에서
       선의 내부라고 할 수 있는 영역들에 검정색 성분이
       일정수준(90%)이상 채워져 있는지 확인하고,
       채워져 있지 않는 경우의 수를 버립니다.
    5. 남아 있는 경우의 수가 1개라면 s_idx와 e_idx의 평균을 내어 리턴하고
       남아 있는 경우의 수가 2개 이상이라면 남아 있는 모든 경우의 수의
       s_idx와 e_idx를 더해 평균을 내어 리턴합니다.

    Args:
        color_image (cv2.Mat): 원본 영상
        edge_image (cv2.Mat): 에지 영상
        save_output (bool): 이 옵션이 켜져 있다면
            파이프라인을 구성하는 각 컴포넌트들의 중간처리 결과물을
            지정된 `component_output_save_dir`에 저장합니다.
            파일의 이름은 자동으로 `{원본 영상의 이름}_{파이프라인 순서}.{확장자}`
            의 형태로 저장됩니다.

    Returns:
        list[int, int]: y=k 의 교점 좌표
    """
    if save_component_output:
        # Assert for component_output_save_dir
        assert component_output_save_dir, (
            "`component_output_save_dir` should not be empty"
            f"if `save_component_output` is {save_component_output}")
        if not os.path.exists(component_output_save_dir):
            os.makedirs(component_output_save_dir)
            logger.info(
                f"Created output directory at {component_output_save_dir}")
        else:
            logger.info(
                f"Output directory already exists at {component_output_save_dir}")

    if save_component_output:
        # Save the color_image
        cv2.imwrite(os.path.join(component_output_save_dir,
                    f"color_image_{nan}.png"), color_image)
        # Save the edge_image
        cv2.imwrite(os.path.join(component_output_save_dir,
                    f"edge_image_{nan}.png"), edge_image)

    edge_row = edge_image[k]

    # Get starting and ending indices of edges
    edge_indices = np.where(edge_row == 255)[0]

    if len(edge_indices) <= 1:
        return nan

    # Create pairs of edges
    edge_pairs = [(edge_indices[i], edge_indices[i+1])
                  for i in range(len(edge_indices)-1)]

    if save_component_output:
        # Compute the lengths for each pair in edge_pairs
        edge_lengths = [e - s for s, e in edge_pairs]

        # Plot the histogram
        plt.figure(figsize=(8, 6))
        plt.hist(edge_lengths, bins=range(0, max(edge_lengths) + 3, 3))
        plt.title("Histogram of Edge Pair Lengths")
        plt.xlabel("Length")
        plt.ylabel("Frequency")

        # Save the histogram to the specified directory
        histogram_path = os.path.join(
            component_output_save_dir, "edge_lengths_histogram.png")
        plt.savefig(histogram_path)
        logger.info(f"Saved histogram of edge lengths to {histogram_path}")

    # Filter pairs based on width_min and width_max
    valid_pairs = [(start, end) for start,
                   end in edge_pairs if width_min <= end - start <= width_max]

    if not valid_pairs:
        return nan

    # Analyze color histogram to determine black color
    color_row = color_image[k]

    BIN_COUNT = 256
    hist_r = cv2.calcHist([color_image], [0], None, [BIN_COUNT], [0, 256])
    hist_g = cv2.calcHist([color_image], [1], None, [BIN_COUNT], [0, 256])
    hist_b = cv2.calcHist([color_image], [2], None, [BIN_COUNT], [0, 256])

    # TODO
    # Histogram stretching
    # Determine the bins that have more than `width_min` pixels
    # Find the min and max values for valid bins only
    # Apply histogram stretching on the valid range
    # Rest of the process remains the same

    # Save histogram if save_component_output is True
    if save_component_output:
        # Save histogram plot
        plt.bar(np.arange(BIN_COUNT), hist_r.ravel(), alpha=0.6)
        plt.bar(np.arange(BIN_COUNT), hist_g.ravel(), alpha=0.6)
        plt.bar(np.arange(BIN_COUNT), hist_b.ravel(), alpha=0.6)
        plt.title("Color Histogram for y=k")
        plt.xlabel("Bins")
        plt.ylabel("Frequency")
        histogram_path = os.path.join(
            component_output_save_dir, f"color_histogram_{nan}.png")
        plt.savefig(histogram_path)
        plt.show() # FIXME: TEMP
        plt.close()
        logger.info(f"Saved histogram plot at {histogram_path}.")

    # Log histogram computation
    logger.debug(f"Computed color histogram for row y={k}.")

    # Select threshold actively. We'll find two peaks inside the remaining part.
    # Peaks can be found where there's a change
    # from increasing to decreasing in histogram values.
    # Find the bin with the maximum frequency
    # which is likely to represent black
    black_threshold = 170 # FIXME: manual

    # Log the calculated black threshold
    logger.info(f"Calculated black threshold: {black_threshold}.")

    # Check if the region inside the edge pair has black color
    valid_black_pairs = []
    for start, end in valid_pairs:
        line_section = np.sum(color_row[start:end], axis=-1) // 3 # FIXME
        black_pixels = len(np.where(line_section < black_threshold)[0])

        if black_pixels / len(line_section) >= 0.9:
            valid_black_pairs.append((start, end))

    if not valid_black_pairs:
        return nan

    # Calculate average center
    center = np.mean([(start + end) // 2 for start,
                     end in valid_black_pairs]).astype(int)

    return center
