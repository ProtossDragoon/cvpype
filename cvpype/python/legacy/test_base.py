# Built-in
import unittest

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.core.types.base import BaseType

# Project-Components
from cvpype.python.core.components.base import (
    InputsOnlyBaseComponent,
    IOBaseComponent,
)


class TestInputsOnlyBaseComponent(unittest.TestCase):
    def test_inputs_type_checking(self):
        with self.subTest(
            'Case: type of `inputs` is not list.'
        ):
            inputs = ComponentIOSpec(name='test', data_container=BaseType())
            with self.assertRaises(TypeError):
                InputsOnlyBaseComponent(inputs=inputs)

        with self.subTest(
            'Case: type of each element in `inputs` list is not `ComponentIOSpec`.'
        ):
            inputs = [1, 'string', (1, 2, 3)]
            with self.assertRaises(TypeError):
                InputsOnlyBaseComponent(inputs=inputs)

        with self.subTest(
            'Case: single element in `inputs` list.'
        ):
            inputs = [ComponentIOSpec(name='a', data_container=BaseType())]
            InputsOnlyBaseComponent(inputs=inputs)

        with self.subTest(
            'Case: multiple elements in `inputs` list.'
        ):
            inputs = [
                ComponentIOSpec(name='a', data_container=BaseType()),
                ComponentIOSpec(name='b', data_container=BaseType()),
                ComponentIOSpec(name='c', data_container=BaseType()),
                ComponentIOSpec(name='d', data_container=BaseType()),
            ]
            InputsOnlyBaseComponent(inputs=inputs)

    def test_duplicate_input_names(self):
        inputs = [
            ComponentIOSpec(name='duplicate', data_container=BaseType()),
            ComponentIOSpec(name='duplicate', data_container=BaseType())
        ]
        with self.assertRaises(ValueError):
            InputsOnlyBaseComponent(inputs=inputs)


class TestIOBaseComponent(unittest.TestCase):
    def test_io_type_checking(self):
        with self.subTest(
            'Case: proper `outputs`, but type of `inputs` is not list.'
        ):
            inputs = ComponentIOSpec(name='a', data_container=BaseType())
            outputs = [ComponentIOSpec(name='b', data_container=BaseType())]
            with self.assertRaises(TypeError):
                IOBaseComponent(inputs=inputs, outputs=outputs)

        with self.subTest(
            'Case: proper `outputs`, but type of `outputs` is not list.'
        ):
            inputs = [ComponentIOSpec(name='a', data_container=BaseType())]
            outputs = ComponentIOSpec(name='b', data_container=BaseType())
            with self.assertRaises(TypeError):
                IOBaseComponent(inputs=inputs, outputs=outputs)

        with self.subTest(
            'Case: proper `outputs`, but invalid empty `inputs`.'
        ):
            inputs = []
            outputs = [ComponentIOSpec(name='input1', data_container=BaseType())]
            with self.assertRaises(TypeError):
                IOBaseComponent(inputs=inputs, outputs=outputs)

        with self.subTest(
            'Case: proper `inputs`, but invalid empty `outputs`.'
        ):
            inputs = [ComponentIOSpec(name='input1', data_container=BaseType())]
            outputs = []
            with self.assertRaises(TypeError):
                IOBaseComponent(inputs=inputs, outputs=outputs)

    def test_duplicate_output_names(self):
        inputs = [
            ComponentIOSpec(name='a', data_container=BaseType()),
            ComponentIOSpec(name='b', data_container=BaseType())
        ]
        outputs = [
            ComponentIOSpec(name='duplicate', data_container=BaseType()),
            ComponentIOSpec(name='duplicate', data_container=BaseType())
        ]
        with self.assertRaises(ValueError):
            IOBaseComponent(inputs=inputs, outputs=outputs)


if __name__ == '__main__':
    unittest.main()
