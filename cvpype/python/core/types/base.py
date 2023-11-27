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

    def check_type(
        self
    ):
        if not isinstance(self.data, self.data_type):
            for data_type in self.data_type:
                raise TypeError(
                    f'The data `{type(self.data)}` passed through '
                    f'the class `{self.__class__.__name__}` '
                    f'is not an instance of the class `{data_type.__name__}`.'
                )

    def to_file(
        self,
        path: str
    ):
        raise NotImplementedError("Must be implemented by a subclass.")
