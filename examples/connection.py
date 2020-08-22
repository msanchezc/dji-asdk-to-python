from dji_asdk_to_python.products.aircraft import Aircraft


APP_IP = "192.168.50.158"

drone = Aircraft(APP_IP)
fc = drone.getFlightController()

print("Aircraft connection status %s" % fc.isConnected())

