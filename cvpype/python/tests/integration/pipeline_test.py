# Built-in
import unittest

# Project-Components
from cvpype.python.core.components.base import BaseComponent, InputsBaseComponent

# Project-Pipelines
from cvpype.python.core.pipelines.base import BasePipeline

from cvpype.python.iospec import ComponentIOSpec


class ExampleComponent(BaseComponent):
    inputs = [
        ComponentIOSpec(
            'example_input'
        )
    ]
    outputs = [
        ComponentIOSpec(
            'example_output'
        )
    ]
    def __init__(
        self,
        do_logging: bool = True,
        do_typecheck: bool = True
    ):
        super().__init__(do_logging, do_typecheck)


class ExamplePipeline(BasePipeline):
    def __init__(
        self
    ) -> None:
        super().__init__()
        self.input = InputsBaseComponent()
        self.output = ExampleComponent()

    def run(
        self,
        x
    ):
        x1 = self.input(x)
        x2 = self.output(x1)
        return x2


class TestBasePipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ExamplePipeline()

    def test_initialization(self):
        self.assertIsInstance(self.pipeline, BasePipeline)
        self.assertIsInstance(self.pipeline.input,
                              self.pipeline.components['input'])
        self.assertIsInstance(self.pipeline.output,
                              self.pipeline.components['output'])

    def test_run(self):
        for x in range(100):
            self.assertEqual(x, self.pipeline.run(x))


if __name__ == '__main__':
    unittest.main()
