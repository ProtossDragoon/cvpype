# cvpype

Computer Vision Pipeline with Python Frontend

## Quickstart

NOTE: This project requires Python >= 3.9

```
git clone https://github.com/ProtossDragoon/cvpype.git
cd cvpype
python3 -m pip install -r requirements.txt
python3 -m scripts.pipeline_from_video data/sample_bumpy.avi
```

## Motivation

```
💡 Conceptualize an Image Processing System Pipeline
----- Top Boundary of cvpype Concerns -----
- **Is the algorithm functioning properly?**
  - ✅ Supports real-time components and file visualization
- **Does the algorithm effectively integrate with other algorithms?**
  - ✅ Rapid pipeline connectivity support
  - ✅ Extensive support for pipeline visualization
- **Is there considerable potential for optimization in the algorithm?**
  - ✅ Easy toggle between debugging and optimization modes
  - TODO: Develop code templates for seamless numba integration
  - TODO: In-depth benchmarking of the algorithm's computation time, including Python overhead analysis
  - TODO: Implement automated parallel processing in the pipeline
- **How would the algorithm appear if developed in a low-level language?**
  - TODO: Provide code templates for straightforward pybind integration
----- Bottom Boundary of cvpype Concerns -----
💪 Redesign the pipeline for commercial application
```

- In image processing, there's often a complex interdependence among various algorithms.
- This complexity can lead to situations where it's crucial to understand the impact of upstream algorithm results on downstream algorithm outputs.
- When a pipeline is formed from these intricate image processing algorithms, the ability to efficiently parallelize each element becomes vital.
- It's necessary to have a structure that facilitates quick Python-based prototyping and visualization, while also allowing for easy integration of implementations like C++.

## Feature preview

### Easy Expansion

Start by creating your own custom component:

```python
from cvpype.python.iospec import ComponentIOSpec
from cvpype.python.basic.types.cvimage import ImageType
from cvpype.python.basic.components.custom import CustomComponent
from cvpype.python.basic.visualizer.image import ImageVisualizer

class MyBlurringComponent(CustomComponent):
    def __init__(
        self
    ):
        super().__init__(
            inputs=[
                ComponentIOSpec(
                    name='image',
                    data_container=ImageType(),
                )
            ],
            outputs=[
                ComponentIOSpec(
                    name='image',
                    data_container=ImageType(),
                )
            ],
            visualizer=ImageVisualizer(
                name='MyBlurringComponent'
            )
        )

    def run(
        self,
        image,
        sigma_color: int = 10,
        sigma_space: int = 10
    ) -> dict:
        blurred_image = cv2.bilateralFilter(
            image, -1,
            sigma_color,
            sigma_space
        )
        self.visualize(blurred_image)
        self.log('Operation completed!')
        return {'image': blurred_image}
```

Test your custom component:

```python
my_component = MyComponent()
# Load opencv image into `frame` variable.
ret = my_component(frame)
im = ret['image'] # `image` is the key of the dictionary that `run` method returns.
```

Incorporate your custom component into a pipeline.

```python
# Import your `MyBlurringComponent` component.
from cvpype.python.basic.components.inputs import InputsComponent
from cvpype.python.basic.pipelines.custom import CustomPipeline
from cvpype.python.basic.components.edgedetecting import EdgeDetectingComponent

class MyPipeline(CustomPipeline):
    def __init__(
        self
    ):
        super().__init__()
        self.inputs = InputsComponent()
        self.blurring = MyBlurringComponent()
        self.edge_detecting = EdgeDetectingComponent()

    def run(
        self,
        image
    ):
        image = self.inputs(image)
        blurred_image = self.blurring(image)
        edge_image = self.edge_detecting(blurred_image)
        return edge_image
```

Execute the pipeline:

```python
my_pipeline = MyPipeline()
my_pipeline.autocreate_graph()
# Load opencv image into `frame` variable.
ret = my_pipeline.run(frame)
im = ret['image'] # `image` is the key of the dictionary that `run` method in the final component returns.
```

### Web visualizer

Use the Pipeline class to automatically and effortlessly convert your visualizers into web-compatible formats.

![](./docs/visualizer.gif)

## Etc

- document: `cd build && cmake .. && make docs && cd ..`
- test: `cd build && cmake .. && make test & cd ..`

# Roadmap

- Implement a producer-consumer architecture utilizing a queue to manage threading in the web visualizer.
- Employ multi-processing to efficiently operate the image processing pipeline.
- Develop a user-friendly and easily editable web visualizer.
- Conceal IOSpec within the run method of the visualizer.

## 🔥

- The current source code is not stable. It has numerous bugs and is challenging to manage.
- Any contributions are welcome. Feel free to make changes to the source code.
- Let's fight together.
