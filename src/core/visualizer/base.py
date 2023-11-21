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
        self.__did_runtime_init = False

    def __call__(
        self,
        *args,
        **kwargs,
    ):
        if not self.is_operating:
            return
        if not self.__did_runtime_init:
            self.runtime_init()
            self.__did_runtime_init = True
        assert len(self.inputs) == len(args), f'args: {args} != {self.inputs}'
        wrapped = []
        for arg, input_spec in zip(args, self.inputs):
            input_spec.data_container.data = arg
            wrapped.append(input_spec.data_container)
        self.visualize(*wrapped, **kwargs)

    def runtime_init(self):
        pass

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
