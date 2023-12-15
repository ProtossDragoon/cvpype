# Built-in
from abc import abstractmethod

# Third party
import flask

# Project
from cvpype.python.backend.base import BaseStreamer


class BaseWebStreamer(BaseStreamer):
    def __init__(
        self,
        width: int | None = None,
        height: int | None = None
    ):
        super().__init__(width=width, height=height)

    @abstractmethod
    def push_to_browser(
        self
    ):
        raise NotImplementedError

    def response(
        self,
        name: str
    ):
        # The reason why this method is so dirty:
        # Flask requires different function 'name' for each route
        # even though the functions are totally different function each other.
        # NOTE: https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
        def fn():
            return flask.Response(
                self.push_to_browser(),
                mimetype=("multipart/x-mixed-replace; boundary=frame")
            )
        fn.__name__ += f'_{name}'
        return fn
