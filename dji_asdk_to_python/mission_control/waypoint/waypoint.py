class LocationCoordinate2D:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude


class WayPointTurnMode:
    CLOCKWISE = "CLOCKWISE"
    COUNTER_CLOCKWISE = "COUNTER_CLOCKWISE"


class Waypoint:
    MAX_ACTION_COUNT = 15
    MAX_ACTION_REPEAT_TIMES = 15
    MIN_ACTION_REPEAT_TIMES = 1
    MIN_ALTITUDE = -200.0
    MAX_ALTITUDE = 3.4028235e38
    MIN_HEADING = -180
    MAX_HEADING = 180
    MAX_ACTION_TIMEOUT = 999
    MIN_ACTION_TIMEOUT = 0
    MIN_CORNER_RADIUS = 0.2
    MAX_CORNER_RADIUS = 1000.0
    MIN_GIMBAL_PITCH = -135.0
    MAX_GIMBAL_PITCH = 45.0
    MIN_SPEED = 0.0
    MAX_SPEED = 15.0

    def __init__(self, latitude, longitude, altitude):
        self.locationCoordinate2D = LocationCoordinate2D(latitude, longitude)
        self.altitude = altitude
        self._heading = 0
        self._gimbal_pitch = 0
        self._turn_mode = WayPointTurnMode.CLOCKWISE
        self._action_repeat_times = 1
        self._action_timeout_in_seconds = 60
        self._corner_radius_in_meters = 0.2
        self._speed = 0

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def setGimbalPitch(self, gimbal_pitch):
        self._gimbal_pitch = self.clamp(
            gimbal_pitch, self.MIN_GIMBAL_PITCH, self.MAX_GIMBAL_PITCH)

    def setHeading(self, heading):
        self._heading = self.clamp(heading, self.MIN_HEADING, self.MAX_HEADING)

    def setSpeed(self, speed):
        self._speed = self.clamp(speed, self.MIN_SPEED, self.MAX_SPEED)

    def to_dict(self):
        locationdict = {
            'latitude': self.locationCoordinate2D.getLatitude(),
            'longitude': self.locationCoordinate2D.getLongitude()
        }

        mydict = {
            'locationcoordinate2d': locationdict,
            'altitude': self.altitude,
            'heading': self._heading,
            'gimbal_pitch': self._gimbal_pitch,
            'turn_mode': self._turn_mode,
            'action_repeat_times': self._action_repeat_times,
            'action_timeout_in_seconds': self._action_timeout_in_seconds,
            'corner_radius_in_meters': self._corner_radius_in_meters,
            'speed': self._speed
        }

        return mydict
