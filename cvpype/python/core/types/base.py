class BaseType:
    data_type = (object,)

    def __init__(
        self,
    ):
        self.data = None

    def __init_subclass__(
        cls
    ):
        if not isinstance(cls.data_type, (type, tuple)):
            raise TypeError(
                '`data_type` class variable should be a single class type '
                'or a tuple that can pass `isinstance` function.'
            )
        if isinstance(cls.data_type, type):
            cls.data_type = (cls.data_type,)
        if isinstance(cls.data_type, tuple):
            for dt in cls.data_type:
                if not isinstance(dt, type):
                    raise TypeError(
                        'All elements of the tuple in `data_type` '
                        'class variable should be class types.'
                    )

    def _check_inner_data_type(
        self
    ):
        if not isinstance(self.data, self.data_type):
            for data_type in self.data_type:
                raise TypeError(
                    f'The data `{type(self.data)}` passed through '
                    f'the class `{self.__class__.__name__}` '
                    f'is not an instance of the class `{data_type.__name__}`.'
                )

    def is_proper_for(
        self,
        type_: object,
    ):
        """
        The function `is_proper_for` checks if the data type of an object
        is a subtype of a specified type and raises an error if it is not.

        @param type_ The `type_` parameter is an object that represents the expected data type. It is used
        to check if the current object is a subtype of the expected data type.
        """
        if not issubclass(self.__class__, type_.__class__):
            raise TypeError(
                f'Data type mismatched `{self.__class__.__name__}`. '
                f'(Expected a subtype of `{type_.__class__.__name__}`)'
            )
        self._check_inner_data_type()

    def to_file(
        self,
        path: str
    ):
        raise NotImplementedError("Must be implemented by a subclass.")
