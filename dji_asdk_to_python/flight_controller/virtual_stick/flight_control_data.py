class FlightControlData:
    def __init__(self, pitch=0, roll=0, yaw=0, vertical_throttle=0):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        self.vertical_throttle = vertical_throttle

    def __str__(self):
        return str(self.__dict__)

    def getPitch(self):
        return self.pitch

    def setPitch(self, pitch):
        self.pitch = pitch

    def getRoll(self):
        return self.roll

    def setRoll(self, roll):
        self.roll = roll

    def getYaw(self):
        return self.yaw

    def setYaw(self, yaw):
        self.yaw = yaw

    def getVerticalThrottle(self):
        return self.vertical_throttle

    def setVerticalThrottle(self, vertical_throttle):
        self.vertical_throttle = vertical_throttle
