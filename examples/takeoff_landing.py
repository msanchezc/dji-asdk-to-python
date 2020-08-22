from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.flight_controller.flight_controller_state import FlightControllerState
from dji_asdk_to_python.flight_controller.flight_mode import FlightMode

APP_IP = "YOUR_AIRCRAFT_IP"

drone = Aircraft(APP_IP)
fc = drone.getFlightController()

print(fc.startTakeoff())

while True:
    flight_controller_state = fc.getState()
    if not isinstance(flight_controller_state, FlightControllerState):
        continue

    flight_mode = flight_controller_state.getFlightMode()
    if flight_controller_state.isFlying() and flight_mode != FlightMode.AUTO_TAKEOFF:
        break

print(fc.startLanding())
