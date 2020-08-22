import logging
import threading

from dji_asdk_to_python.mission_control.\
    waypoint.waypoint_mission_operator_listener import (
        WaypointMissionOperatorListener,
        WaypointMissionUploadEvent,
        WaypointUploadProgress,
        WaypointMissionState,
        WaypointMissionExecutionEvent,
        WaypointExecutionProgress,
        WaypointMissionExecuteState,
    )

from dji_asdk_to_python.flight_controller.flight_controller_state import (
    FlightControllerState,
)


def process_waypoint_mission_operator_listener(listener, message):
    method = message["method"]
    if method == "onExecutionStart":
        onExecutionStart = listener.onExecutionStart
        onExecutionStart()
    elif method == "onExecutionFinish":
        dji_error = None
        onExecutionFinish = listener.onExecutionFinish
        onExecutionFinish(dji_error)
    elif method == "onUploadUpdate":
        onUploadUpdate = listener.onUploadUpdate

        def getProgress():
            progress = message["getProgress"]
            there_is_progress = progress["there_is_progress"]
            if there_is_progress:
                index = int(progress["uploadedWaypointIndex"])
                total_waypoint_count = int(progress["totalWaypointCount"])
                is_summary_uploaded = progress["isSummaryUploaded"]
                return WaypointUploadProgress(
                    index, total_waypoint_count, is_summary_uploaded
                )
            else:
                return None

        def getPreviousState():
            previous_state = message["getPreviousState"]
            return WaypointMissionState(previous_state)

        def getCurrentState():
            current_state = message["getCurrentState"]
            return WaypointMissionState(current_state)

        waypoint_mission_upload_event = WaypointMissionUploadEvent(
            getProgress, getPreviousState, getCurrentState
        )
        onUploadUpdate(waypoint_mission_upload_event)

    elif method == "onExecutionUpdate":
        onExecutionUpdate = listener.onExecutionUpdate

        def getProgress():
            progress = message["getProgress"]
            there_is_progress = progress["there_is_progress"]
            if there_is_progress:
                is_waypoint_reached = progress["isWaypointReached"]
                target_waypoint_index = int(progress["targetWaypointIndex"])
                total_waypoint_count = int(progress["totalWaypointCount"])
                execute_state = progress["executeState"]

                return WaypointExecutionProgress(
                    target_waypoint_index,
                    is_waypoint_reached,
                    total_waypoint_count,
                    WaypointMissionExecuteState(execute_state),
                )
            else:
                return None

        def getPreviousState():
            previous_state = message["getPreviousState"]
            return WaypointMissionState(previous_state)

        def getCurrentState():
            current_state = message["getCurrentState"]
            return WaypointMissionState(current_state)

        waypoint_mission_execution_event = WaypointMissionExecutionEvent(
            getProgress, getPreviousState, getCurrentState
        )
        onExecutionUpdate(waypoint_mission_execution_event)
    else:
        raise Exception("method listener not recognized")


def process_flight_controller_state_callback(listener, message):
    try:
        method = message["method"]
    except Exception as e:
        logging.error(message)
        logging.error("Exception %s " % e)
        return
    if method == "onUpdate":
        onUpdate = listener.onUpdate
        from dji_asdk_to_python.utils.process_message import (
            data_to_flight_controller_state
        )
        fcs = data_to_flight_controller_state(message)
        t = threading.Thread(target=onUpdate, args=[listener, fcs])
        t.start()

    else:
        raise Exception("method listener not recognized")


def process_message_listener(listener, message):
    if isinstance(listener, WaypointMissionOperatorListener):
        process_waypoint_mission_operator_listener(listener, message)
    elif isinstance(listener, FlightControllerState.Callback):
        process_flight_controller_state_callback(listener, message)
    else:
        raise Exception("listener not recognized")
