from dji_asdk_to_python.products import Aircraft
import numpy as np
from dji_asdk_to_python.precision_landing.aproximation import ArucoAproximation
from dji_asdk_to_python.precision_landing.landing import ArucoLanding
from time import sleep
import os
from dji_asdk_to_python.errors import CustomError

APP_IP = "192.168.50.158"

aircraft = Aircraft(APP_IP)
camera_distortion = np.loadtxt("/home/luis/Documentos/psbposas/dji-asdk-to-python/examples/calibration/camera_distortion.txt", delimiter=",")
camera_matrix = np.loadtxt("/home/luis/Documentos/psbposas/dji-asdk-to-python/examples/calibration/camera_matrix.txt", delimiter=",")
stage1 = ArucoAproximation(drone_ip=APP_IP,camera_distortion=camera_distortion, camera_matrix=camera_matrix, marker_id=17, marker_size_cm=70)
stage2 = ArucoLanding(drone_ip=APP_IP,camera_distortion=camera_distortion, camera_matrix=camera_matrix, marker_id=62, marker_size_cm=12)
streaming_manager = aircraft.getLiveStreamManager()
rtp_manager = streaming_manager.getRTPManager()
rtp_manager.setWidth(1280)
rtp_manager.setHeigth(720)
result = rtp_manager.startStream()
print("result startStream %s" % result)
if isinstance(result, CustomError):
    raise Exception("%s" % result)

stage1.start(rtp_manager)

input("PRESS A KEY TO ENTER STAGE 2") #DBest notification of top platform deployment should be awaited here

stage2.start(rtp_manager) 

