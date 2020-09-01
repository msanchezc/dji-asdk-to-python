import cv2
from dji_asdk_to_python.precision_landing.aruco_single_tracker import ArucoSingleTracker
from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.errors import CustomError
from dji_asdk_to_python.flight_controller.virtual_stick.flight_control_data import FlightControlData
from dji_asdk_to_python.flight_controller.flight_controller_state import FlightControllerState
from dji_asdk_to_python.precision_landing.PID import PID
import math


class ArucoAproximation:
    """
    Inits the Stage2 class

        Parameters:

        drone_ip (str) -> The IP of the drone
        camera_matrix (ndarray) -> The camera matrix of the drone's camera
        camera_distortion (ndarray) -> The camera distortion of the drone's camera
        marker_id (int) -> The ID of the aruco marker to be detected on the landing stage
        marker_size_cm (int) -> The size in CM of the aruco marker to be detected in the stage

    """

    def __init__(self, drone_ip, camera_matrix, camera_distortion, marker_id, marker_size_cm):
        self.aircraft = Aircraft(drone_ip)
        self.marker_id = marker_id
        self.marker_size_cm = marker_size_cm
        self.ast = ArucoSingleTracker(camera_distortion=camera_distortion, camera_matrix=camera_matrix)
        self.rtp_manager = self.aircraft.getLiveStreamManager().getRTPManager()

        self.p = 0.004
        self.i = 0.000005
        self.d = 0.0005

        self.pidx = PID(P=self.p, I=self.i, D=self.d)
        self.pidy = PID(P=self.p, I=self.i, D=self.d)
        self.pidz = PID(P=self.p, I=self.i, D=self.d)

        self.pidx.SetPoint = 0.0
        self.pidy.SetPoint = 0.0
        self.pidz.SetPoint = 300.0

        self.pidx.setSampleTime(0.1)
        self.pidy.setSampleTime(0.1)
        self.pidz.setSampleTime(0.1)

        self.yaw_margin = 15

    def start(self):
        self.rtp_manager.setWidth(1280)
        self.rtp_manager.setHeigth(720)
        self.rtp_manager.startStream()
        result = self.rtp_manager.startStream()
        print("result startStream %s" % result)
        if isinstance(result, CustomError):
            raise Exception("%s" % result)

        print("--------------------------------------- STAGE 1 --------------------------------------------------------")

        gimbal = self.aircraft.getGimbal()
        gimbal.rotate(-90, 0, 0)
        print("Gimbal set to -90 degrees")

        fc = self.aircraft.getFlightController()

        fc.setVirtualStickModeEnabled(True)
        fcd = FlightControlData()

        while True:
            fcd.setPitch(0)
            fcd.setYaw(0)
            fcd.setRoll(0)
            fcd.setVerticalThrottle(0)

            flight_controller_state = fc.getState()

            if isinstance(flight_controller_state, FlightControllerState):
                flying = flight_controller_state.isFlying()
                if not flying:
                    break

            frame = self.rtp_manager.getFrame()
            if frame is None:
                continue

            (
                marker_found,
                x_marker,
                y_marker,
                z_marker,
                x_camera,
                y_camera,
                z_camera,
                roll_marker,
                yaw_marker,
                pitch_marker,
                roll_marker,
                roll_camera,
                yaw_camera,
                pitch_camera,
            ) = self.ast.track(frame, self.marker_id, self.marker_size_cm)

            if marker_found:

                print("x_marker %s y_marker %s z_marker %s" % (x_marker, y_marker, z_marker))
                print("yaw_camera %s" % yaw_camera)

                if abs(yaw_camera) > self.yaw_margin:
                    print("CORRECTING YAW")
                    if yaw_camera < 0:
                        fcd.setYaw(10)
                    else:
                        fcd.setYaw(-10)

                self.pidx.update(x_marker)
                self.pidy.update(y_marker)
                self.pidz.update(z_marker)

                xoutput = self.pidx.output
                youtput = self.pidy.output
                zoutput = self.pidz.output

                print("X output:%s" % xoutput)
                print("Y output:%s" % youtput)
                print("Z output:%s" % zoutput)

                fcd.setPitch(youtput)
                fcd.setRoll(xoutput * -1)
                # math.sqrt(math.pow(x_marker, 2) + math.pow(y_marker, 2)) < 10 and Conditional of the following if
                if z_marker > 100 and abs(yaw_camera) < 20:
                    print("DESCENDING")
                    if abs(zoutput) > 4:
                        fcd.setVerticalThrottle(-2.7)
                    else:
                        fcd.setVerticalThrottle(zoutput)

                if z_marker < 320 and abs(yaw_camera) < 30 and math.sqrt(math.pow(x_marker, 2) + math.pow(y_marker, 2)) < 30:
                    print("STAGE 1 COMPLETED")
                    self.rtp_manager.stopStream()
                    break

                print("pitch %s, roll %s, yaw %s, throttle %s" % (fcd.getPitch(), fcd.getRoll(), fcd.getYaw(), fcd.getVerticalThrottle()))
                fc.sendVirtualStickFlightControlData(fcd)
                fcd.setPitch(0)
                fcd.setYaw(0)
                fcd.setRoll(0)
                fcd.setVerticalThrottle(0)

            cv2.imshow("frame", frame)

            if cv2.waitKey(100) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()

    def stop_streaming(self):
        self.rtp_manager.stopStream()
