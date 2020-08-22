import time
from dji_asdk_to_python.products.aircraft import Aircraft


APP_IP = "192.168.0.109"

drone = Aircraft(APP_IP)
gimbal = drone.getGimbal()


for i in range(10):
    print("iteration %s" % i)
    if i % 2 == 0:
        gimbal.rotate(pitch=-90, roll=0, yaw=0)
    else:
        gimbal.rotate(pitch=0, roll=0, yaw=0)
    time.sleep(2)
