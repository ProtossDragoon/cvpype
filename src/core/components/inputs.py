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
        for i, arg in enumerate(args):
            assert not isinstance(arg, ComponentIOSpec), (
                'Input component cannot be used '
                'over `ComponentIOSpec` input.'
            )
            iospec = ComponentIOSpec(
                name='input',
                data_container=InputType(),
                allow_copy=True,
                allow_change=True,
            )
            iospec.data_container.data = arg
            wrapped_args.append(iospec)
        return wrapped_args
