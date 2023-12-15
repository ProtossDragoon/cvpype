import time
import logging
import threading

# Third party
import streamlit as st
import streamlit.components.v1 as components

# Project
from cvpype.python.backend.web.server import Server
from cvpype.python.backend.web.streamer.camera import CameraWebStreamer
from cvpype.python.backend.web.streamer.videofile import VideofileWebStreamer

st.set_page_config(
    page_title='cvpype',
    layout='wide',
    page_icon='🔥',
    menu_items={
        'About': 'https://github.com/ProtossDragoon/cvpype'
    }
)

class StreamingFrame:
    def __set_logger(
        self,
        name: str
    ):
        self.logger = logging.getLogger(
            f'{self.__class__.__name__}({name})'
        )
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(
            f'(%(asctime)s)[%(levelname)s]:%(module)s.%(name)s: %(message)s',
            datefmt='%Y/%m/%d-%H:%M:%S',
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def __init__(
        self,
        name: str,
        running_server: Server,
    ):
        self.__set_logger(name)
        self.logger.info('Setting up a new StreamingFrame')
        self.running_server = running_server
        self.name = name
        self.width = None
        self.height = None

    @property
    def url(
        self
    ):
        url = self.running_server.get_url(self.name)
        self.logger.info(f'{url}')
        return url

    def wait_ready(
        self
    ):
        while (
            (self.width is None) or
            (self.height is None)
        ):
            self.logger.info(
                'Waiting to get the iframe window\'s '
                'proper width and height...'
            )
            self.width = self.running_server.get_streamer(self.name).width
            self.height = self.running_server.get_streamer(self.name).height
            time.sleep(0.3)
        self.logger.info(
            'Completed to set the window\'s '
            f'width and height! ({self.width}, {self.height})'
        )


@st.cache_resource
def get_server(
) -> Server:
    server = Server()
    return server


@st.cache_resource
def get_stream(
    name: str,
    video_path: str | None = None
) -> StreamingFrame:
    global server
    if video_path:
        streamer = VideofileWebStreamer(video_path, width=480)
    else:
        streamer = CameraWebStreamer(width=480)
    server.add_videostream(name, streamer)
    frame = StreamingFrame(name, server)
    return frame


@st.cache_resource
def run_server(
):
    global server
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()


server = get_server()
frame1 = get_stream('main_cam1')
frame2 = get_stream('main_cam2')
frame3 = get_stream('sample.mov', video_path='./data/sample.mov')
run_server()

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.header(frame1.name)
    st.caption(frame1.url)
    frame1.wait_ready()
    components.iframe(
        frame1.url,
        width=frame1.width,
        height=frame1.height,
    )
with col2:
    st.header(frame2.name)
    st.caption(frame2.url)
    frame2.wait_ready()
    components.iframe(
        frame2.url,
        width=frame2.width,
        height=frame2.height,
    )
with col3:
    st.header(frame3.name)
    st.caption(frame3.url)
    frame3.wait_ready()
    components.iframe(
        frame3.url,
        width=frame3.width,
        height=frame3.height,
    )
