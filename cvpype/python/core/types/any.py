# Project-Types
from cvpype.python.core.types.base import BaseType


class AnyType(BaseType):
    def is_proper_for(
        self,
        type_: object,
    ):
        pass
