from typing import Any


class BaseType:
    def __init__(
        self,
    ):
        self.data = None

    def to_file(
        self,
        path: str
    ):
        raise NotImplementedError("Must be implemented by a subclass.")
