class WaypointMission:
    def __init__(self, builder):
        self.builder = builder.__dict__

    class Builder:
        def __init__(self):
            pass

        def setWaypointCount(self, waypoint_count):
            self.waypoint_count = waypoint_count

        def setMaxFlightSpeed(self, max_flight_speed):
            self.max_flight_speed = max_flight_speed

        def setAutoFlightSpeed(self, auto_flight_speed):
            self.auto_flight_speed = auto_flight_speed

        def setWaypointList(self, waypoint_list):
            self.waypoint_list = []
            for waypoint in waypoint_list:
                self.waypoint_list.append(waypoint.to_dict())

        def setMissionID(self, mission_id):
            self.mission_id = mission_id

        def setRepeatTimes(self, repeat_times):
            self.repeat_times = repeat_times

        def setGimbalPitchRotationEnabled(self, gimbal_pitch_rotation_enabled):
            self.gimbal_pitch_rotation_enabled = gimbal_pitch_rotation_enabled

        def setExitMissionOnRCSignalLostEnabled(self, exit_mission_on_rc_signal_lost_enabled):
            self.exit_mission_on_rc_signal_lost_enabled = exit_mission_on_rc_signal_lost_enabled

        def setGotoFirstWaypointMode(self, waypoint_mission_go_to_waypoint_mode):
            self.waypoint_mission_go_to_waypoint_mode = waypoint_mission_go_to_waypoint_mode

        def setFlightPathMode(self, waypoint_mission_flightpath_mode):
            self.waypoint_mission_flightpath_mode = waypoint_mission_flightpath_mode

        def setHeadingMode(self, waypoint_mission_heading_mode):
            self.waypoint_mission_heading_mode = waypoint_mission_heading_mode

        def setFinishedAction(self, waypoint_mission_finished_action):
            self.waypoint_mission_finished_action = waypoint_mission_finished_action
