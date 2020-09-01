import cv2, time

from dji_asdk_to_python.products.aircraft import Aircraft
from dji_asdk_to_python.errors import CustomError


APP_IP = "192.168.0.109"
RTMP_SERVER_IP = "192.168.0.136" # "192.168.0.136"
LIVE_URL = "rtmp://%s:1935/live/apolo" % RTMP_SERVER_IP

STREAMING_DURATION = 100  # seconds

aircraft = Aircraft(APP_IP)
streaming_manager = aircraft.getLiveStreamManager()
rtmp_manager = streaming_manager.getRTMPManager()

is_streaming = rtmp_manager.isStreaming()

while is_streaming:
    result = rtmp_manager.stopStream()
    is_streaming = rtmp_manager.isStreaming()

rtmp_manager.setLiveUrl(LIVE_URL)

result = rtmp_manager.startStream()
print("result startStream %s" % result)


input("Press a key to stop streaming")

result = rtmp_manager.stopStream()
print("result stopStream %s" % result)
