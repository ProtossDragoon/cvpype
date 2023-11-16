from typing import Any
from src.core.types.line import LinesType


class OpenCVLinesType(LinesType):
    def __init__(self, data: Any):
        super().__init__(data)
