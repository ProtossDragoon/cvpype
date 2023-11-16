from typing import Any


class BaseType:
    def __init__(
        self,
        data: Any,
    ):
        self.data = data

    def to_file(
        self,
        path: str
    ):
        raise NotImplementedError("Must be implemented by a subclass.")
