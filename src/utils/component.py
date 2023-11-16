import os

import cv2

from src.core.components.base import BaseComponent
from src.core.types.image import ImageType
from src.applications.types.image import OpenCVGrayscaledImageType


def run_component_with_singular_input_of_ImageType(
    component: BaseComponent,
    video_path: os.PathLike,
    playback_speed: float = 1.0,
    output_path: os.PathLike = '',
    output_specname: str = None,
):
    assert len(component.inputs) == 1
    assert issubclass(
        component.inputs[0].data_type,
        ImageType
    ), (
        f'`{component.inputs[0].data_type.__name__}` is not '
        f'compatible with `{ImageType.__name__}`'
    )
    if output_path:
        if output_specname:
            names = [e.name for e in component.outputs]
            output_idx = names.index(output_specname)
        else:
            assert len(component.outputs)
            output_idx = 0
        assert issubclass(
            component.outputs[output_idx].data_type,
            ImageType
        )

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Cannot open video at path {video_path}")
        raise FileNotFoundError(f"Cannot open video at path {video_path}")
    print(f"Video loaded from {video_path}")

    # Determine the delay
    # based on the original video's FPS
    # and the playback speed
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int((1.0 / fps) * 1000 / playback_speed)

    if output_path:
        # Output video settings
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if issubclass(
            component.inputs[0].data_type,
            OpenCVGrayscaledImageType
        ):
            # NOTE: Every image slices from video
            # has color palette.
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if not ret:
            break
        ret = component.run(frame)
        if output_path:
            im = ret[output_idx]
            assert height == im.shape[0]
            assert width == im.shape[1]
            if issubclass(
                component.outputs[output_idx].data_type,
                OpenCVGrayscaledImageType
            ):
                # NOTE: Cannot convert into a color
                # video with a gray scaled image
                im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
            out.write(im)
    cap.release()
    out.release()
    if output_path:
        print(f"Video saved to {video_path}")
