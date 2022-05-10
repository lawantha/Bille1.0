import os
import threading
import time
from collections import Counter

import cv2
import numpy as np
#from Detector import detector
from keras.preprocessing import image
import warnings

# from Packages.functions import time_range

warnings.filterwarnings("ignore")
from keras.preprocessing.image import load_img, img_to_array
from keras.models import  load_model
#import matplotlib.pyplot as plt

# load model
model = load_model('../Models/trained_model_csv.h5')

# cascade file for face detection
face_haar_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')


# get video from web cam
cap = cv2.VideoCapture(1)
start = time.time()
end = start+60
print(start,'           ',end)

arr=[]


#loop for capture all frames
def cam():
    arr_limit = 10
    arr_index = 0
    cap = cv2.VideoCapture('../emotions.mp4')
    time_count = 5
    while True:
        # captures frame and returns boolean value and captured image start
        retv, test_img = cap.read()

        #check that the frame is empty
        if (test_img is None):
            print("Received empty frame. Exiting")
            cap.release()
            #capture using cv2.CAP_DSHOW (in windows7 opencv could not display video while using third party camera)
            cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FPS, 24)
            print(cap)
            retv, test_img = cap.read()

        cv2.normalize(test_img, test_img, 0, 255, cv2.NORM_MINMAX)
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 700)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)

        #OpenCV Video I/O API Backend)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))


        # capturing image stops

        # Fliping the image
        flip_img = cv2.flip(test_img, 1)

        #Converting the input frame to grayscale
        gray_img = cv2.cvtColor(flip_img, cv2.COLOR_BGR2GRAY)

        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

        # emotions = ('anger', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'natural')
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(flip_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=3)
            face = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
            resize = cv2.resize(face, (48, 48))
            # img_pixels = image.img_to_array(resize)
            # img_pixels = np.expand_dims(img_pixels, axis=0)
            # img_pixels /= 255
            normalize = resize/255.0
            reshape = np.reshape(normalize,(1,48,48,1))
            result = model.predict(reshape)
            label = np.argmax(result, axis=1)[0]
            # print (label)


            # predictions = model.predict(img_pixels)

            # find max indexed array
            # max_index = np.argmax(predictions[0])

            #model_old_rgb
            #emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
            #model2
            #emotions = {0 : 'angry', 1 : 'disgust', 2 : 'fear', 3 : 'happy', 4 : 'neutral', 5 : 'sad', 6 : 'surprise'}
            #model_csv
            emotions = ('anger', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'natural')
            # predicted_emotion = emotions[max_index]
            # print(emotions[label])

            # dts = [emotions[label] for dt in time_range(start, end, 5)]
            # print(dts)
            # print(emotions[label])

            if len(arr) >= arr_limit:
                arr[arr_index]=emotions[label]
                arr_index=(arr_index+1)%arr_limit
            else:
                arr.append(emotions[label])

            cv2.putText(flip_img, emotions[label], (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        resized_img = cv2.resize(flip_img, (1000, 700))
        # print(arr)
        # carr = Counter(arr).most_common(1)
        # print(carr)

        # පහෙන්පහට_array_එක_මුල_ඉදන්_යන්නෙ_න_නේ.තියෙන_එකටම_එකතු_වෙවී_යනවා_නේ
        # තප්පර - දෙකෙන් - දෙකට - වගේ - value - එක - ගන්න - බෑ - ද - අරක - වගේ - colabs
        cv2.imshow('Facial emotion analysis', resized_img)
        if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
            break

    print(arr)
    carr=Counter(arr).most_common(1)
    print('aaaaaaaaaa')
    # nparr=np.array(arr)
    # print(nparr)
    # carr=np.argmax(np.bincount(nparr))
    print(carr)
    cap.release()
    cv2.destroyAllWindows()

def array():
    while True:
        # print('aaaaa')
        # print(arr)
        carr = [word for word, word_count in Counter(arr).most_common(2)]
        # nparr=np.array(arr)
        # print(nparr)
        # carr=np.argmax(np.bincount(nparr))
        print(carr)
        time.sleep(1)

# def delayed_detection():
#     time.sleep(10)
#     array()

import socket
if __name__ == '__main__':
    threading.Thread(target = cam).start()
    # threading.Thread(target = array).start()
    print(socket.gethostname())
    


