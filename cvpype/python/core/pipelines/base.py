# Built-in
import time
import logging
from abc import ABC, abstractmethod
from typing import Union, Dict

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Visualizers
from cvpype.python.core.visualizer.base import BaseVisualizer

# Project-Components
from cvpype.python.core.components.base import (
    BaseComponent,
    InputsOnlyBaseComponent,
    IOBaseComponent
)

# Project-Streamers
from cvpype.python.backend.web.streamer.base import BaseStreamer


class BasePipeline(ABC):
    def __init__(
        self,
    ) -> None:
        self.components: Dict[str, BaseComponent]
        self.visualizers: Dict[str, BaseVisualizer]
        self.logger = logging.getLogger(self.__class__.__name__)

    def _unpack_components(
        self
    ) -> Dict[str, BaseComponent]:
        _pipelines: Dict[str, BasePipeline] = {}
        _components: Dict[str, BaseComponent] = {}
        for attr_name, attr_value in self.__dict__.items():
            if isinstance(attr_value, BasePipeline):
                self.logger.debug(f'Pipeline detected (self.{attr_name})')
                _pipelines[attr_name] = attr_value
            if isinstance(attr_value, BaseComponent):
                self.logger.debug(f'Component detected (self.{attr_name})')
                _components[attr_name] = attr_value
        for _, pipeline in _pipelines.items():
            _components.update(pipeline._unpack_components())
        return _components

    def _unpack_iospecs(
        self
    ):
        iospec_ids = []
        for _, component in self.components.items():
            if isinstance(component, IOBaseComponent):
                for output in component.outputs:
                    assert id(output) not in iospec_ids, (
                        'Cannot use duplicated component '
                        f'`{component.__class__.__name__}` for multicore processing.'
                        'This restriction will be removed in the future.'
                    )
                    iospec_ids.append(id(output))
            if isinstance(component, (InputsOnlyBaseComponent, IOBaseComponent)):
                for iospec in component.inputs:
                    assert id(iospec) not in iospec_ids, (
                        'Cannot use duplicated component '
                        f'`{component.__class__.__name__}` for multicore processing.'
                        'This restriction will be removed in the future.'
                    )
                    iospec_ids.append(id(iospec))
        # TODO

    def _unpack_visualizers(
        self
    ):
        _visualizers: Dict[str, BaseVisualizer] = {}
        for _, component in self.components.items():
            if component.visualizer is not None:
                name = component.visualizer.name
                self.logger.debug(f'Visualizer detected ({name})')
                # FIXME: Duplicated visualizer name should be accepted.
                assert _visualizers.get(name, None) is None, (
                    f'Duplicated visualizer name. `{name}`'
                )
                _visualizers[name] = component.visualizer
        return _visualizers

    def autocreate_graph(
        self
    ):
        self.components = self._unpack_components()
        self.visualizers = self._unpack_visualizers()
        self._unpack_iospecs()

    @abstractmethod
    def run(
        self,
        *args,
    ) -> Union[ComponentIOSpec, list[ComponentIOSpec]]:
        raise NotImplementedError

    def run_from_streamer(
        self,
        streamer: BaseStreamer
    ):
        # FIXME: dirty api
        streamer.open()
        while not streamer.is_ready:
            self.logger.info(
                'Waiting for the stream is ready ...'
            )
            time.sleep(0.5)
        def fn():
            while True:
                self.run(streamer.output_frame.copy())
        return fn
