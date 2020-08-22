from dji_asdk_to_python.utils.message_builder import MessageBuilder
from dji_asdk_to_python.utils.shared import checkParameters
from dji_asdk_to_python.utils.socket_utils import SocketUtils


class MissionControl:
    def __init__(self, app_ip):
        self.app_ip = app_ip

    # -------------------- MISSION OPERATORS ------------------------

    def getWaypointMissionOperator(
        self,
        callback=None,
        timeout=10
    ):
        """Returns the operator for waypoint missions"""

        checkParameters(
            callback=callback,
            method_name="getWaypointMissionOperator",
            timeout=timeout,
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_WAYPOINT_MISSION_OPERATOR,
            message_class=MessageBuilder.MISSION_CONTROL,
            message_data=None,
        )

        return_type = str

        SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
        )
