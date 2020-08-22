import enum
import socket


class WaypointMissionState(enum.Enum):
    """
    All the possible state of WaypointMissionOperator.
        - NOT_SUPPORTED: The connected product does not support waypoint mission.
        - READY_TO_UPLOAD: The aircraft is ready to upload a mission.
        - UPLOADING: The uploading is started successfully. Detail information for each waypoint is being uploaded one by one.
        - READY_TO_EXECUTE: Waypoint mission is uploaded completely and the aircraft is ready to start the execution.
        - EXECUTING: The execution is started successfully.
        - EXECUTION_PAUSED: Waypoint mission is paused successfully. User can call resumeMission to continue the execution.
        - DISCONNECTED: The connection between the mobile device, remote controller and aircraft is broken.
        - RECOVERING: The connection between the mobile device, remote controller and aircraft is built-up. The operator is synchronizing the state from the aircraft.
        - UNKNOWN: The state of the operator is unknown. It is the initial state when the operator is just created.

    """

    NOT_SUPPORTED = "NOT_SUPPORTED"
    READY_TO_UPLOAD = "READY_TO_UPLOAD"
    UPLOADING = "UPLOADING"
    READY_TO_EXECUTE = "READY_TO_EXECUTE"
    EXECUTING = "EXECUTING"
    EXECUTION_PAUSED = "EXECUTION_PAUSED"
    DISCONNECTED = "DISCONNECTED"
    RECOVERING = "RECOVERING"
    UNKNOWN = "UNKNOWN"


class WaypointMissionExecuteState(enum.Enum):
    """
    Current waypoint mission state.
        - INITIALIZING:	Waypoint mission is initializing, which means the mission has started and the aircraft is going to the first waypoint.
        - MOVING: Aircraft is currently moving toward the mission's next waypoint. This happens when the WaypointMissionFlightPathMode is set to NORMAL.
        - CURVE_MODE_MOVING: Aircraft is currently moving. This happens when the WaypointMissionFlightPathMode is set to CURVED.
        - CURVE_MODE_TURNING: Aircraft is currently turning. This happens when the WaypointMissionFlightPathMode is set to CURVED.
        - BEGIN_ACTION: Aircraft has reached a waypoint, has rotated to the new heading and is now processing actions. This state will be called before the waypoint actions starts executing and will occur for each waypoint action.
        - DOING_ACTION: Aircraft is at a waypoint and is executing an action.
        - FINISHED_ACTION: Aircraft is at a waypoint and has finished executing the current waypoint action. This state occurs once for each waypoint action.
        - RETURN_TO_FIRST_WAYPOINT: Aircraft has returned to the first waypoint. This happens when the getFinishedAction is set to RETURN_TO_FIRST_WAYPOINT.
        - PAUSED: The mission is currently paused by the user.
    """

    INITIALIZING = "INITIALIZING"
    MOVING = "MOVING"
    CURVE_MODE_MOVING = "CURVE_MODE_MOVING"
    CURVE_MODE_TURNING = "CURVE_MODE_TURNING"
    BEGIN_ACTION = "BEGIN_ACTION"
    DOING_ACTION = "DOING_ACTION"
    FINISHED_ACTION = "FINISHED_ACTION"
    RETURN_TO_FIRST_WAYPOINT = "RETURN_TO_FIRST_WAYPOINT"
    PAUSED = "PAUSED"


class WaypointUploadProgress:
    """
    The upload progress of the waypoint mission operator.
    """

    def __init__(self, uploadedWaypointIndex, totalWaypointCount, isSummaryUploaded):
        """
        Args:
            - uploadedWaypointIndex (int): The index of the last uploaded waypoint. Information for each waypoint is uploaded one by one in ascending order. If no waypoint has been uploaded, the value will be -1.
            - totalWaypointCount (int): The total count of waypoints in the waypoint mission.
            - isSummaryUploaded (bool): The waypoint mission operator has uploaded the the mission's summary (information except waypoints).
        """
        assert isinstance(uploadedWaypointIndex, int) and isinstance(totalWaypointCount, int) and isinstance(isSummaryUploaded, bool)
        self.uploadedWaypointIndex = uploadedWaypointIndex
        self.totalWaypointCount = totalWaypointCount
        self.isSummaryUploaded = isSummaryUploaded


class WaypointMissionUploadEvent:
    """
    The upload event of a waypoint mission.
    """

    def __init__(self, getProgress, getPreviousState, getCurrentState):
        """
        Args:
            - getProgress (function): A function that returns an instance of type WaypointUploadProgress, upload progress of the mission. It is null if there is an error during upload.
            - getPreviousState (function): A function that returns previous state of the operator of type WaypointMissionState.
            - getCurrentState (function): A function that returns current state of the operator of type WaypointMissionState.
        """
        assert callable(getProgress) and callable(getPreviousState) and callable(getCurrentState)
        self.getProgress = getProgress
        self.getPreviousState = getPreviousState
        self.getCurrentState = getCurrentState


class WaypointExecutionProgress:
    """
    The mission execution progress of the waypoint mission operator.
    """

    def __init__(
        self, targetWaypointIndex, isWaypointReached, totalWaypointCount, executeState
    ):
        """
        Args:
            - targetWaypointIndex (int): Index of the waypoint for the next mission to which the aircraft will proceed.
            - isWaypointReached (bool): YES when the aircraft reaches a waypoint. After the waypoint actions and heading change is complete, the targetWaypointIndex will increment and this property will become NO.
            - totalWaypointCount (int): The total count of waypoints in the waypoint mission.
            - executeState (WaypointMissionExecuteState): Current execution state of the aircraft.
        """
        assert isinstance(targetWaypointIndex, int)
        assert isinstance(totalWaypointCount, int)
        assert isinstance(isWaypointReached, bool)
        assert isinstance(executeState, WaypointMissionExecuteState)

        self.targetWaypointIndex = targetWaypointIndex
        self.totalWaypointCount = totalWaypointCount
        self.isWaypointReached = isWaypointReached
        self.executeState = executeState


class WaypointMissionExecutionEvent:
    """
    The execution event of a waypoint mission.
    """

    def __init__(self, getProgress, getPreviousState, getCurrentState):
        """
        Args:
            - getProgress (function): A function that returns an instance of type WaypointExecutionProgress, execution progress of the mission. It is null if there is an error during the execution.
            - getPreviousState (function): A function that returns previous state of the operator of type WaypointMissionState.
            - getCurrentState (function): A function that returns current state of the operator of type WaypointMissionState.
        """
        assert callable(getProgress)
        assert callable(getPreviousState)
        assert callable(getCurrentState)

        self.getProgress = getProgress
        self.getPreviousState = getPreviousState
        self.getCurrentState = getCurrentState


class WaypointMissionOperatorListener:
    """
    Listener interface for Waypoint mission operator events.
    """

    def __init__(
        self,
        onUploadUpdate,
        onDownloadUpdate,
        onExecutionStart,
        onExecutionUpdate,
        onExecutionFinish,
    ):
        """
        Args:
            - onUploadUpdate (function): A function with a single parameter of type WaypointMissionUploadEvent that is called when an upload event happens.
            - onDownloadUpdate (function): A function with a single parameter of type WaypointMissionDownloadEvent that is called when an upload event happens.
            - onExecutionStart (function): A function that is called when the waypoint mission starts.
            - onExecutionUpdate (function): A function with a single parameter of type WaypointMissionExecutionEvent that is called when there is an execution update for the waypoint mission operator.
            - onExecutionFinish (function): A function that is called when the waypoint mission ends.
        """
        assert callable(onUploadUpdate)
        assert callable(onDownloadUpdate)
        assert callable(onExecutionStart)
        assert callable(onExecutionUpdate)
        assert callable(onExecutionFinish)

        self.onUploadUpdate = onUploadUpdate
        self.onDownloadUpdate = onDownloadUpdate
        self.onExecutionStart = onExecutionStart
        self.onExecutionUpdate = onExecutionUpdate
        self.onExecutionFinish = onExecutionFinish

        self.running = False
        self.sock = None

    def _close(self):
        self.running = False
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
