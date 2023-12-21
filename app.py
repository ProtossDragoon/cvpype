# TODO: This file is designed to test the functionality of Streamer and related components.
# Desired operational outcomes are not yet attainable.

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
from cvpype.python.backend.web.streamer.rtimage import RealtimeImageWebStreamer
from cvpype.python.applications.pipelines.linetracking import LineTrackingPipeline

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

server = get_server()


@st.cache_resource
def get_pipeline(
):
    pipe = LineTrackingPipeline(
        crop_y=330,
        crop_y_end=380,
        roi_y=370,
        image_h=480
    )
    pipe.autocreate_graph()
    return pipe

pipe = get_pipeline()


@st.cache_resource
def get_streamingframe(
    name: str,
    video_path: str | None = None,
) -> StreamingFrame:
    if video_path:
        # video -> video streamer -> web server -> streaming frame
        streamer = VideofileWebStreamer(video_path, width=480)
    else:
        # camera -> camrea streamer -> web server -> streaming frame
        streamer = CameraWebStreamer(width=480)
    server.add_videostream(name, streamer)
    frame = StreamingFrame(name, server)
    return frame


@st.cache_resource
def get_streamingframe_from_pipe(
    name: str,
    visualizer_name: str,
):
    # visualizer -> real time frame streamer
    # video -> video streamer -> \
        # pipeline -> (visualizer) -> real time frame streamer -> \
            # web server -> streaming frame
    visualizer = pipe.visualizers.get(visualizer_name)
    streamer = RealtimeImageWebStreamer()
    server.add_videostream(name, streamer)
    visualizer.set_web_streamer(streamer)
    frame = StreamingFrame(name, server)
    return frame


frame1 = get_streamingframe('main_cam1')
frame2 = get_streamingframe(
    'sample.mov',
    video_path='./data/sample.mov'
)
for name in [
    'GrayscailingComponent',
    'CroppingComponent',
    'BilateralBlurringComponent',
    'EdgeDetectingComponent',
    'LineFindingComponent',
    'SDVLineVisualizationComponent',
    'WidthBasedIntersectionFiltering'
]:
    pipe.visualizers.get(name).is_threading = True

frame3 = get_streamingframe_from_pipe('GrayscailingComponent', 'GrayscailingComponent')
frame4 = get_streamingframe_from_pipe('EdgeDetectingComponent', 'EdgeDetectingComponent')
frame5 = get_streamingframe_from_pipe('SDVLineVisualizationComponent', 'SDVLineVisualizationComponent')


@st.cache_resource
def run_server():
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()


@st.cache_resource
def run_pipe(
    video_path: str
):
    unique = set([e.is_threading for _, e in pipe.visualizers.items()])
    assert len(unique) == 1, (
        'Some OS cannot utilize cv2.imshow or plt.show in a thread. '
        'Port all visualizers into the web streaming mode. '
        f'Visualizers: {list(pipe.visualizers.keys())}'
    )
    streamer = VideofileWebStreamer(video_path)
    thread = threading.Thread(target=pipe.run_from_streamer(streamer), daemon=True)
    thread.start()


run_server()
run_pipe('./data/sample_lcurve.mov')


col1, col2 = st.columns([1, 1])
with col1:
    with st.container(border=True):
        st.header(frame1.name)
        st.caption(frame1.url)
        frame1.wait_ready()
        components.iframe(
            frame1.url,
            width=frame1.width,
            height=frame1.height,
        )
with col2:
    with st.container(border=True):
        st.header(frame2.name)
        st.caption(frame2.url)
        frame2.wait_ready()
        components.iframe(
            frame2.url,
            width=frame2.width,
            height=frame2.height,
        )
col3, col4 = st.columns([1, 1])
with col3:
    with st.container(border=True):
        st.header(frame3.name)
        st.caption(frame3.url)
        frame3.wait_ready()
        components.iframe(
            frame3.url,
            height=frame3.height,
        )
with col4:
    with st.container(border=True):
        st.header(frame4.name)
        st.caption(frame4.url)
        frame4.wait_ready()
        components.iframe(
            frame4.url,
            width=frame4.width,
            height=frame4.height,
        )
col5, col6 = st.columns([1, 1])
with col5:
    with st.container(border=True):
        st.header(frame5.name)
        st.caption(frame5.url)
        frame5.wait_ready()
        components.iframe(
            frame5.url,
            width=frame5.width,
            height=frame5.height,
        )
with col6:
    pass
