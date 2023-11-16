# Built-in
import logging
from abc import ABC, abstractmethod

# Projects
from src.core.visualizer.base import BaseVisualizer
from src.core.iospec import ComponentIOSpec


# Configure the root logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Base Component class
class BaseComponent(ABC):
    name: str
    inputs: list[ComponentIOSpec]
    outputs: list[ComponentIOSpec]
    visualizer: BaseVisualizer

    def __init__(
        self,
        do_logging = True
    ):
        self.do_logging = do_logging
        self.logger = logging.getLogger(self.__class__.__name__)

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        for input_ in cls.inputs:
            if not isinstance(input_, ComponentIOSpec):
                raise ValueError(
                    f'inputs (class: `{type(input_)}`) is '
                    'not a subclass of `ComponentIOSpec`.'
                )
        for output in cls.outputs:
            if not isinstance(output, ComponentIOSpec):
                raise ValueError(
                    f'outputs (class: `{type(output)}`) is '
                    'not a subclass of `ComponentIOSpec`.'
                )

    @abstractmethod
    def run(self, *args, **kwargs):
        """컴포넌트를 실행합니다.

        `args`는 클래스의 `inputs`리스트에 명시된 스펙의 `data_type`이
        순차적으로 입력될 것을 가정합니다. 반환형은 `outputs`리스트에
        명시된 스펙의 리스트입니다. `kwargs` 파라미터를 통해
        런타임 인자들을 입력받을 수 있습니다.
        """

    def log(self, message: str, level: str = 'info'):
        """Log a message with the given level."""
        if self.do_logging:
            getattr(self.logger, level.lower(), self.logger.info)(message)

    def visualize(self, *args, **kwargs):
        self.visualizer(*args, **kwargs)
