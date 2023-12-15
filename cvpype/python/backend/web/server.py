# Built-in
import argparse

# Third party
import flask

# Project
from cvpype.python.backend.web.streamer.base import BaseWebStreamer
from cvpype.python.backend.web.streamer.camera import CameraWebStreamer


class Server():
    @property
    def app(
        self
    ) -> flask.Flask:
        return self._app

    @app.setter
    def app(
        self,
        app: flask.Flask,
    ):
        self._app = app

    def __hash__(
        self
    ) -> int:
        """! The function calculates a hash value
        based on the host and port attributes of an object.
        This function is useful for `streamlit` web framework that
        detects identical object by hash value to prevent
        re-create or re-initializing the server object.

        @return The code is returning an integer value.
        """
        import re
        return 100000000000 + int(
            ''.join(re.findall(r'\d+', f'{self.host}:{self.port}'))
        )

    def __init__(
        self,
        host: str | None = '0.0.0.0',
        port: int | None = 8000,
    ):
        self.host = host
        self.port = port
        self.app = flask.Flask(__name__)
        self.app.add_url_rule(
            rule='/', view_func=self.index,
        )
        self.streamers = {}

    def get_streamer(
        self,
        name: str
    ) -> BaseWebStreamer:
        return self.streamers.get(name)

    def get_url(
        self,
        name
    ):
        if name not in self.streamers:
            raise KeyError(
                f'Videostream `{name}` is not exists! '
                f'(Exist names: {list(self.streamers.keys())})'
            )
        return f'http://{self.host}:{self.port}/{name}'

    def run(
        self,
    ):
        self.app.run(
            host=self.host,
            port=self.port,
            threaded=True,
            debug=True,
            use_reloader=False,
        )

    def index(
        self
    ):
        def has_no_empty_params(rule):
            defaults = rule.defaults if rule.defaults is not None else ()
            arguments = rule.arguments if rule.arguments is not None else ()
            return len(defaults) >= len(arguments)

        links = []
        for rule in self.app.url_map.iter_rules():
            # NOTE: Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = flask.url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        return links

    def add_videostream(
        self,
        name: str,
        streamer: BaseWebStreamer,
    ):
        assert not name.startswith('/'), (
            'name must not start with slash(/). '
            f'(Current value: `{name}`)'
        )
        if name in self.streamers:
            raise KeyError(
                f'Videostream `{name}` already exists.'
            )
        streamer.open()
        self.streamers[name] = streamer
        self.app.add_url_rule(
            rule=f'/{name}',
            view_func=streamer.response(name)
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--port",
        type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)"
    )
    args = parser.parse_args()
    app = Server(port=args.port)
    app.add_videostream('/video_feed', CameraWebStreamer())
    app.run()
