from dji_asdk_to_python.flight_controller.flight_controller import (
    FlightController
)
from dji_asdk_to_python.gimbal.gimbal import Gimbal
from dji_asdk_to_python.sdk_manager.live_stream_manager import (
    LiveStreamManager
)


class Aircraft:
    def __init__(self, app_ip):
        self.app_ip = app_ip

    def getGimbal(self):
        return Gimbal(self.app_ip)

    def getFlightController(self):
        return FlightController(self.app_ip)

    def getLiveStreamManager(self):
        return LiveStreamManager(self.app_ip)
