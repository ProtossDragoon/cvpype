from cvpype.python.core.types.base import BaseType


class ComponentIOSpec:
    def __init__(
        self,
        name: str,
        data_container: BaseType,
        allow_copy: bool = True,
        allow_change: bool = True,
    ) -> None:
        assert type(name) is str
        assert isinstance(data_container, BaseType)
        assert type(allow_copy) is bool
        assert type(allow_change) is bool
        self.name = name
        self.data_container = data_container
        self.allow_copy = allow_copy
        self.allow_change = allow_change
