from dji_asdk_to_python.mission_control.waypoint.waypoint import LocationCoordinate2D
from dji_asdk_to_python.products import Aircraft
import time

app_ip = "192.168.0.174"


def startGoHomeCallback(data):
    print("callback startGoHomeCallback is executed")
    print(data)


def cancelGoHomeCallback(data):
    print("callback cancelGoHomeCallback is executed")
    print(data)


def setHomeLocationCallback(data):
    print("callback setHomeLocationCallback is executed")
    print(data)


def getHomeLocationCallback(data):
    print("callback getHomeLocationCallback is executed")
    print(data)


drone = Aircraft(app_ip)
fc = drone.getFlightController()

homeLocation = LocationCoordinate2D(3.3310794794873844, -76.53948434110453)

fc.getHomeLocation(getHomeLocationCallback)
fc.startGoHome(startGoHomeCallback)
time.sleep(45)
fc.cancelGoHome(cancelGoHomeCallback)
time.sleep(5)
fc.getHomeLocation(getHomeLocationCallback)
fc.setHomeLocation(homeLocation.__dict__, setHomeLocationCallback)
fc.getHomeLocation(getHomeLocationCallback)
time.sleep(5)
fc.startGoHome(startGoHomeCallback)
