import enum


class FlightMode(enum.Enum):
    """
    Flight controller flight modes. For more information, see http://wiki.dji.com/en/index.php/Phantom_3_Professional-Aircraft.
        - MANUAL: Manual mode.
        - ATTI: Attitude mode.
        - ATTI_COURSE_LOCK: Attitude course lock mode.
        - ATTI_HOVER: Attitude hover mode.
        - GPS_ATTI: GPS Attitude mode.
        - GPS_COURSE_LOCK: GPS course lock mode.
        - GPS_HOME_LOCK: GPS Home mode.
        - GPS_HOT_POINT: GPS hotpoint mode.
        - ASSISTED_TAKEOFF:	Assisted takeoff mode.
        - AUTO_TAKEOFF:	Auto takeoff mode.
        - AUTO_LANDING:	Auto landing mode.
        - ATTI_LANDING:	Attitude landing mode.
        - GPS_WAYPOINT:	GPS waypoint mode.
        - GO_HOME: Go home mode.
        - JOYSTICK:	Joystick mode.
        - ATTI_LIMITED:	Attitude limited mode.
        - DRAW:	Draw mode.
        - GPS_ATTI_WRISTBAND: GPS attitude limited mode.
        - GPS_FOLLOW_ME: GPS follow me mode.
        - ACTIVE_TRACK:	ActiveTrack mode.
        - TAP_FLY: TapFly mode.
        - GPS_SPORT: Sport mode.
        - GPS_NOVICE: GPS Novice mode.
        - UNKNOWN: The main controller flight mode is unknown.
        - CONFIRM_LANDING: Confirm landing mode.
        - TERRAIN_FOLLOW: The aircraft should move following the terrain.
        - TRIPOD: Tripod mode.
        - TRACK_SPOTLIGHT: Active track mode, corresponds to Spotlight active track mode.
        - MOTORS_JUST_STARTED: The motors are just started.
    """

    MANUAL = "MANUAL"
    ATTI = "ATTI"
    ATTI_COURSE_LOCK = "ATTI_COURSE_LOCK"
    ATTI_HOVER = "ATTI_HOVER"
    GPS_ATTI = "GPS_ATTI"
    GPS_COURSE_LOCK = "GPS_COURSE_LOCK"
    GPS_HOME_LOCK = "GPS_HOME_LOCK"
    GPS_HOT_POINT = "GPS_HOT_POINT"
    ASSISTED_TAKEOFF = "ASSISTED_TAKEOFF"
    AUTO_TAKEOFF = "AUTO_TAKEOFF"
    AUTO_LANDING = "AUTO_LANDING"
    ATTI_LANDING = "ATTI_LANDING"
    GPS_WAYPOINT = "GPS_WAYPOINT"
    GO_HOME = "GO_HOME"
    JOYSTICK = "JOYSTICK"
    ATTI_LIMITED = "ATTI_LIMITED"
    DRAW = "DRAW"
    GPS_ATTI_WRISTBAND = "GPS_ATTI_WRISTBAND"
    GPS_FOLLOW_ME = "GPS_FOLLOW_ME"
    ACTIVE_TRACK = "ACTIVE_TRACK"
    TAP_FLY = "TAP_FLY"
    GPS_SPORT = "GPS_SPORT"
    GPS_NOVICE = "GPS_NOVICE"
    CONFIRM_LANDING = "CONFIRM_LANDING"
    TERRAIN_FOLLOW = "TERRAIN_FOLLOW"
    TRIPOD = "TRIPOD"
    TRACK_SPOTLIGHT = "TRACK_SPOTLIGHT"
    MOTORS_JUST_STARTED = "MOTORS_JUST_STARTED"
    UNKNOWN = "UNKNOWN"
