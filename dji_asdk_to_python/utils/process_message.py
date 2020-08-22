from .message_builder import MessageBuilder
from dji_asdk_to_python.flight_controller.flight_controller_state import FlightControllerState
from dji_asdk_to_python.flight_controller.location_coordinate_3d import LocationCoordinate3D
from dji_asdk_to_python.flight_controller.go_home_execution_state import GoHomeExecutionState
from dji_asdk_to_python.flight_controller.flight_mode import FlightMode
from dji_asdk_to_python.flight_controller.attitude import Attitude
from dji_asdk_to_python.flight_controller.virtual_stick.control_mode import (
    VerticalControlMode,
)


from dji_asdk_to_python.errors import (
    JsonError,
    DJIError,
    BridgeIOError,
    ModuleNotAvailableError,
)


def data_to_flight_controller_state(data):
    message = data
    are_motors_on = message["areMotorsOn"]
    is_flying = message["isFlying"]
    velocity_x = message["velocityX"]
    velocity_y = message["velocityY"]
    velocity_z = message["velocityZ"]
    flight_time_in_seconds = message["flight_time_in_seconds"]

    aircraft_location = message["getAircraftLocation"]
    latitude = aircraft_location["getLatitude"]
    longitude = aircraft_location["getLongitude"]
    altitude = aircraft_location["getAltitude"]

    aircraft_attitude = message["getAttitude"]
    pitch = aircraft_attitude["pitch"]
    roll = aircraft_attitude["roll"]
    yaw = aircraft_attitude["yaw"]

    go_home_execution_state = message["go_home_execution_state"]
    flight_mode = message["flight_mode"]

    fcs = FlightControllerState()
    fcs._aircraft_location = LocationCoordinate3D(
        latitude=latitude, longitude=longitude, altitude=altitude
    )
    fcs._aircraft_attitude = Attitude(pitch=pitch, roll=roll, yaw=yaw)
    fcs._is_flying = is_flying
    fcs._are_motors_on = are_motors_on
    fcs._velocity_x = velocity_x
    fcs._velocity_y = velocity_y
    fcs._velocity_z = velocity_z
    fcs._go_home_execution_state = GoHomeExecutionState(go_home_execution_state)
    fcs._flight_time_in_seconds = flight_time_in_seconds
    fcs._flight_mode = FlightMode(flight_mode)
    return fcs


def process_return_type(server_message, return_type):
    if return_type == FlightControllerState:
        result = data_to_flight_controller_state(server_message["data"])
    elif return_type == bool:
        response = server_message[MessageBuilder.DATA][MessageBuilder.BOOL]
        result = response
    elif return_type == int:
        response = server_message[MessageBuilder.DATA][MessageBuilder.INT]
        result = response
    elif return_type == VerticalControlMode:
        response = server_message[MessageBuilder.DATA][
            MessageBuilder.VERTICAL_CONTROL_MODE
        ]

        if response == "VELOCITY":
            result = VerticalControlMode(0)
        elif response == "POSITION":
            result = VerticalControlMode(1)
    elif return_type == DJIError:
        result = None
    elif return_type is None:
        result = server_message["data"]
    else:
        raise Exception("Return type %s can not be processed" % return_type)
    return result


def process_error_message(server_message):
    if server_message[MessageBuilder.ERROR_TYPE] == MessageBuilder.DJI_ERROR:
        result = DJIError(
            server_message[DJIError.ERROR_CODE], server_message[DJIError.DESCRIPTION],
        )
    elif (
        server_message[MessageBuilder.ERROR_TYPE] == MessageBuilder.MODULE_NOT_AVAILABLE
    ):
        result = ModuleNotAvailableError(server_message[DJIError.DESCRIPTION])
    elif server_message[MessageBuilder.ERROR_TYPE] == MessageBuilder.JSON_ERROR:
        result = JsonError(server_message[DJIError.DESCRIPTION])
    elif server_message[MessageBuilder.ERROR_TYPE] == MessageBuilder.IOERROR:
        result = BridgeIOError(server_message[DJIError.DESCRIPTION])
    return result
