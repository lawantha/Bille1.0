import random
import sys
import time

sys.path.append('venv/Lib/site-packages')
import socket
import threading
from collections import Counter

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtCore import pyqtSlot, QDate, QTimer, QThread, QDateTime
from keras.models import load_model
from pygrabber.dshow_graph import FilterGraph

from Packages.functions import *
from UIs.UI_1 import Ui_Billie

UI = Ui_Billie()
arr=['Recognizing...']
arr2=['Recognizing...']
billie_say=['hello. what can i do for you', 'hey', 'hey. how are you', 'hello. how are you']

cap = cv2.VideoCapture(1)
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

        if 'billi' in command or 'Billi' in command or 'billy' in command:

            print_convo(f'You:- {command}')
            print_status('Talking.....')
            get_billie_say=random.choice(billie_say)
            print_convo(f'\nBillie:- {get_billie_say}\n')
            talk(get_billie_say)

            print_status('Listening.....')
            command, print_val2 = runCommand()
            print_convo(f'You:- {command}\n')
            print_convo(print_val2)

        else:
            if is_internet():
                print('Undefined command---------')
                billie_talk = f"Billie:- Undefined command\n\n"
                playsound('Audios/2_Voice_stop.mp3')
                # talk('Sorry I couldnt understand it')
                # quit()
            else:
                print_convo('\n----------internet error. please check your internet connection\n')
                print_status('internet error....')
        self.get_command()


class MainThread2(QThread):
    def __init__(self):
        super(MainThread2, self).__init__()
        print('open UI1')

    def run(self):
        # a = threading.Thread(target=self.emotion_detection)
        # a.start()
        graph = FilterGraph()
        print(graph.get_input_devices())
        UI.comboBox.addItems(graph.get_input_devices())
        UI.comboBox.currentIndexChanged.connect(self.selectionchange)
        i=UI.comboBox.currentIndex()
        self.emotion_detection(i)


    # select camera
    def selectionchange(self):
        i=UI.comboBox.currentIndex()
        print("Current index",i,"selection changed ",UI.comboBox.currentText())

    def emotion_detection(self,cam_id):
        arr_limit = 50
        arr_index = 0
        # load model
        model = load_model('Models/trained_model_csv.h5')

        # cascade file for face detection
        face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # get video from web cam
        cap = cv2.VideoCapture(cam_id)

        # loop for capture all frames
        while True:
            i = UI.comboBox.currentIndex()
            # print('cam--',i)
            # captures frame and returns boolean value and captured image start
            retv, test_img = cap.read()

            # check that the frame is empty
            if (test_img is None):
                print("Camera Changed")

                # capture using cv2.CAP_DSHOW
                # (in windows7 opencv could not display video while using third party camera)
                cap = cv2.VideoCapture(i)
                retv, test_img = cap.read()
                print(cap)
                if (test_img is None):
                    print("Received empty frame. Exiting")
                    cap.release()
                    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                    retv, test_img = cap.read()
                    print(cap)
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

                # UI.mood_lable.setText(emotions[label])

                if len(arr) >= arr_limit:
                    arr[arr_index] = emotions[label]
                    arr_index = (arr_index + 1) % arr_limit
                else:
                    arr.append(emotions[label])


            resized_img = cv2.resize(flip_img, (1000, 700))

            # get image infos
            height, width, channel = flip_img.shape
            step = channel * width
            # create QImage from image
            qImg = QImage(flip_img.data, width, height, step, QImage.Format_RGB888)
            # show image in label
            UI.video_label.setPixmap(QPixmap.fromImage(qImg))

            if i != cam_id:
                print(i,cam_id)
                cam_id=i
                cap.release()
        # print('cap relese')
        # cv2.destroyAllWindows


def date():
    dateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
    UI.date_label.setText(dateTime)
    # print(dateTime)

class Array(QThread):

    def __init__(self):
        super(Array, self).__init__()
        print('open array')

    def run(self):
        self.array()

    def array(selfe):
        arr2_limit=400000000
        start_time = time.time()
        seconds = 20*60

        while True:
            carr_ar = [word for word, word_count in Counter(arr).most_common(1)]
            carr=carr_ar[0]
            UI.mood_lable.setText(carr)
            current_time = time.time()
            elapsed_time = current_time - start_time
            # print(carr)

            if elapsed_time > seconds:
                carr_ar = [word for word, word_count in Counter(arr2).most_common(1)]
                carr2 = carr_ar[0]
                print('b')
                mood(carr2)
                start_time = time.time()
                arr2.clear()
            else:
                arr2.append(carr)


startBillie = MainThread()
startVideo = MainThread2()
startArray = Array()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        UI.setupUi(self)

        # start
        timer = QTimer(self)
        timer.timeout.connect(date)
        timer.start(1000)
        UI.name_lable.setText(socket.gethostname())
        startVideo.start()
        startBillie.start()
        startArray.start()

        UI.movie = QMovie('img/block_1.gif')
        UI.gif1.setMovie(UI.movie)
        UI.movie.start()

        UI.main_img.setPixmap(QPixmap("img/background.jpg"))


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
