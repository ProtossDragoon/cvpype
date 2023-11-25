# Built-in
import logging
from abc import ABC, abstractmethod
from typing import Any

# Project
from src.core.visualizer.base import BaseVisualizer
from src.core.iospec import ComponentIOSpec
from src.core.types.base import BaseType
from src.core.types.input import InputType
from src.core.types.output import NoOutput

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
        do_logging: bool = True,
        do_typecheck: bool = True,
    ):
        self.do_logging = do_logging
        self.do_typecheck = do_typecheck
        self.logger = logging.getLogger(self.__class__.__name__)

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        for input_ in cls.inputs:
            if not isinstance(input_, ComponentIOSpec):
                raise ValueError(
                    f'inputs (class: `{type(input_)}`) is '
                    'not a subclass of `ComponentIOSpec`.'
                )
        input_names = [e.name for e in cls.inputs]
        assert len(set(input_names)) == len(input_names), (
            'The names of the input spec have to be disticntable. '
            f'Current names: {input_names}'
        )
        for output in cls.outputs:
            if not isinstance(output, ComponentIOSpec):
                raise ValueError(
                    f'outputs (class: `{type(output)}`) is '
                    'not a subclass of `ComponentIOSpec`.'
                )
        output_names = [e.name for e in cls.outputs]
        assert len(set(output_names)) == len(output_names), (
            'The names of the output spec have to be disticntable. '
            f'Current names: {output_names}'
        )

    def __call__(
        self,
        *args: Any,
        **kwargs: Any
    ):
        # input type checking
        assert len(args) == len(self.inputs), (
            f'You defined {len(self.inputs)} inputs '
            f'(types: {[type(e.data_container) for e in self.inputs]}), '
            f'but {len(args)} input(s) ({args}) was given.'
        )

        # unwrapping
        unwrapped_args = []
        for arg, input_ in zip(args, self.inputs):
            assert isinstance(arg, ComponentIOSpec), (
                f'Argument `{arg}` was not wrapped '
                'by class `ComponentIOSpec`'
            )
            arg = arg.data_container
            arg.check_type()
            input_ = input_.data_container
            if isinstance(arg, InputType):
                input_.data = arg.data
                arg = arg.data
            elif isinstance(arg, input_.__class__):
                input_.data = arg.data
                arg = arg.data
            elif isinstance(arg, BaseType):
                raise TypeError(
                    f'Input data type mismatched `{arg.__class__.__name__}`. '
                    f'(Expected `{input_.__class__.__name__}`)'
                )
            unwrapped_args.append(arg)

        # run core method
        rets = self.run(*unwrapped_args, **kwargs)

        # output type checking
        if rets:
            assert type(rets) is dict, (
                'Return value of `run()` method should be dictionary '
                f'that contains keys among {[e.name for e in self.outputs]}, '
                f'but now the type of the return value is {type(rets)}'
            )
            assert len(rets) == len(self.outputs), (
                f'You defined {len(self.outputs)} outputs '
                f'(types: {[e.data_container for e in self.outputs]}), '
                f'but {len(rets)} output(s) was given.'
            )
        else:
            assert len(self.outputs) == 1, (
                "If you don't intend to return any output, "
                'you should not define an output spec. '
                'But currently, the output specs are: '
                f'{[e.data_container for e in self.outputs]}'
            )
            assert isinstance(self.outputs[-1].data_container, NoOutput), (
                "If you don't intend to return any output, "
                'you should not define any output spec other than `NoOutput`. '
                'But currently, the output specs are: '
                f'{[e.data_container for e in self.outputs]}'
            )
            rets = {}

        # wrapping
        wrapped_rets = []
        for name, ret in rets.items():
            output_spec = self.get_output_spec(name)
            output_spec.data_container.data = ret
            output_spec.data_container.check_type()
            wrapped_rets.append(output_spec.data_container)

        if len(self.outputs) == 1:
            return self.outputs[0]
        return self.outputs

    def get_input_spec(
        self,
        name: str,
    ):
        specs = [spec for spec in self.inputs if spec.name == name]
        assert len(specs) == 1, (
            f'There are {len(specs)} inputs with same name.'
        )
        return specs[-1]

    def get_output_spec(
        self,
        name: str,
    ):
        specs = [spec for spec in self.outputs if spec.name == name]
        assert len(specs) == 1, (
            f'There are {len(specs)} outputs with same name.'
        )
        return specs[-1]

    def change_input_type(
        self,
        name: str,
        type_,
    ):
        assert issubclass(type_, BaseType)
        spec = self.get_input_spec(name)
        data = spec.data_container.data
        spec.data_container = type_()
        spec.data_container.data = data

    def change_output_type(
        self,
        name: str,
        type_,
    ):
        assert issubclass(type_, BaseType)
        spec = self.get_output_spec(name)
        data = spec.data_container.data
        spec.data_container = type_()
        spec.data_container.data = data

    @abstractmethod
    def run(self, *args, **kwargs) -> dict:
        raise NotImplementedError

    def log(self, message: str, level: str = 'info'):
        if self.do_logging:
            getattr(self.logger, level.lower(), self.logger.info)(message)

    def visualize(self, *args, **kwargs):
        self.visualizer(*args, **kwargs)
