# Built-in
import logging
from abc import ABC, abstractmethod
from typing import Union

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Components
from cvpype.python.core.components.base import (
    BaseComponent,
    InputsOnlyBaseComponent,
    IOBaseComponent
)


class BasePipeline(ABC):
    def __init__(
        self,
    ) -> None:
        self.components = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def autocreate_graph(
        self
    ):
        self.components = {}
        iospec_ids = []
        for attr_name, attr_value in self.__dict__.items():
            if isinstance(attr_value, BaseComponent):
                self.logger.debug(f'Component detected (self.{attr_name})')
                self.components[attr_name] = attr_value
        for _, component in self.components.items():
            if isinstance(component, (InputsOnlyBaseComponent, IOBaseComponent)):
                for iospec in component.inputs:
                    assert id(iospec) not in iospec_ids, (
                        'Cannot use duplicated component '
                        f'`{attr_value.__class__.__name__}` for multicore processing.'
                        'This restriction will be removed in the future.'
                    )
                    iospec_ids.append(id(iospec))
                for output in component.outputs:
                    assert id(output) not in iospec_ids, (
                        'Cannot use duplicated component '
                        f'`{attr_value.__class__.__name__}` for multicore processing.'
                        'This restriction will be removed in the future.'
                    )
                    iospec_ids.append(id(output))
        # TODO

    @abstractmethod
    def run(
        self
    ) -> Union[ComponentIOSpec, list[ComponentIOSpec]]:
        raise NotImplementedError
