# Built-in
import unittest

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project
from cvpype.python.core.types.base import BaseType

# Project-Components
from cvpype.python.basic.components.inputs import InputsComponent


class TestInputsComponent(unittest.TestCase):

    def test_call_with_non_spec_args(self):
        component = InputsComponent()
        x = 123

        y = component(x)
        self.assertIsInstance(y, ComponentIOSpec)
        self.assertIsInstance(y.data_container, BaseType)
        self.assertEqual(y.data_container.data, x)

    def test_call_with_spec_args(self):
        component = InputsComponent()
        x = 123
        spec_arg = ComponentIOSpec('test', BaseType())
        spec_arg.data_container.data = x

        y = component(spec_arg)
        self.assertIsNot(y, spec_arg)
        self.assertIsInstance(y, ComponentIOSpec)
        self.assertIsInstance(y.data_container, BaseType)
        self.assertEqual(y.data_container.data, x)

    def test_repeated_calls(self):
        component = InputsComponent()
        x1 = 123
        x2 = 456

        y1 = component(x1)
        self.assertIsInstance(y1, ComponentIOSpec)
        self.assertEqual(y1.data_container.data, x1)
        y2 = component(x2)
        self.assertIsInstance(y2, ComponentIOSpec)
        self.assertEqual(y2.data_container.data, x2)
        self.assertIs(y1, y2)

    def test_call_with_non_spec_multiple_args(self):
        component = InputsComponent()
        x1 = 123
        x2 = 'test'

        y = component(x1, x2)
        self.assertEqual(len(y), 2)
        self.assertIsInstance(y[0], ComponentIOSpec)
        self.assertIsInstance(y[1], ComponentIOSpec)
        self.assertEqual(y[0].data_container.data, x1)
        self.assertEqual(y[1].data_container.data, x2)

    def test_call_with_spec_multiple_args(self):
        component = InputsComponent()
        x1 = 123
        x2 = 'test'
        spec_arg1 = ComponentIOSpec('test1', BaseType())
        spec_arg2 = ComponentIOSpec('test2', BaseType())
        spec_arg1.data_container.data = x1
        spec_arg2.data_container.data = x2

        y = component(spec_arg1, spec_arg2)
        self.assertEqual(len(y), 2)
        self.assertIsNot(y[0], spec_arg1)
        self.assertIsNot(y[1], spec_arg2)
        self.assertIsInstance(y[0], ComponentIOSpec)
        self.assertIsInstance(y[1], ComponentIOSpec)
        self.assertEqual(y[0].data_container.data, x1)
        self.assertEqual(y[1].data_container.data, x2)

    def test_call_with_combined_multiple_args(self):
        component = InputsComponent()
        x1 = 123
        x2 = 'test'
        spec_arg = ComponentIOSpec('test', BaseType())
        spec_arg.data_container.data = x2

        y = component(x1, spec_arg)
        self.assertEqual(len(y), 2)
        self.assertIsInstance(y[0], ComponentIOSpec)
        self.assertIsNot(y[1], spec_arg)
        self.assertIsInstance(y[1], ComponentIOSpec)
        self.assertEqual(y[0].data_container.data, x1)
        self.assertEqual(y[1].data_container.data, x2)


if __name__ == '__main__':
    unittest.main()
