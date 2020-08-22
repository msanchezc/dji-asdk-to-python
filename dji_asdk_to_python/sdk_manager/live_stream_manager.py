from dji_asdk_to_python.utils.streaming_utils import StreamingListener
from dji_asdk_to_python.utils.socket_utils import SocketUtils
from dji_asdk_to_python.utils.message_builder import MessageBuilder


class RTPManager:
    def __init__(self, app_ip):
        self.app_ip = app_ip
        self.streaming_listener = StreamingListener(width=1920, height=1088)

    def _remote_start(self):
        ip = SocketUtils.getIp()
        message = MessageBuilder.build_message(
            message_method=MessageBuilder.START_RTP_STREAMING,
            message_class=MessageBuilder.RTP_STREAMING,
            message_data={"port": self.streaming_listener.port, "ip": ip},
        )

        self.streaming_listener.start()  # TODO check for pipe state

        def callback(result):
            if isinstance(result, bool) and result:
                return True
            else:
                return result

        return_type = bool
        timeout = 10
        result = SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=True,
        )
        return result

    def _remote_stop(self):
        message = MessageBuilder.build_message(
            message_method=MessageBuilder.STOP_RTP_STREAMING,
            message_class=MessageBuilder.RTP_STREAMING,
            message_data={},
        )

        def callback(result):
            if isinstance(result, bool) and result:
                self.streaming_listener.stop()
                return True
            else:
                return result

        return_type = bool
        timeout = 10

        result = SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=True,
        )
        return result

    def setWidth(self, width):
        """
        Set frames width
        """
        assert isinstance(width, int)
        if self.isStreaming():
            raise Exception("Already streaming, can not set width")
        self.streaming_listener.width = width

    def setHeigth(self, height):
        """
        Set frames heigth
        """
        assert isinstance(height, int)
        if self.isStreaming():
            raise Exception("Already streaming, can not set height")
        self.streaming_listener.height = height

    def getWidth(self):
        """
        Returns:
            [int]: Width of frames
        """
        return self.streaming_listener.width

    def getHeight(self):
        """
        Returns:
            [int]: Height of frames
        """
        return self.streaming_listener.height

    def isStreaming(self):
        """
        Returns:
            [boolean]: True if is streaming
        """
        return self.streaming_listener.streaming

    def getFrame(self):
        """
        Returns:
            [numpy.array]: An rgb image
        """
        return self.streaming_listener.getFrame()

    def startStream(self):
        """
            Start RTP streaming
        """
        return self._remote_start()

    def stopStream(self):
        """
            Stop RTP streaming
        """
        return self._remote_stop()


class RTMPManager:
    def __init__(self, app_ip):
        self.app_ip = app_ip

    def isStreaming(self, timeout=10):
        """
        Determines if the live streaming starts or not. After starting this flag will not be affected by the RTMP server status.

        Returns:
            [bool]: True if the live stream manager is streaming.
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.IS_STREAMING,
            message_class=MessageBuilder.LIVE_STREAM_MANAGER,
            message_data=None,
        )

        return_type = bool

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            timeout=timeout,
            callback=None,
            return_type=return_type,
            blocking=True,
        )

    def setLiveUrl(self, live_url, timeout=10):
        """
        Determines if the live streaming starts or not. After starting this flag will not be affected by the RTMP server status.

        Args:
            - live_url (str): The URL address string of the RTMP Server.

        Returns:
            [bool]: True if live url was setted
        """

        assert isinstance(live_url, str)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.SET_LIVE_URL,
            message_class=MessageBuilder.LIVE_STREAM_MANAGER,
            message_data={"live_url": live_url},
        )

        return_type = bool

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            timeout=timeout,
            return_type=return_type,
            callback=None,
            blocking=True,
        )

    def startStream(self, timeout=10):
        """
        Starts the live streaming. If the manager starts successfully, isStreaming will return true. The encoder will start to encoding the video frame if it is needed. The video will be streamed to the RTMP server if the server is available. The audio can be streamed along with the video if the audio setting is enabled.

        Returns:
            [int]: An int value of the error code.
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.START_STREAM,
            message_class=MessageBuilder.LIVE_STREAM_MANAGER,
            message_data=None,
        )

        return_type = int

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            timeout=timeout,
            callback=None,
            return_type=return_type,
            blocking=True,
        )

    def stopStream(self, timeout=10):
        """
        Stop the live streaming. The operation is asynchronous and isStreaming will return false when the operation is complete.

        Returns:
            [bool]: True if stopStream was called
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.STOP_STREAM,
            message_class=MessageBuilder.LIVE_STREAM_MANAGER,
            message_data=None,
        )

        return_type = bool

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            timeout=timeout,
            return_type=return_type,
            callback=None,
            blocking=True,
        )


class LiveStreamManager:
    """
        The manager is used tolive streaming using RTMP and RTP.
    """

    def __init__(self, app_ip):
        self.app_ip = app_ip

    def getRTPManager(self):
        """
        Returns:
            [RTPManager]: An RTPManager instance
        """
        return RTPManager(self.app_ip)

    def getRTMPManager(self):
        """
        Returns:
            [RTPManager]: An RTMPManager instance
        """
        return RTMPManager(self.app_ip)
