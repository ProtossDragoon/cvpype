from src.core.types.base import BaseType


class ComponentIOSpec:
    def __init__(
        self,
        name: str,
        data_type,
        allow_copy: bool,
        allow_change: bool,
    ) -> None:
        assert type(name) is str
        assert isinstance(data_type, BaseType)
        assert type(allow_copy) is bool
        assert type(allow_change) is bool
        self.name = name
        self.data_type = data_type
        self.allow_copy = allow_copy
        self.allow_change = allow_change

        self.data = None
