import time
from dji_asdk_to_python.products.aircraft import Aircraft


APP_IP = "192.168.0.109"

drone = Aircraft(APP_IP)
fc = drone.getFlightController()

print(fc.startTakeoff())
time.sleep(5)
print(fc.startLanding())
