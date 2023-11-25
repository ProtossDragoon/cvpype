# Built-in
import logging
from abc import ABC, abstractmethod

# Project
from src.core.iospec import ComponentIOSpec

# Configure the root logger
logging.basicConfig(level=logging.INFO)


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
        self.logger = logging.getLogger(self.__class__.__name__)
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
