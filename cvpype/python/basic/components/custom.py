# Project
from cvpype.python.iospec import ComponentIOSpec

# Project-Types
from cvpype.python.core.types.base import BaseType

# Project-Components
from cvpype.python.core.components.base import BaseComponent


class CustomComponent(BaseComponent):
    """This class serves as a wrapper for the BaseComponent,
    providing an abstraction for the application layer.
    """
    inputs = [
        ComponentIOSpec(
            name='temp',
            data_container=BaseType(),
        )
    ]
    outputs = [
        ComponentIOSpec(
            name='temp',
            data_container=BaseType(),
        )
    ]
