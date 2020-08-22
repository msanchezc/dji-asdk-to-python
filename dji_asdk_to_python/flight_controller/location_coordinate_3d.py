class LocationCoordinate3D:
    """
    This is a structure for presenting the location, latitude, longitude, altitude.
    """

    def __init__(self, latitude, longitude, altitude):
        """
        Args:
            latitude ([float]): Latitude in degrees
            longitude ([float]): Longitude in degrees
            altitude ([float]): Altitude in meters
        """
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def getLatitude(self):
        """
        Returns:
            [float]: Returns the latitude.
        """
        return self.latitude

    def getLongitude(self):
        """
        Returns:
            [float]: Returns the longitude.
        """
        return self.longitude

    def getAltitude(self):
        """
        Returns the relative altitude of the aircraft relative to take off location, measured by barometer, in meters.

        Returns:
            [float]: A float value of the relative altitude of the aircraft relative to take off location.
        """
        return self.altitude
