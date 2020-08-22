import time
from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.flight_controller.virtual_stick.flight_control_data import FlightControlData
from dji_asdk_to_python.flight_controller.virtual_stick.control_mode import VerticalControlMode


APP_IP = "YOUR_AIRCRAFT_IP"

drone = Aircraft(APP_IP)
fc = drone.getFlightController()
fc.setVirtualStickModeEnabled(True)
vsm = fc.getVirtualStickModeEnabled()
print("VirtualStickModeEnabled is %s" % vsm)

fcd = FlightControlData(pitch=0, roll=0, yaw=0, vertical_throttle=1)
fc.startTakeoff()
time.sleep(7)  # waits until takeoff completes

# Throttle test
for i in range(2):
    fcd.setVerticalThrottle(fcd.getVerticalThrottle() * -1)
    print(fcd)
    time.sleep(1)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(2)
    fcd.setVerticalThrottle(fcd.getVerticalThrottle() * -1)
    print(fcd)
    time.sleep(1)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(2)

# Yaw test
fcd.setVerticalThrottle(0)
fcd.setYaw(20)
for i in range(2):
    fcd.setYaw(fcd.getYaw() * -1)
    print(fcd)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(2)
    fcd.setYaw(fcd.getYaw() * -1)
    print(fcd)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(2)

# Pitch test
fcd.setYaw(0)
fcd.setPitch(1)
for i in range(2):
    fcd.setPitch(fcd.getPitch() * -1)
    print(fcd)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(2)
    fcd.setPitch(fcd.getPitch() * -1)
    print(fcd)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(2)

# Roll test
fcd.setPitch(0)
fcd.setRoll(1)
for i in range(2):
    fcd.setRoll(fcd.getRoll() * -1)
    print(fcd)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(2)
    fcd.setRoll(fcd.getRoll() * -1)
    print(fcd)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(2)

fc.setVerticalControlMode(VerticalControlMode.VELOCITY)

# Using callback does not block execution


def printVerticalMode(vertical_mode):
    print("aircraft vertical mode is %s" % vertical_mode)


fc.getVerticalControlMode(callback=printVerticalMode)
fc.setVerticalControlMode(VerticalControlMode.POSITION)
fc.getVerticalControlMode(callback=printVerticalMode)

fcd.setYaw(0)
fcd.setRoll(0)
fcd.setPitch(0)

for i in range(3):
    fcd.setVerticalThrottle(3)
    print(fcd)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(3)
    fcd.setVerticalThrottle(15)
    print(fcd)
    for i in range(10):
        fc.sendVirtualStickFlightControlData(fcd)
        time.sleep(0.1)
    time.sleep(3)

print(fc.getVerticalControlMode(callback=printVerticalMode))

fc.setVirtualStickModeEnabled(False)
fc.startLanding()
