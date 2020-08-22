class Attitude:
    """
    This is a structure for presenting the attitude, pitch, roll, yaw.
    """

    def __init__(self, pitch, roll, yaw):
        """
        Args:
            pitch ([float]): Pitch in degrees
            roll ([float]): Roll in degrees
            yaw ([float]): Yaw in meters
        """
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
