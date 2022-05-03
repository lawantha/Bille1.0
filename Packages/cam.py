# import camera as camera
import cv2
# import imutils as imutils
import sys


from pygrabber.dshow_graph import FilterGraph
i=0
for i in range (0,4):
    graph = FilterGraph()
    print(graph.get_input_devices())

def CameraIndexes():
    # Cam indexes limit, that you would like to check? .
    index = 0
    arr = []
    iter_idx = 10
    while iter_idx > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        iter_idx -= 1
    return arr

    print("\n\nCamera Indexes: ", CameraIndexes())

def camm():
    cam='ZZ3'
    cap = cv2.VideoCapture(cam)
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
        # info = {
        #     "framecount": cap.get(cv2.CAP_PROP_FRAME_COUNT),
        #     "fps": cap.get(cv2.CAP_PROP_FPS),
        #     "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        #     "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        #     "codec": int(cap.get(cv2.CAP_PROP_FOURCC))
        # }
        # print(info)
        retv, frame = cap.read()
        cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
        #cv2.imwrite("frame.jpg", frame)
        # print(retv)

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if(frame is None):
            print("Received empty frame. Exiting")
            # sys.exit()
            cap.release()
            cap=cv2.VideoCapture(cam, cv2.CAP_DSHOW)
            print(cap)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            retv, frame = cap.read()

        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.imshow('frame', gray_img)

        # return gray_img
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


# camm()