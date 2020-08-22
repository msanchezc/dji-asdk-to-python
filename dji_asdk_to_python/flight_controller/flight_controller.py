from dji_asdk_to_python.utils.message_builder import MessageBuilder
from dji_asdk_to_python.errors import DJIError

from dji_asdk_to_python.utils.shared import checkParameters
from dji_asdk_to_python.utils.socket_utils import SocketUtils
from dji_asdk_to_python.flight_controller.flight_controller_state import (
    FlightControllerState,
)
from dji_asdk_to_python.flight_controller.virtual_stick.control_mode import (
    VerticalControlMode,
)
from dji_asdk_to_python.flight_controller.virtual_stick.flight_control_data import (
    FlightControlData,
)


class FlightController:
    """
    This class contains components of the flight controller and provides methods to send different commands to the flight controller. This object is available from the Aircraft object.
    """

    def __init__(self, app_ip):
        """
        Args:
            - app_ip (str): Android device ip
        """
        self.app_ip = app_ip
        self._state_callbacks = {}

    def getState(self, callback=None, timeout=10):
        """
        Returns:
            [FlightControllerState]: the current state of flight controller.
        """

        checkParameters(callback=callback, method_name="getState", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_STATE,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=None,
        )

        return_type = FlightControllerState

        blocking = callback is None

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )

    def isConnected(self, timeout=1):
        """
        Gets boolean value from flight controller connection

        Args:
            - timeout (int): A timeout seconds time
        Returns:
            [boolean]: boolean value from flight controller connection.
        """

        checkParameters(callback=None, method_name="isConnected", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.IS_CONNECTED,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=None,
        )

        return_type = bool

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=None,
            timeout=timeout,
            return_type=return_type,
            blocking=True,
        )

    # -------------------------------- STATE UPDATES ------------------------------------

    def addStateCallback(self, callback):
        """
        Add callback function that updates the flight controller's current state data. This method is called 10 times per second.


        Args:
            callback (FlightControllerState.Callback): The execution callback with the execution result returned.
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.ADD_STATE_CALLBACK,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data={},
        )

        return_type = DJIError

        result = SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=None,
            timeout=10,
            return_type=return_type,
            listener=callback,
        )

        if result is None:
            # no news, good news
            self._state_callbacks[callback.uid] = callback

        return result

    def removeStateCallback(self, callback):
        """
        Removes callback function that updates the flight controller's current state data.

        Args:
            callback (FlightControllerState.Callback): The execution callback with the execution result returned.
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.REMOVE_STATE_CALLBACK,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data={},
        )

        return_type = DJIError

        result = SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=None,
            timeout=10,
            return_type=return_type,
            listener=callback,
        )

        if result is None:
            # no news, good news
            if isinstance(callback, FlightControllerState.Callback):
                print("removeStateCallback")
                callback.sock.close()  # Close client socket
                self._state_callbacks[callback.uid].sock = None
                self._state_callbacks[callback.uid].running = False
                self._state_callbacks[callback.uid] = None
                self._state_callbacks.pop(callback.uid, None)

        return result

    # -------------------------------- FLIGHT ACTIONS ------------------------------------
    def startTakeoff(self, callback=None, timeout=10):
        """
        Allow your aircraft to start take off

        Starts aircraft takeoff. Takeoff is considered complete when the aircraft is hovering 1.2 meters (4 feet) above the ground. Callback is called when aircraft crosses 0.5 meters (1.6 feet). If the motors are already on, this command cannot be executed.

        Args:
            - callback (function): An callback function with a simgle parameter of type CustomError
            - timeout (int): A timeout seconds time
        """
        checkParameters(callback=callback, method_name="startTakeoff", timeout=timeout)
        message = MessageBuilder.build_message(
            message_method=MessageBuilder.START_TAKEOFF,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=None,
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

    def startLanding(self, callback=None, timeout=10):
        """
        Allow your aircraft to start landing

        Starts auto-landing of the aircraft. Callback is called once aircraft begins to descend for auto-land.

        Args:
            - callback (function): An callback function with a simgle parameter of type CustomError
            - timeout (int): A timeout seconds time
        """
        checkParameters(callback=callback, method_name="startLanding", timeout=timeout)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.START_LANDING,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=None,
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

    # ---------------------------- END OF FLIGHT ACTIONS ---------------------------

    # ------------------------------ VIRTUAL STICK ----------------------------------
    def setVirtualStickModeEnabled(self, enabled, callback=None, timeout=10):
        """
        Allow your aircraft to enables/disables virtual stick control mode.

        By enabling virtual stick control mode, the aircraft can be controlled using sendVirtualStickFlightControlData. Not supported by Mavic Pro when using the WiFi connection.

        Args:
            - enabled (bool): True/False if you want to activate/deactivate virtual control
            - callback (function): An callback function with a simgle parameter of type CustomError
            - timeout (int): A timeout seconds time
        """
        checkParameters(
            callback=callback,
            method_name="isVirtualStickControlModeAvailable",
            timeout=timeout,
        )
        if not isinstance(enabled, bool):
            raise Exception("setVirtualStickModeEnabled: enabled must be boolean")

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.SET_VIRTUAL_STICK_CONTROL_MODE_ENABLED,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data={"enabled": str(enabled)},
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

    def getVirtualStickModeEnabled(self, callback=None, timeout=10):
        """
        Gets virtual stick mode status (enabled/disabled)

        Not supported by Mavic Pro when using the WiFi connection.

        Args:
            - callback (function): An callback function with a simgle parameter of type VirtualStickModeEnabled
            - timeout (int): A timeout seconds time
        """

        checkParameters(
            callback=callback, method_name="getVirtualStickModeEnabled", timeout=timeout
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_VIRTUAL_STICK_MODE_ENABLED,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=None,
        )

        return_type = bool

        blocking = callback is None

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )

    def sendVirtualStickFlightControlData(
        self, flight_control_data, callback=None, timeout=1
    ):
        """
        Sends flight control data using virtual stick commands.

        The isVirtualStickControlModeAvailable method must return true to use virtual stick commands. Virtual stick commands should be sent to the aircraft between 5 Hz and 25 Hz.

        Args:
            - flight_control_data (FlightControlData): A control data that contains all the virtual stick control data needed to move the aircraft in all directions.
            - callback (function): An callback function with a simgle parameter of type CustomError
            - timeout (int): A timeout seconds time
        """

        assert isinstance(flight_control_data, FlightControlData)
        flight_control_data = flight_control_data.__dict__
        checkParameters(
            callback=callback,
            method_name="sendVirtualStickFlightControlData",
            timeout=timeout,
        )
        message = MessageBuilder.build_message(
            message_method=MessageBuilder.SEND_VIRTUAL_STICK_FLIGHT_CONTROL_DATA,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=flight_control_data,
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

    def getVerticalControlMode(self, callback=None, timeout=10):
        """
        Gets the vertical control mode for virtual stick)

        CAUTION: It will be reset to VELOCITY when the flight controller is reconnected

        Args:
            - callback (function): An callback function with a simgle parameter of type VerticalControlMode
            - timeout (int): A timeout seconds time
        """

        checkParameters(
            callback=callback, method_name="getVerticalControlMode", timeout=timeout,
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_VERTICAL_CONTROL_MODE,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=None,
        )

        return_type = VerticalControlMode

        blocking = callback is None

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=blocking,
        )

    def setVerticalControlMode(self, vertical_control_mode, callback=None, timeout=10):
        """
        Sets whether virtual stick vertical controller changes aircraft's altitude or vertical velocity.

        Args:
            - vertical_control_mode (VerticalControlMode): Defines how vertical control values are interpreted by the aircraft.
            - callback (function): An callback function with a simgle parameter of type CustomError
            - timeout (int): A timeout seconds time
        """
        checkParameters(
            callback=callback, method_name="setVerticalControlMode", timeout=timeout,
        )

        assert isinstance(vertical_control_mode, VerticalControlMode)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.SET_VERTICAL_CONTROL_MODE,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data={"vertical_control_mode": vertical_control_mode.value},
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

    # ------------------------------- END OF VIRTUAL STICK METHODS--------------------------------

    # --------------------------------------- HOME -----------------------------------------
    def startGoHome(self, callback=None, timeout=10):
        """
        The aircraft will start to go home.

        The completion callback will return execution result once this method is invoked.

        Args:
            - callback (function): An callback function with a simgle parameter of type CustomError
            - timeout (int): A timeout seconds time
        """
        checkParameters(
            callback=callback, method_name="startGoHome", timeout=timeout,
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.START_GO_HOME,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=None,
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

    def cancelGoHome(self, callback=None, timeout=10):
        """
        The aircraft will stop going home and will hover in place.

        Args:
            - callback (function): An callback function with a simgle parameter of type CustomError
            - timeout (int): A timeout seconds time
        """
        checkParameters(
            callback=callback, method_name="cancelGoHome", timeout=timeout,
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.CANCEL_GO_HOME,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data=None,
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

    def getHomeLocation(self, callback=None, timeout=10):
        """Gets the home point of the aircraft."""
        checkParameters(
            callback=callback, method_name="getHomeLocation", timeout=timeout,
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.GET_HOME_LOCATION,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
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

    def setHomeLocation(self, homeLocation, callback=None, timeout=10):
        """
        Sets the home location of the aircraft.

        The home location is where the aircraft returns when commanded by startGoHome, when its signal is lost or when the battery is below the lowBatteryWarning threshold. The user should be careful setting a new home point location, as sometimes the product will not be under user control when returning home. A home location is valid if it is within 30m of one of the following:
            - initial take-off location
            - aircraft's current location
            - current mobile location with at least kCLLocationAccuracyNearestTenMeters accuracy level
            - current remote controller's location as shown by RC GPS.

        Args:
            - callback (function): An callback function with a simgle parameter of type CustomError
            - timeout (int): A timeout seconds time
        """
        checkParameters(
            callback=callback, method_name="setHomeLocation", timeout=timeout,
        )

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.SET_HOME_LOCATION,
            message_class=MessageBuilder.FLIGHT_CONTROLLER,
            message_data={"homeLocation": homeLocation},
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


# ----------------------------------- END OF HOME METHODS ----------------------------------
