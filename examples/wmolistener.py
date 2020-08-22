from dji_asdk_to_python.mission_control.waypoint import WaypointMissionOperator
from dji_asdk_to_python.mission_control.waypoint import WaypointMissionState
from dji_asdk_to_python.mission_control.waypoint import WaypointMissionOperatorListener


""" 
This example tests:
    - Waits for all the waypoints of a mission to be uploaded
"""

APP_IP = "192.168.0.180"

wpmoperator = WaypointMissionOperator(app_ip=APP_IP)
wpmolistener = None

def onUploadUpdate(waypoint_mission_upload_event):
    progress = waypoint_mission_upload_event.getProgress()
    current_state = waypoint_mission_upload_event.getCurrentState()
    previous_state = waypoint_mission_upload_event.getPreviousState()
    print("---------------------------------")
    if progress is not None:
        print("uploadedWaypointIndex: %s" % progress.uploadedWaypointIndex)
        print("totalWaypointCount: %s " % progress.totalWaypointCount)
        print("isSummaryUploaded: %s" % progress.isSummaryUploaded)
    print("getCurrentState: %s" % current_state)
    print("getPreviousState: %s" % previous_state)
    print("---------------------------------")

    if current_state == WaypointMissionState.READY_TO_EXECUTE:
        print("Current state is READY_TO_EXECUTE")
        result = wpmoperator.startMission()
        print("startMission result %s" % result)
        # wpmoperator.removeListener(wpmolistener)

def onDownloadUpdate():
    pass

def onExecutionStart():
    print("Mission begins to run")

def onExecutionUpdate(waypoint_mission_execution_event):
    progress = waypoint_mission_execution_event.getProgress()
    current_state = waypoint_mission_execution_event.getCurrentState()
    previous_state = waypoint_mission_execution_event.getPreviousState()
    print("---------------------------------")
    if progress is not None:
        print("isWaypointReached: %s" % progress.isWaypointReached)
        print("targetWaypointIndex: %s " % progress.targetWaypointIndex)
        print("totalWaypointCount: %s " % progress.totalWaypointCount)
        print("executeState: %s" % progress.executeState)
    print("getCurrentState: %s" % current_state)
    print("getPreviousState: %s" % previous_state)
    print("---------------------------------")

    if current_state == WaypointMissionState.EXECUTING:
        print("Current state is EXECUTING")

def onExecutionFinish(dji_error):
    print("Mission finished with error %s" % dji_error)
    wpmoperator.removeListener(wpmolistener)

wpmolistener = WaypointMissionOperatorListener(
    onUploadUpdate,
    onDownloadUpdate,
    onExecutionStart,
    onExecutionUpdate,
    onExecutionFinish,
)
result = wpmoperator.addListener(wpmolistener)
print("Listener result %s" % result)
