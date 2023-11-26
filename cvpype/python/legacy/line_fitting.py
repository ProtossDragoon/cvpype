import csv
import logging
import os

import cv2
import numpy as np

from cvpype.python.utils import loggerutil
from legacy.intersection_tracking \
    import get_line_center_between_edge_pipeline

# loggerutil.set_basic_config(logging.DEBUG)
logger = logging.getLogger(__name__)


def single_image_pipeline(
    color_image: cv2.Mat,
    save_component_output: bool = False,
    component_output_save_dir: os.PathLike = ''
) -> cv2.Mat:
    """입력 영상을 입력받아 차량을 중심으로 좌우 차선이 그려진 영상을 반환합니다.
    차선이 검출되지 않으면 원본 영상을 반환합니다.
    내부적으로는 다음과 같이 동작합니다.
    1. 영상을 읽어와 그레이스케일 영상으로 변환합니다.
    2. 차선이 나타나지 않는 영상의 상단 절반을 잘라냅니다.
    3. 아랫쪽 절반 영상에 케니 검출기를 적용합니다.
    4. 허프 변환을 적용하여 직선의 파라미터들을 추출합니다.
    5. 직선의 각도가 일정 범위를 벗어난다고 판단되면
       인접한 차선이 아니라고 판단하여 제거합니다.
    6. 앞서 잘라내 두었던 상단의 절반 영상을 병합합니다.
    7. 영상에 붉은색 직선을 y=400을 그립니다.
    8. 차선 후보들 중 y=400과의 교점을 구합니다.

    Args:
        save_output (bool): 이 옵션이 켜져 있다면
            파이프라인을 구성하는 각 컴포넌트들의 중간처리 결과물을
            지정된 `component_output_save_dir`에 저장합니다.
            파일의 이름은 자동으로 `{원본 영상의 이름}_{파이프라인 순서}.{확장자}`
            의 형태로 저장됩니다.

    Returns:
        cv2.Mat: 차선 두 개와 붉은색 y=400 직선이 그려진 이미지
    """
    # Check if the output directory exists, if not create it
    if save_component_output:
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

    # Read the image
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    logger.debug("Image converted to grayscale")
    if save_component_output:
        cv2.imwrite(os.path.join(
            component_output_save_dir, "1_gray.png"), gray_image)

    # Step 2: Crop the top half of the image
    height = gray_image.shape[0]
    crop_image = gray_image[int(height/2):, :]
    if save_component_output:
        cv2.imwrite(os.path.join(component_output_save_dir,
                    "2_cropped.png"), crop_image)

    # Step: Bilateral Gaussian filtering
    logger.debug("Applying Bilateral Gaussian blurring.")
    hparam_sigma_space = 10 # 의미: 가우시안 필터의 블러링 강도
    hparam_sigma_color = 10 # 의미: 주변과 색상값 차이가 얼마나 커야 에지라고 볼 것인가
    crop_image = cv2.bilateralFilter(crop_image, -1,
                                     hparam_sigma_color,
                                     hparam_sigma_space)

    if save_component_output:
        cv2.imwrite(os.path.join(component_output_save_dir,
                    "2_1_blurred_output.png"), crop_image)

    # Step 3: Apply Canny edge detection
    # 공통 의미: 낮아지면 느슨하게, 높아지면 까다롭게 에지 선별.
    threshold_low = 100 # 의미: 에지 후보를 만드는 기준선. 이론: 약한 에지를 판단하는 기준
    threshold_high = 200 # 의미: 에지 확정에 대한 기준선. 이론: 강한 에지를 판단하는 기준
    edge_image = cv2.Canny(crop_image, threshold_low, threshold_high)
    if save_component_output:
        cv2.imwrite(os.path.join(component_output_save_dir,
                    "3_edges.png"), edge_image)

    # FIXME
    # Call the get_line_center_between_edge_pipeline function for each half
    _x_index_center = edge_image.shape[1] // 2
    _x_index_occulded = 280
    _occulded_thick = _x_index_center - _x_index_occulded

    left_edge_image = edge_image[:, :_x_index_center-_occulded_thick]
    right_edge_image = edge_image[:, _x_index_center+_occulded_thick:]
    left_nan = 0
    left_lane_center = get_line_center_between_edge_pipeline(
        color_image[int(height/2):, :_x_index_occulded],
        left_edge_image,
        5, 60, 400-int(height/2),
        save_component_output,
        component_output_save_dir,
        nan = left_nan
    )
    right_nan = 640
    right_lane_center = get_line_center_between_edge_pipeline(
        color_image[int(height/2):, _x_index_center+_occulded_thick:],
        right_edge_image,
        5, 60, 400-int(height/2),
        save_component_output,
        component_output_save_dir,
        nan = right_nan,
    )

    # Adjust the right lane center if it's not 'nan'
    if right_lane_center != right_nan:
        # Adjust the right lane center since the image was divided
        right_lane_center += (_x_index_center+_occulded_thick)

    # FIXME
    csv_filename = os.path.join(".", "lane_centers.csv")
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([left_lane_center, right_lane_center])

    # Step 4: Apply Hough transform to find lines
    lines = cv2.HoughLinesP(edge_image, 1, np.pi / 180,
                            threshold=100, minLineLength=10, maxLineGap=250)
    if lines is None or len(lines) == 0:
        logger.warning(f"No candidate lines detected for the image.")
        cv2.putText(color_image, "No candidate lines detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return color_image

    if lines is not None:
        logger.debug(f"{len(lines)} lines detected by Hough Transform")
        if save_component_output:
            # Visualize lines on a separate image for saving
            lines_visualization = cv2.cvtColor(edge_image, cv2.COLOR_GRAY2BGR)
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(lines_visualization, (x1, y1),
                             (x2, y2), (0, 255, 0), 2)
            cv2.imwrite(os.path.join(component_output_save_dir,
                        "4_lines.png"), lines_visualization)

    # Step 5: Filter out irrelevant lines based on angle
    filtered_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
            if 30 <= abs(angle) <= 150:
                filtered_lines.append(line)
    logger.debug(f"{len(filtered_lines)} lines remained after filtering")

    if save_component_output:
        filtered_lines_visualization = cv2.cvtColor(edge_image, cv2.COLOR_GRAY2BGR)
        for line in filtered_lines:
            for x1, y1, x2, y2 in line:
                cv2.line(filtered_lines_visualization,
                         (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.imwrite(os.path.join(component_output_save_dir,
                    "5_filtered_lines.png"), filtered_lines_visualization)

    # Step 6: Merge with the top half of the original image
    top_half = color_image[:int(height/2), :]
    bottom_half_with_lines = cv2.cvtColor(edge_image, cv2.COLOR_GRAY2BGR)
    for line in filtered_lines:
        for x1, y1, x2, y2 in line:
            cv2.line(bottom_half_with_lines, (x1, y1),
                     (x2, y2), (0, 255, 0), 1)
    merged_image = np.concatenate((top_half, bottom_half_with_lines), axis=0)

    # Step 7: Draw a red horizontal line at y=400
    cv2.line(merged_image, (0, 400),
             (merged_image.shape[1], 400), (0, 0, 255), 2)

    # Visualize the lane centers on the merged_image
    for center, label in zip([left_lane_center, right_lane_center], ['L', 'R']):
        # Draw the 'x' marker
        cv2.drawMarker(merged_image,
                        (center, 400), (0, 0, 255),
                        markerType=cv2.MARKER_CROSS,
                        markerSize=10, thickness=2)
        # Annotate the coordinate
        cv2.putText(merged_image, f"{label}: ({center}, {400})",
                    (center - 30, 400 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    return merged_image
