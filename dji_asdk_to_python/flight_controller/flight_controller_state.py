import uuid


class FlightControllerState:
    """
    This class represents the current state of the flight controller.
    """

    class Callback:
        """
        Callback class that updates the flight controller's current state data. This method gets called 10 times per second after startUpdatingFlightControllerCurrentState is called.
        """

        def __init__(self, onUpdate):
            """
            Args:
                onUpdate ([function]): Called with a single arg of type FlightControllerState when the flight controller's current state data has been updated. This method is called 10 times per second.
            """
            assert callable(onUpdate)
            self.uid = uuid.uuid1()
            self.running = True
            self.onUpdate = onUpdate

    def __init__(self):
        self._are_motors_on = None
        self._is_flying = None
        self._aircraft_location = None
        self._aircraft_attitude = None
        self._attitude = None
        self._velocity_x = None
        self._velocity_y = None
        self._velocity_z = None
        self._go_home_execution_state = None
        self._flight_time_in_seconds = None
        self._flight_mode = None

    # -------------------------------- FLIGHT INFORMATION ------------------------------------

    def areMotorsOn(self):
        """
        Returns:
            [bool]: true if motors are on.
        """
        return self._are_motors_on

    def isFlying(self):
        """
        Returns:
            [bool]: true if aircraft is flying.
        """
        return self._is_flying

    def getAircraftLocation(self):
        """
        Gets the current location of the aircraft as a coordinate. nil if the location is invalid.
        Returns:
            [LocationCoordinate3D]: The current location of the aircraft as a coordinate.
        """
        return self._aircraft_location

    def getAttitude(self):
        """
        Gets the attitude of the aircraft, where the pitch, roll, and yaw values will be in the range of [-180, 180] degrees. If its pitch, roll, and yaw values are 0, the aircraft will be hovering level with a True North heading.
        Returns:
            [Attitude]: The attitude of the aircraft.
        """
        return self._aircraft_attitude

    def getVelocityX(self):
        """
        Current speed of the aircraft in the x direction, in meters per second, using the N-E-D (North-East-Down) coordinate system.
        Returns:
            [float]: A float value of the current speed of the aircraft in the x direction.
        """
        return self._velocity_x

    def getVelocityY(self):
        """
        Current speed of the aircraft in the y direction, in meters per second, using the N-E-D (North-East-Down) coordinate system.
        Returns:
            [float]: A float value of the current speed of the aircraft in the y direction.
        """
        return self._velocity_y

    def getVelocityZ(self):
        """
        Current speed of the aircraft in the z direction, in meters per second, using the N-E-D (North-East-Down) coordinate system.

        Returns:
            [float]: A float value of the current speed of the aircraft in the z direction.
        """
        return self._velocity_z

    def getFlightTimeInSeconds(self):
        """
        The accumulated flight time, in seconds, since the aircraft's motors were turned on.

        Returns:
            [int]: An int value of the flight time.
        """
        return self._flight_time_in_seconds

    # --------------------------------------- HOME ------------------------------------------------

    def getGoHomeExecutionState(self):
        """
        Current status of go-home execution.
        Returns:
            [GoHomeExecutionState]:	An enum value of GoHomeExecutionState.
        """
        return self._go_home_execution_state

    # --------------------------------------- FLIGHT MODE ------------------------------------------

    def getFlightMode(self):
        """
        Flight controller flight mode. For more info, see https://developer.dji.com/mobile-sdk/documentation/introduction/component-guide-remotecontroller.html#flight-mode
        Returns:
            [FlightMode]:	An enum value of FlightMode.
        """
        return self._flight_mode
