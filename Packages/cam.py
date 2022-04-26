import camera as camera
import cv2
import imutils as imutils
import sys

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
# cap.set(cv2.CAP_PROP_EXPOSURE, -5)
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)
# cap.set(cv2.CAP_PROP_AUTO_WB, 0)
# cap.set(cv2.CAP_PROP_TEMPERATURE, 7000)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 700)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
print("cam opend")

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while(cap.isOpened()):
    info = {
        "framecount": cap.get(cv2.CAP_PROP_FRAME_COUNT),
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "codec": int(cap.get(cv2.CAP_PROP_FOURCC))
    }
    print(info)
    retv, frame = cap.read()
    cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
    #cv2.imwrite("frame.jpg", frame)
    # print(retv)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if(frame is None):
        print("Received empty frame. Exiting")
        # sys.exit()
        cap.release()
        cap=cv2.VideoCapture(1, cv2.CAP_DSHOW)
        print(cap)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        retv, frame = cap.read()

    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    cv2.imshow('frame', gray_img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()