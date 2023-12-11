# Built-in
import unittest

# Third party
import numpy as np

# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.core.types.base import BaseType
from cvpype.python.basic.types.cvimage import ImageType

# Project-Components
from cvpype.python.core.components.base import IOBaseComponent
from cvpype.python.basic.components.inputs import InputsComponent

# Project-Pipelines
from cvpype.python.core.pipelines.base import BasePipeline


class ExampleAddComponent(IOBaseComponent):
    def __init__(
        self
    ):
        super().__init__(
            inputs = [
                ComponentIOSpec(
                    name='example_input',
                    data_container=BaseType()
                )
            ],
            outputs = [
                ComponentIOSpec(
                    name='example_output',
                    data_container=BaseType()
                )
            ]
        )

    def run(
        self,
        x
    ) -> dict:
        return {'example_output': x + 1}


class ExampleImageIOComponent(IOBaseComponent):
    def __init__(
        self
    ):
        super().__init__(
            inputs = [
                ComponentIOSpec(
                    name='example_input',
                    data_container=ImageType()
                )
            ],
            outputs = [
                ComponentIOSpec(
                    name='example_output',
                    data_container=ImageType()
                )
            ]
        )

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
        self.input = InputsComponent()
        self.add_one = ExampleAddComponent()

    def run(
        self,
        x
    ):
        x1 = self.input(x)
        x2 = self.add_one(x1)
        return x2


class ExampleIdenticalComponentExistentPipeline(BasePipeline):
    def __init__(
        self
    ) -> None:
        super().__init__()
        self.input = InputsComponent()
        self.add_one_1 = ExampleAddComponent()
        self.add_one_2 = ExampleAddComponent()

    def run(
        self,
        x
    ):
        x1 = self.input(x)
        x2 = self.add_one_1(x1)
        x3 = self.add_one_2(x2)
        return x3


class ExampleImagePipeline(BasePipeline):
    def __init__(
        self
    ) -> None:
        super().__init__()
        self.input = InputsComponent()
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
        self.pipeline.autocreate_graph()
        self.assertIn(self.pipeline.input,
                      self.pipeline.components.values())
        self.assertIn(self.pipeline.add_one,
                      self.pipeline.components.values())

    def test_run(self):
        for i in range(-100, 100):
            self.assertEqual(i+1, self.pipeline.run(i).data_container.data)


class TestIdenticalComponentExistentPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ExampleIdenticalComponentExistentPipeline()

    def test_init(self):
        self.assertIsInstance(self.pipeline, BasePipeline)

    def test_init_graph(self):
        self.pipeline.autocreate_graph()

    def test_run(self):
        for i in range(-100, 100):
            self.assertEqual(i+2, self.pipeline.run(i).data_container.data)


class TestImagePipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ExampleImagePipeline()

    def test_init(self):
        self.assertIsInstance(self.pipeline, BasePipeline)

    def test_init_graph(self):
        self.pipeline.autocreate_graph()
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
