import sys
import threading

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtCore import pyqtSlot, QDate, QTimer, QThread, QDateTime
from keras.models import load_model
from pygrabber.dshow_graph import FilterGraph

from functions import *
from UIs.UI_1 import Ui_Billie

UI = Ui_Billie()
arr=[]
time_count=10
arr_limit=time_count*24
arr_index=0

# print bliies' status
def print_status(val):
    UI.status_label.setText(val)

# print conversation
def print_convo(val):
    UI.textBrowser.append(f"{val}")


class MainThread(QThread):
    print('start')

    def __init__(self):
        super(MainThread, self).__init__()
        print('start2')

    def run(self):
        self.get_command()

    def get_command(self):
        global command, print_val1
        print('get command')
        try:
            print_status('Listening.....')

            command, print_val1 = getAudio()
            print_status(print_val1)
            print(command,'   ',print_val1)

        except:
            pass
            print('---error')

        self.execute_command(command, print_val1)
        return command

    def execute_command(self, command, print_vall):
        print('execute command')

        print('------',command)

        if 'billi' in command:

            print_convo(f'You:- {command}')
            print_status('Talking.....')
            print_convo('\nBillie:- Hello. what can I do for you?\n')
            talk('Hello. what can I do for you?')

            print_status('Listening.....')
            command, print_val2 = runCommand()
            print_convo(f'You:- {command}\n')
            print_convo(print_val2)

        else:
            print_status('Undefined.....')
            playsound('../Audios/2_Voice_stop.mp3')
            print('---------undefined')
        self.get_command()


class MainThread2(QThread):
    def __init__(self):
        super(MainThread2, self).__init__()
        print('open UI1')

    def run(self):
        # a = threading.Thread(target=self.emotion_detection)
        # a.start()
        self.emotion_detection()
        graph = FilterGraph()
        UI.comboBox.addItems(graph.get_input_devices())
        print(graph.get_input_devices())
        UI.comboBox.currentIndexChanged.connect(self.selectionchange)


    # select camera
    def selectionchange(self):
        i=UI.comboBox.currentIndex()
        print("Current index",i,"selection changed ",UI.comboBox.currentText())

    def emotion_detection(self):
        # load model
        model = load_model('../Models/trained_model_csv.h5')

        # cascade file for face detection
        face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # get video from web cam
        cap = cv2.VideoCapture(1)

        # loop for capture all frames
        while True:
            # captures frame and returns boolean value and captured image start
            retv, test_img = cap.read()

            # check that the frame is empty
            if (test_img is None):
                print("Received empty frame. Exiting")
                cap.release()

                # capture using cv2.CAP_DSHOW
                # (in windows7 opencv could not display video while using third party camera)
                cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                print(cap)
                retv, test_img = cap.read()

            cv2.normalize(test_img, test_img, 0, 255, cv2.NORM_MINMAX)
            # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 700)
            # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)

            # OpenCV Video I/O API Backend)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

            # capturing image stops

            # Fliping the image
            flip_img = cv2.flip(test_img, 1)

            flip_img = cv2.cvtColor(flip_img, cv2.COLOR_BGR2RGB)

            # Converting the input frame to grayscale
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
                normalize = resize / 255.0
                reshape = np.reshape(normalize, (1, 48, 48, 1))
                result = model.predict(reshape)
                label = np.argmax(result, axis=1)[0]
                # print(label)

                emotions = ('anger', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'natural')

                cv2.putText(flip_img, emotions[label], (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                UI.mood_lable.setText(emotions[label])

                if len(arr) >= arr_limit:
                    arr[arr_index] = emotions[label]
                    arr_index = (arr_index + 1) % arr_limit
                else:
                    arr.append(emotions[label])

            # මෙතනින් - value - එක - එලියට -return -කරන්න - බෑ - ද?-loop - එක - ඉවර - වෙන්නේ - නැතුව
            # එහෙම - නැත්තන් - loop - එක - ඒ - වෙලාවට - පස්සේ - restart - කරොත් -return -කරගන්න - පුළුවන් - නේ?


            resized_img = cv2.resize(flip_img, (1000, 700))

            # get image infos
            height, width, channel = flip_img.shape
            step = channel * width
            # create QImage from image
            qImg = QImage(flip_img.data, width, height, step, QImage.Format_RGB888)
            # show image in label
            UI.video_label.setPixmap(QPixmap.fromImage(qImg))

        # cap.release()
        # cv2.destroyAllWindows



startBillie = MainThread()
startVideo = MainThread2()


def date():
    dateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
    UI.date_label.setText(dateTime)
    # print(dateTime)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        UI.setupUi(self)

        # start
        timer = QTimer(self)
        timer.timeout.connect(date)
        timer.start(1000)
        startBillie.start()
        startVideo.start()
        # t1 = threading.Thread(target=self.audio)
        # t1.start()
        # t2 = threading.Thread(target=self.video)
        # t2.start()

    def audio(self):
        startBillie.start()

    def video(self):
        startVideo.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())
