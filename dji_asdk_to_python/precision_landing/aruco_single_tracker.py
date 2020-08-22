"""
This demo calculates multiple things for different scenarios.
IF RUNNING ON A PI, BE SURE TO sudo modprobe bcm2835-v4l2
Here are the defined reference frames:
TAG:
                A y
                |
                |
                |tag center
                O---------> x
CAMERA:
                X--------> x
                | frame center
                |
                |
                V y
F1: Flipped (180 deg) tag frame around x axis
F2: Flipped (180 deg) camera frame around x axis
The attitude of a generic frame 2 respect to a frame 1 can obtained by calculating euler(R_21.T)
We are going to obtain the following quantities:
    > from aruco library we obtain tvec and Rct, position of the tag in camera frame and attitude of the tag
    > position of the Camera in Tag axis: -R_ct.T*tvec
    > Transformation of the camera, respect to f1 (the tag flipped frame): R_cf1 = R_ct*R_tf1 = R_cf*R_f
    > Transformation of the tag, respect to f2 (the camera flipped frame): R_tf2 = Rtc*R_cf2 = R_tc*R_f
    > R_tf1 = R_cf2 an symmetric = R_f
"""

import math
import numpy as np
import cv2
import itertools
import cv2.aruco as aruco


class ArucoSingleTracker:
    def __init__(self, camera_matrix, camera_distortion):

        self._camera_matrix = camera_matrix
        self._camera_distortion = camera_distortion

        # --- 180 deg rotation matrix around the x axis
        self._R_flip = np.zeros((3, 3), dtype=np.float32)
        self._R_flip[0, 0] = 1.0
        self._R_flip[1, 1] = -1.0
        self._R_flip[2, 2] = -1.0

        # --- Define the aruco dictionary
        self._aruco_dict = aruco.custom_dictionary_from(
            20, 4, aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        )

        self._parameters = aruco.DetectorParameters_create()

    def _rotationMatrixToEulerAngles(self, R):
        # Calculates rotation matrix to euler angles
        # The result is the same as MATLAB except the order
        # of the euler angles ( x and z are swapped ).

        def isRotationMatrix(R):
            Rt = np.transpose(R)
            shouldBeIdentity = np.dot(Rt, R)
            I = np.identity(3, dtype=R.dtype)
            n = np.linalg.norm(I - shouldBeIdentity)
            return n < 1e-6

        assert isRotationMatrix(R)

        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

        singular = sy < 1e-6

        if not singular:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0

        return np.array([x, y, z])

    def track(
        self, frame, id_to_find=None, marker_size=None,
    ):

        marker_found = False
        x = y = z = pitch_camera = x_camera = y_camera = z_camera = 0

        # -- Convert in gray scale
        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )  # -- remember, OpenCV stores color images in Blue, Green, Red

        # -- Find all the aruco markers in the image
        corners, ids, rejected = aruco.detectMarkers(
            image=gray,
            dictionary=self._aruco_dict,
            parameters=self._parameters,
            cameraMatrix=self._camera_matrix,
            distCoeff=self._camera_distortion,
        )
        pitch_marker, roll_marker, yaw_marker = None, None, None
        pitch_camera, roll_camera, yaw_camera = None, None, None

        planned_ids = []
        if ids is not None:
            planned_ids = list(itertools.chain(*ids))
        if id_to_find in planned_ids:
            index_id_to_find = planned_ids.index(id_to_find)
            marker_found = True
            # -- array of rotation and position of each marker in camera frame
            # -- rvec = [[rvec_1], [rvec_2], ...]    attitude of the marker respect to camera frame
            # -- tvec = [[tvec_1], [tvec_2], ...]    position of the marker in camera frame
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
                corners, marker_size, self._camera_matrix, self._camera_distortion
            )

            # -- Unpack the output
            rvec, tvec = rvecs[index_id_to_find][0], tvecs[index_id_to_find][0]

            x = tvec[0]
            y = tvec[1]
            z = tvec[2]

            # -- Obtain the rotation matrix tag->camera
            R_ct = np.matrix(cv2.Rodrigues(rvec)[0])
            R_tc = R_ct.T

            # -- Get the attitude in terms of euler 321 (Needs to be flipped first)
            (
                roll_marker,
                pitch_marker,
                yaw_marker,
            ) = self._rotationMatrixToEulerAngles(self._R_flip * R_tc)

            # -- Now get Position and attitude f the camera respect to the marker
            pos_camera = -R_tc * np.matrix(tvec).T
            x_camera = pos_camera[0]
            y_camera = pos_camera[1]
            z_camera = pos_camera[2]

            (
                roll_camera,
                pitch_camera,
                yaw_camera,
            ) = self._rotationMatrixToEulerAngles(self._R_flip * R_tc)

        if type(None) == type(yaw_marker):
            marker_found = False
            yaw_marker = 0

        if marker_found:
            roll_camera = math.degrees(roll_camera)
            yaw_camera = math.degrees(yaw_camera)
            pitch_camera = math.degrees(pitch_camera)
            roll_marker = math.degrees(roll_marker)
            yaw_marker = math.degrees(yaw_marker)
            pitch_marker = math.degrees(pitch_marker)
            x_camera = float(x_camera)
            y_camera = float(y_camera)
            z_camera = float(z_camera)

        result = (
            marker_found,
            x,
            y,
            z,
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
        )
        return result
