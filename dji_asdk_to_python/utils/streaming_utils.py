from contextlib import closing
import socket
import numpy as np
import cv2
import random
import string
import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst  # noqa: E402


class StreamingListener(object):
    def __init__(self, width=1920, height=1080, port=None):
        self.width = width
        self.height = height
        self.streaming = False
        self.pipe_name = self.rand_str(10)
        if port is None:
            self.port = StreamingListener.find_free_port()
        else:
            self.port = port

        # Gstreamer
        Gst.init(None)
        self._frame = None
        self.video_source = (
            'udpsrc port=%s caps="application/x-rtp, \
                encoding-name=(string)H264" ! queue '
            % self.port
        )
        self.video_decode = "! rtph264depay ! queue ! h264parse ! avdec_h264 ! \
            videoconvert ! video/x-raw,format=(string)BGR ! videoconvert"

        # Create a sink to get data
        self.video_sink_conf = (
            "! appsink name=%s emit-signals=true \
                sync=false max-buffers=2 drop=true" % self.pipe_name
        )

        self.video_pipe = None
        self.video_sink = None
        self.appsrc = None
        # End Gstreamer

    @staticmethod
    def find_free_port():
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('localhost', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    @staticmethod
    def rand_str(n):
        return ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=n)
        )

    @staticmethod
    def _gst_to_opencv(sample):
        buf = sample.get_buffer()
        caps = sample.get_caps()
        array = np.ndarray(
            (
                caps.get_structure(0).get_value("height"),
                caps.get_structure(0).get_value("width"),
                3,
            ),
            buffer=buf.extract_dup(0, buf.get_size()),
            dtype=np.uint8,
        )
        return array

    def _gst_callback(self, sink):
        sample = sink.emit("pull-sample")
        new_frame = self._gst_to_opencv(sample)
        new_frame = cv2.resize(new_frame, (self.width, self.height))
        self._frame = new_frame
        return Gst.FlowReturn.OK

    def start(self):
        self.streaming = True

        # Gstreamer
        config = [
            self.video_source,
            self.video_decode,
            self.video_sink_conf,
        ]
        command = " ".join(config)
        self.video_pipe = Gst.parse_launch(command)
        self.video_pipe.set_state(Gst.State.PLAYING)
        self.appsrc = self.video_pipe.get_child_by_name("source")
        self.video_sink = self.video_pipe.get_by_name(self.pipe_name)
        self.video_sink.connect("new-sample", self._gst_callback)
        # End Gstreamer

    def getFrame(self):
        frame = self._frame
        self._frame = None
        return frame  # self._images_queue.pop()

    def stop(self):
        self.streaming = False
        self.video_pipe.set_state(Gst.State.NULL)
