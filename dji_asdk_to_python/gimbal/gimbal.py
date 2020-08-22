from dji_asdk_to_python.utils.message_builder import MessageBuilder
from dji_asdk_to_python.errors import DJIError

from dji_asdk_to_python.utils.shared import checkParameters
from dji_asdk_to_python.utils.socket_utils import SocketUtils


class Gimbal:
    """
    This class provides methods to control the gimbal. These include rotating the gimbal with angle. This object is available from the Aircraft object.
    """

    def __init__(self, app_ip):
        """
        Args:
            - app_ip (str): Android device ip
        """
        self.app_ip = app_ip

    def rotate(self, pitch, roll, yaw, callback=None, timeout=10):
        """
        Rotate gimbal's pitch, roll, and yaw with ABSOLUTE_ANGLE.

        Args:
            - callback (function): An callback function with a simgle parameter of type DJIError
            - timeout (int): A timeout seconds time
        """
        checkParameters(callback=callback, method_name="startLanding", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.ROTATE,
            message_class=MessageBuilder.GIMBAL,
            message_data={"pitch": pitch, "roll": roll, "yaw": yaw},
        )

        return_type = DJIError

        blocking = callback is None

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )
