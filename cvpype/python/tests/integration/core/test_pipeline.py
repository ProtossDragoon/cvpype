# Built-in
import unittest

# Third party
import numpy as np

# Project-Types
from cvpype.python.core.types.base import BaseType
from cvpype.python.basic.types.cvimage import ImageType

# Project-Components
from cvpype.python.core.components.base import BaseComponent, InputsBaseComponent

# Project-Pipelines
from cvpype.python.core.pipelines.base import BasePipeline

from cvpype.python.iospec import ComponentIOSpec


class ExampleAddComponent(BaseComponent):
    inputs = [
        ComponentIOSpec(
            name='example_input',
            data_container=BaseType()
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='example_output',
            data_container=BaseType()
        )
    ]

    def run(
        self,
        x
    ) -> dict:
        return {'example_output': x + 1}


class ExampleImageIOComponent(BaseComponent):
    inputs = [
        ComponentIOSpec(
            name='example_input',
            data_container=ImageType()
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='example_output',
            data_container=ImageType()
        )
    ]

    def run(
        self,
        image
    ) -> dict:
        return {'example_output': image}


class ExamplePipeline(BasePipeline):
    def __init__(
        self
    ) -> None:
        super().__init__()
        self.input = InputsBaseComponent()
        self.output = ExampleAddComponent()

    def run(
        self,
        x
    ):
        x1 = self.input(x)
        x2 = self.output(x1)
        return x2


class ExampleBrokenPipeline(BasePipeline):
    def __init__(
        self
    ) -> None:
        super().__init__()
        self.input = InputsBaseComponent()
        self.calc = ExampleAddComponent()
        self.output = ExampleAddComponent()

    def run(
        self,
        x
    ):
        x1 = self.input(x)
        x2 = self.calc(x1)
        x3 = self.output(x2)
        return x3


class ExampleImagePipeline(BasePipeline):
    def __init__(
        self
    ) -> None:
        super().__init__()
        self.input = InputsBaseComponent()
        self.output = ExampleImageIOComponent()

    def run(
        self,
        x
    ):
        x1 = self.input(x)
        x2 = self.output(x1)
        return x2


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ExamplePipeline()

    def test_init(self):
        self.assertIsInstance(self.pipeline, BasePipeline)

    def test_init_graph(self):
        self.pipeline.create_graph()
        self.assertIn(self.pipeline.input,
                      self.pipeline.components.values())
        self.assertIn(self.pipeline.output,
                      self.pipeline.components.values())

    def test_run(self):
        for i in range(100):
            self.assertEqual(i+1, self.pipeline.run(i).data_container.data)


class TestBrokenPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ExampleBrokenPipeline()

    def test_init(self):
        self.assertIsInstance(self.pipeline, BasePipeline)

    def test_init_graph(self):
        with self.assertRaises(AssertionError):
            self.pipeline.create_graph()


class TestImagePipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ExampleImagePipeline()

    def test_init(self):
        self.assertIsInstance(self.pipeline, BasePipeline)

    def test_init_graph(self):
        self.pipeline.create_graph()
        self.assertIn(self.pipeline.input,
                      self.pipeline.components.values())
        self.assertIn(self.pipeline.output,
                      self.pipeline.components.values())

    def test_run(self):
        arr = np.ones([1,])
        self.assertEqual(
            arr.sum(),
            self.pipeline.run(arr).data_container.data.sum()
        )
        arr = np.ones([5,])
        self.assertEqual(
            arr.sum(),
            self.pipeline.run(arr).data_container.data.sum()
        )
        arr = np.ones([1, 1])
        self.assertEqual(
            arr.sum(),
            self.pipeline.run(arr).data_container.data.sum()
        )
        arr = np.ones([1, 10])
        self.assertEqual(
            arr.sum(),
            self.pipeline.run(arr).data_container.data.sum()
        )
        arr = np.ones([10, 1])
        self.assertEqual(
            arr.sum(),
            self.pipeline.run(arr).data_container.data.sum()
        )
        arr = np.ones([100, 100])
        self.assertEqual(
            arr.sum(),
            self.pipeline.run(arr).data_container.data.sum()
        )


if __name__ == '__main__':
    unittest.main()
