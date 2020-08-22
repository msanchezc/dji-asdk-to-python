from dji_asdk_to_python.products import Aircraft
from dji_asdk_to_python.flight_controller.flight_controller_state import (
    FlightControllerState,
)


APP_IP = "192.168.0.109"

drone = Aircraft(APP_IP)
fc = drone.getFlightController()

flight_controller_state = fc.getState()

print("areMotorsOn %s " % flight_controller_state.areMotorsOn())
print("isFlying %s " % flight_controller_state.isFlying())
print("velocityX %s " % flight_controller_state.getVelocityX())
print("velocityY %s " % flight_controller_state.getVelocityY())
print("velocityZ %s " % flight_controller_state.getVelocityZ())

aircraft_location = flight_controller_state.getAircraftLocation()

print("getAltitude %s " % aircraft_location.getAltitude())
print("getLatitude %s " % aircraft_location.getLatitude())
print("getLongitude %s " % aircraft_location.getLongitude())

aircraft_attitude = flight_controller_state.getAttitude()

print("pitch %s " % aircraft_attitude.pitch)
print("roll %s " % aircraft_attitude.roll)
print("yaw %s " % aircraft_attitude.yaw)
print("GoHomeExecutionState %s" % flight_controller_state.getGoHomeExecutionState())
print("getFlightMode %s" % flight_controller_state.getFlightMode())
