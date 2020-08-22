import time
from dji_asdk_to_python.mission_control.waypoint import Waypoint
from dji_asdk_to_python.mission_control.waypoint import WaypointMissionOperator
from dji_asdk_to_python.mission_control.waypoint import WaypointMission
from dji_asdk_to_python.products import Aircraft
from dji_asdk_to_python.mission_control.waypoint import (
    WaypointMissionGoToWaypointMode,
    WaypointMissionFinishedAction,
    WaypointMissionFlighPathMode,
    WaypointMissionHeadingMode,
)
import json

APP_IP = "192.168.0.109"

drone = Aircraft(app_ip=APP_IP)

fc = drone.getFlightController()

wp1 = Waypoint(3.3312591288067144, -76.53951935644871, 45)
wp2 = Waypoint(3.3311239061197466, -76.5389064716888, 45)
wp3 = Waypoint(3.3310315262535997, -76.53939865704304, 45)

wp2.setGimbalPitch(-90)
wp2.setSpeed(5)

wp3.setGimbalPitch(-90)
wp3.setSpeed(10)

def uploadMissionCallback(result):
    print(result)

fc.startTakeoff()
time.sleep(5)

waypoints = [wp1, wp2, wp3]
builder = WaypointMission.Builder()

builder.setWaypointList(waypoint_list=waypoints)
builder.setWaypointCount(waypoint_count=len(waypoints))
builder.setMaxFlightSpeed(15)
builder.setAutoFlightSpeed(15)
builder.setMissionID(0)
builder.setRepeatTimes(1)
builder.setGimbalPitchRotationEnabled(True)
builder.setExitMissionOnRCSignalLostEnabled(False)
builder.setGotoFirstWaypointMode(WaypointMissionGoToWaypointMode.SAFELY)
builder.setFlightPathMode(WaypointMissionFlighPathMode.NORMAL)
builder.setHeadingMode(WaypointMissionHeadingMode.AUTO)
builder.setFinishedAction("GO_HOME")

mission = WaypointMission(builder=builder)

wpmoperator = WaypointMissionOperator(app_ip=APP_IP)

wpmoperator.loadMission(mission=mission)
time.sleep(3)
wpmoperator.uploadMission()
time.sleep(3)

result = wpmoperator.startMission()

print(result)
