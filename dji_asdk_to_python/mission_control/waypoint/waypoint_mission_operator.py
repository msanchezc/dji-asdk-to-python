from dji_asdk_to_python.utils.message_builder import MessageBuilder
from dji_asdk_to_python.errors import DJIError
from dji_asdk_to_python.utils.shared import checkParameters
from dji_asdk_to_python.utils.socket_utils import SocketUtils


class WaypointMissionOperator:
    def __init__(self, app_ip):
        self.app_ip = app_ip

    # ------------------------------ PREPARATION ------------------------

    def loadMission(self, mission, callback=None, timeout=10):
        """Loads the WaypointMission into device memory.
            This also verifies all the information of mission"""

        checkParameters(callback=callback,
                        method_name="loadMission", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.LOAD_MISSION,
            message_class=MessageBuilder.WAYPOINT_MISSION_OPERATOR,
            message_data={"data": mission.__dict__},
        )

        blocking = True

        return_type = DJIError

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )

    def getLoadedMission(self, callback=None, timeout=10):
        """Gets the currently loaded mission of the operator"""

        checkParameters(
            callback=callback, method_name="getLoadedMission", timeout=timeout
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_LOADED_MISSION,
            message_class=MessageBuilder.WAYPOINT_MISSION_OPERATOR,
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

    def uploadMission(self, callback=None, timeout=10):
        """Starts to upload the getLoadedMission to the aircraft.
            It can only be called when the getLoadedMission is complete and the getCurrentState is READY_TO_UPLOAD"""

        checkParameters(callback=callback,
                        method_name="uploadMission", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.UPLOAD_MISSION,
            message_class=MessageBuilder.WAYPOINT_MISSION_OPERATOR,
            message_data=None,
        )

        return_type = DJIError

        SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
        )

    def retryUploadMission(self, callback=None, timeout=10):
        """Retry upload waypoint mission"""

        checkParameters(
            callback=callback, method_name="retryUploadMission", timeout=timeout
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.RETRY_UPLOAD_MISSION,
            message_class=MessageBuilder.WAYPOINT_MISSION_OPERATOR,
            message_data=None,
        )

        return_type = DJIError

        SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
        )

    # ------------------------ MISSION EXECUTION --------------------

    def startMission(self, callback=None, timeout=10):
        """Starts the uploaded mission"""

        checkParameters(callback=callback,
                        method_name="startMission", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.START_MISSION,
            message_class=MessageBuilder.WAYPOINT_MISSION_OPERATOR,
            message_data=None,
        )

        blocking = callback is None

        return_type = DJIError

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )

    def setAutoFlightSpeed(self, speed, callback=None, timeout=10):
        """Set the flight speed while the mission is executing automatically (without manual joystick speed input)"""

        checkParameters(
            callback=callback, method_name="setAutoFlightSpeed", timeout=timeout
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.SET_AUTO_FLIGHT_SPEED,
            message_class=MessageBuilder.WAYPOINT_MISSION_OPERATOR,
            message_data={"speed": speed},
        )

        return_type = DJIError

        SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
        )

    # ------------------------------ LISTENER ------------------------------
    def addListener(self, listener):
        """
        Add listener to listen for events

        Args:
            listener (WaypointMissionOperatorListener): An WaypointMissionOperatorListener instance
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.ADD_LISTENER,
            message_class=MessageBuilder.WAYPOINT_MISSION_OPERATOR,
            message_data={},
        )

        return_type = DJIError

        result = SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=None,
            timeout=10,
            return_type=return_type,
            listener=listener,
        )

        return result

    def removeListener(self, listener):
        """
        Remove waypoint mission operator listener

        Args:
            listener (WaypointMissionOperatorListener): An WaypointMissionOperatorListener instance
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.REMOVE_LISTENER,
            message_class=MessageBuilder.WAYPOINT_MISSION_OPERATOR,
            message_data={},
        )

        return_type = bool

        result = SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=None,
            timeout=10,
            return_type=return_type,
            blocking=True,
        )

        listener._close()

        return result
