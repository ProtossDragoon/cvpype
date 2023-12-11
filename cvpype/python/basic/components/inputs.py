# Built-in
from typing import Any

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.core.types.any import AnyType

# Project-Components
from cvpype.python.core.components.base import BaseComponent


class InputsComponent(BaseComponent):
    """The component in a pipeline that checks if the arguments passed into
    the pipeline are of type `ComponentIOSpec`.

    If they are not, it wraps them in `ComponentIOSpec` so that
    they can flow through the pipeline. This class is designed
    to be executed only once at the beginning of the pipeline.
    It serves a similar role to Keras' `input` layer.
    """
    def __init__(
        self,
        visualizer = None
    ):
        super().__init__(visualizer)
        self.outputs = []

    def __call__(
        self,
        *args: Any,
        **kwargs
    ):
        if not self.outputs: # NOTE: run once
            self._init_output(args)
        for arg, output in zip(args, self.outputs):
            if isinstance(arg, ComponentIOSpec):
                output.data_container.data = arg.data_container.data
            else:
                output.data_container.data = arg
        if len(self.outputs) > 1:
            return self.outputs
        return self.outputs[0]

    def _init_output(
        self,
        args
    ):
        l = len(args)
        self.outputs = [
            ComponentIOSpec(
                f'auto_{i}',
                AnyType(),
            ) for i in range(l)
        ]
