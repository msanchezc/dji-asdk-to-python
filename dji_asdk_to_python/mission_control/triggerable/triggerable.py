from dji_asdk_to_python.utils.message_builder import MessageBuilder
from dji_asdk_to_python.errors import DJIError
from dji_asdk_to_python.utils.shared import checkParameters
from dji_asdk_to_python.utils.socket_utils import SocketUtils


class Triggerable:
    def __init__(self, app_ip):
        self.app_ip = app_ip

    def getTriggers(self, callback=None, timeout=10):
        """Get List of Trigger objects"""

        checkParameters(callback=callback, method_name="getTriggers", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_TRIGGERS,
            message_class=MessageBuilder.MISSION_CONTROL,
            message_data=None,
        )

        return_type = list

        SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
        )

    def setTriggers(self, triggers, callback=None, timeout=10):
        """Set the Trigger objects list"""

        checkParameters(callback=callback, method_name="getTriggers", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_VIRTUAL_STICK_MODE_ENABLED,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=triggers,
        )

        return_type = DJIError

        SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
        )
