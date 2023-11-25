# Built-in
import logging
from typing import Any

# Project
from src.core.types.input import InputType
from src.core.iospec import ComponentIOSpec


class InputsComponent():
    def __call__(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        wrapped_args = []
        for arg in args:
            if isinstance(arg, ComponentIOSpec):
                wrapped_args.append(arg)
            else:
                iospec = ComponentIOSpec(
                    name='input',
                    data_container=InputType(),
                    allow_copy=True,
                    allow_change=True,
                )
                iospec.data_container.data = arg
                wrapped_args.append(iospec)
        if len(wrapped_args) == 1:
            wrapped_args = wrapped_args[0]
        return wrapped_args
