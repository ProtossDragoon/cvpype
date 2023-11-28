# Project-Components
from cvpype.python.core.components.inputs import InputsComponent
from cvpype.python.applications.components.intersectionfinding import IntersectionFindingComponent
from cvpype.python.applications.components.intersectionfiltering import (
    WidthBasedIntersectionFilteringComponent,
    ColorBasedIntersectionFilteringComponent
)


# FIXME: Pipeline 클래스로 래핑
def get_intersection_finding_pipeline(
    roi_y: int,
    width_min: int,
    width_max: int,
):
    """에지 정보를 가진 영상과 y=`k`의 교점의 좌표를 바탕으로
    두께가 `width_min` 이상이고 `width_max` 이하인 검은선을 찾아
    선의 중심 x좌표를 반환합니다. 내 위치를 기준으로 좌, 우 차선을 찾습니다.
    선을 찾지 못했다면 아무것도 반환하지 않습니다.

    선을 찾는 작동원리는 다음과 같습니다.
    예를 들어 y=k 에서 에지 영상이 아래와 같이 나타난다면,
        [ 0, 0, 255, 0, 255, 0, 0, 255, 0, 0]
    1. 에지 쌍을 만들며 선 간격의 경우의 수를 모두 리스트업합니다.
        경우의수1: s_idx = 2, e_idx = 4, width = 2
        경우의수2: s_idx = 2, e_idx = 7, width = 5
        경우의수3: s_idx = 4, e_idx = 7, width = 3
        만약 에지가 1개 이하로 존재한다면 아무것도 반환하지 않습니다.
    2. 선 간격이 width_min 이상, width_max 인 것들만을 가져옵니다.
        만약 `width_min=3`, `width_max=5` 이라면
        경우의수2, 경우의수3을 제외하고 나머지는 버립니다.
        남은 경우의 수가 없다면 아무것도 반환하지 않습니다.
    3. 선의 색상은 검정색임을 가정했으므로, 다양한 광학적 조건 속에서
        검정색의 기준을 찾아내기 위해 컬러 영상에서 y=k 영역을 추출한 후
        히스토그램 분석을 이용합니다.
    4. 찾아낸 검정색의 기준을 이용해 남아 있는 경우의 수에서
        선의 내부라고 할 수 있는 영역들에 검정색 성분이
        일정수준(90%)이상 채워져 있는지 확인하고,
        채워져 있지 않는 경우의 수를 버립니다.
    5. 각 차선마다 남아 있는 경우의 수가 1개라면 s_idx와 e_idx의 평균을 내어 리턴하고
        남아 있는 경우의 수가 2개 이상이라면 남아 있는 모든 경우의 수의
        s_idx와 e_idx를 더해 평균을 내어 리턴합니다.

    Returns:
        list[tuple[int, int]]: y=k 의 교점 좌표 0~2개
    """
    inputs = InputsComponent()
    intersection_finding = IntersectionFindingComponent(
        y=roi_y
    )
    width_based_filtering = WidthBasedIntersectionFilteringComponent(
        width_min=width_min,
        width_max=width_max
    )
    color_based_filtering = ColorBasedIntersectionFilteringComponent(
        y=roi_y
    )

    def fn(color_image, edge_image):
        color_image, edge_image = inputs(color_image, edge_image)
        intersections = intersection_finding(edge_image)
        intersections = width_based_filtering(intersections)
        # intersections = color_based_filtering(color_image, intersections)
        return intersections

    return fn
