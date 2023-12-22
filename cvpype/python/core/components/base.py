# Built-in
import logging
from abc import ABC, abstractmethod
from typing import Any

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.core.types.base import BaseType

# Project-Visualizers
from cvpype.python.core.visualizer.base import BaseVisualizer

# Configure the root logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _InputsComponentTool():
    def set_inputs(
        self,
        inputs: list[ComponentIOSpec]
    ):
        """! The `set_inputs` function sets the inputs for a component,
        performing type and value checks.

        @param inputs The `inputs` parameter is
        a list of `ComponentIOSpec` objects.
        """
        if type(inputs) is not list:
            raise TypeError(
                'Type of `inputs` should be list. '
                f'Current value: `{inputs}` (type: {type(inputs)})'
            )
        if len(inputs) == 0:
            raise TypeError('`inputs` should not be empty.')
        for input_ in inputs:
            if not isinstance(input_, ComponentIOSpec):
                raise TypeError(
                    f'inputs (class: `{type(input_)}`) is '
                    'not a subclass of `ComponentIOSpec`.'
                )
        self.inputs = inputs
        self.inputs_name = [i.name for i in self.inputs]
        if len(set(self.inputs_name)) != len(self.inputs):
            raise ValueError(
                f'There are input specs with a same name.'
            )

    def check_args(
        self,
        args: Any,
    ):
        """! The `check_args` function checks if the number and
        types of arguments match the specifications
        provided.

        @param args args is a list of arguments that
        are being passed to a function or method.
        """
        assert len(args) == len(self.inputs), (
            f'You defined {len(self.inputs)} inputs '
            f'(types: {[type(e.data_container) for e in self.inputs]}), '
            f'but {len(args)} input(s) ({args}) was given.'
        )
        for arg, input_ in zip(args, self.inputs):
            assert isinstance(arg, ComponentIOSpec), (
                f'Argument `{arg}` (class: `{type(arg)}`) is '
                'not a subclass of `ComponentIOSpec`.'
            )
            arg.data_container.is_proper_for(input_.data_container)

    def get_input_spec(
        self,
        name: str,
    ):
        """! The function `get_input_spec` returns the input specification
        with the given name, and raises an error if there are multiple
        input specifications with the same name.

        @param name The `name` parameter is a string that represents
        the name of the input specification that you want to retrieve.

        @return the input specification with the given name.
        """
        specs = [spec for spec in self.inputs if spec.name == name]
        if not specs:
            raise ValueError(
                'There are no input specifications with the given name.'
            )
        assert len(specs) == 1, (
            f'There is more than one input with the same name: {len(specs)}.'
        )
        return specs[-1]

    def change_input_type(
        self,
        name: str,
        type_,
    ):
        """! The function `change_input_type` changes the type of a
        data container while preserving the data it contains.

        @param name The `name` parameter is a string that represents the name of the input.
        @param type_ The `type_` parameter in the `change_input_type` method
        is the new type that you want to change the input to.
        It should be a subclass of `BaseType`.
        """
        assert issubclass(type_, BaseType)
        spec = self.get_input_spec(name)
        data = spec.data_container.data
        spec.data_container = type_()
        spec.data_container.data = data

    def move_to_input(
        self,
        srcs: list[ComponentIOSpec]
    ):
        """! The function `move_to_input` copies the data from the `data_container`
        of each argument to the corresponding `data_container` of the `inputs` list.

        @param srcs A list of `ComponentIOSpec` objects.
        """
        self.check_args(srcs)
        for src, dst in zip(srcs, self.inputs):
            dst.data_container.data = src.data_container.data


class _OutputsComponentTool():
    def set_outputs(
        self,
        outputs: list[ComponentIOSpec]
    ):
        """! The `set_outputs` function sets the outputs of a component
        and performs type and value checks on the provided outputs.

        @param outputs The `outputs` parameter is a list of `ComponentIOSpec` objects.
        """
        if type(outputs) is not list:
            raise TypeError(
                'Type of `outputs` should be list. '
                f'Current value: `{outputs}` (type: {type(outputs)})'
            )
        if len(outputs) == 0:
            raise TypeError('`outputs` should not be empty.')
        for output in outputs:
            if not isinstance(output, ComponentIOSpec):
                raise TypeError(
                    f'outputs (class: `{type(output)}`) is '
                    'not a subclass of `ComponentIOSpec`.'
                )
        self.outputs = outputs
        self.outputs_name = [o.name for o in self.outputs]
        if len(set(self.outputs_name)) != len(self.outputs):
            raise ValueError(
                f'There are output specs with a same name.'
            )

    def check_return(
        self,
        rets: Any
    ):
        """! The `check_return` function is used to validate the return value
        of the `run()` method, ensuring that it is a dictionary with keys
        matching the specified component input/output specifications.

        @param rets Any: The `rets` parameter is expected to be a dictionary.
        It represents the return value of a `run()` method.
        """
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
        for (name, ret), _ in zip(rets.items(), self.outputs):
            output = self.get_output_spec(name)
            assert isinstance(ret, output.data_container.data_type), (
                f'You defined {output.data_container.data_type} type for '
                f'output `{name}`, but value {ret} '
                f'(types: {[e.data_container for e in self.outputs]}) was given.'
            )

    def get_output_spec(
        self,
        name: str,
    ):
        """! The function `get_output_spec` returns the output specification
        with the given name, and raises an error if there are multiple input
        specifications with the same name.

        @param name The `name` parameter is a string that represents the name
        of the input specification that you want to retrieve.

        @return the output specification with the given name.
        """
        specs = [spec for spec in self.outputs if spec.name == name]
        if not specs:
            raise ValueError(
                'There are no output specifications with the given name.'
            )
        assert len(specs) == 1, (
            f'There is more than one output with the same name: {len(specs)}.'
        )
        return specs[-1]

    def change_output_type(
        self,
        name: str,
        type_,
    ):
        """! The function `change_output_type` changes the type of a data container
        while preserving the data it contains.

        @param name The `name` parameter is a string that represents the name of the output.
        @param type_ The `type_` parameter in the `change_output_type` method
        is the new type that you want to change the output to.
        It should be a subclass of `BaseType`.
        """
        assert issubclass(type_, BaseType)
        spec = self.get_output_spec(name)
        data = spec.data_container.data
        spec.data_container = type_()
        spec.data_container.data = data

    def move_to_output(
        self,
        rets: dict
    ):
        """! The function `move_to_output` checks the return values,
        and then assigns each return value to the corresponding output data container.

        @param rets A dictionary containing the return values.
        The keys are the names of the return values, and the values are the actual return values.
        """
        self.check_return(rets)
        for (name, ret), _ in zip(rets.items(), self.outputs):
            output = self.get_output_spec(name)
            output.data_container.data = ret


class BaseComponent(ABC):
    def __init__(
        self,
        visualizer: BaseVisualizer,
        do_logging: bool = False,
    ) -> None:
        self.do_logging = do_logging
        self.visualizer = visualizer

    @abstractmethod
    def __call__(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        raise NotImplementedError

    def log(
        self,
        message: str,
        level: str = 'info'
    ):
        if self.do_logging:
            getattr(self.logger, level.lower(), self.logger.info)(message)

    def visualize(
        self,
        *args,
        **kwargs
    ):
        self.visualizer(*args, **kwargs)


class InputsOnlyBaseComponent(BaseComponent, _InputsComponentTool):
    def __init__(
        self, /, *,
        inputs: list[ComponentIOSpec],
        visualizer: BaseVisualizer = None,
    ) -> None:
        super().__init__(visualizer)
        self.set_inputs(inputs)

    def __call__(
        self,
        *args: ComponentIOSpec,
        **kwargs: Any,
    ):
        self.move_to_input(args)
        unwrapped_args = []
        for input_ in self.inputs:
            unwrapped_args.append(input_.data_container.data)

        self.run(*unwrapped_args, **kwargs)

    @abstractmethod
    def run(
        self,
        *args,
        **kwargs
    ) -> dict:
        raise NotImplementedError


class IOBaseComponent(BaseComponent, _InputsComponentTool, _OutputsComponentTool):
    def __init__(
        self, /, *,
        inputs: list[ComponentIOSpec] = None,
        outputs: list[ComponentIOSpec] = None,
        visualizer: BaseVisualizer = None,
    ) -> None:
        super().__init__(visualizer)
        self.set_inputs(inputs)
        self.set_outputs(outputs)

    def __call__(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        self.move_to_input(args)
        unwrapped_args = []
        for input_ in self.inputs:
            unwrapped_args.append(input_.data_container.data)

        rets = self.run(*unwrapped_args, **kwargs)

        self.move_to_output(rets)
        if len(self.outputs) > 1:
            return self.outputs
        return self.outputs[0]

    @abstractmethod
    def run(
        self,
        *args,
        **kwargs
    ) -> dict:
        raise NotImplementedError
