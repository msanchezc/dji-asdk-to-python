import cv2, time

from dji_asdk_to_python.products import Aircraft
from dji_asdk_to_python.errors import CustomError


APP_IP = "192.168.50.158"
STREAMING_DURATION = 1000  # seconds

aircraft = Aircraft(APP_IP)
streaming_manager = aircraft.getLiveStreamManager()
rtp_manager = streaming_manager.getRTPManager()
rtp_manager.setWidth(1920)
rtp_manager.setHeigth(1080)
result = rtp_manager.startStream()
print("result startStream %s" % result)

start = time.time()
elapsed_seconds = 0

if isinstance(result, CustomError):
    raise Exception("%s" % result)

while elapsed_seconds < STREAMING_DURATION:
    end = time.time()
    elapsed_seconds = end - start
    frame = rtp_manager.getFrame()

    if frame is None:
        continue

    cv2.imshow("frame", frame)

    if cv2.waitKey(100) & 0xFF == ord("q"):
        break


cv2.destroyAllWindows()

rtp_manager.stopStream()
