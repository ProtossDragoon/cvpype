from abc import ABC, abstractmethod

from src.core.iospec import ComponentIOSpec


class BaseVisualizer(ABC):
    inputs: list[ComponentIOSpec]

    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__()
        self.name = name
        self.is_operating = is_operating

    def __call__(
        self,
        *args,
        **kwargs,
    ):
        assert len(self.inputs) == len(args)
        wrapped = []
        for arg, input_type in zip(args, self.inputs):
            input_type.data = arg
            wrapped.append(input_type)
        return self.visualize(*wrapped, **kwargs)

    @abstractmethod
    def visualize(self, *args, **kwargs):
        raise NotImplementedError


class CombinedVisualizer(BaseVisualizer):
    def __init__(
        self,
        name: str,
        is_operating: bool = True
    ) -> None:
        super().__init__(name, is_operating)

    @abstractmethod
    def visualize(self, *args, **kwargs):
        raise NotImplementedError
