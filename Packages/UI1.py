import sys,threading
from datetime import datetime
import time
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QDate, QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from keras.models import  load_model
from pygrabber.dshow_graph import FilterGraph



class UI1_Dialog(QMainWindow):
    def __init__(self):
        super(UI1_Dialog, self).__init__()
        loadUi("../UIs/UI_1.ui", self)
        print('open UI1')
        # self.video()
        a = threading.Thread(target=self.emotion_detection)
        a.start()
        t = threading.Thread(target=self.date)
        t.start()
        # # create a timer
        # self.timer = QTimer()
        # # set timer timeout callback function
        # self.timer.timeout.connect(self.video)
        graph = FilterGraph()
        self.comboBox.addItems(graph.get_input_devices())
        print(graph.get_input_devices())
        self.comboBox.currentIndexChanged.connect(self.selectionchange)

    # Update time
    def date(self):
        while True:
            date = datetime.now().strftime("%d/%m/%Y        %H:%M:%S")
            time_ = datetime.now().strftime("%H:%M:%S")
            self.date_label.setText(date)
            print(date)
            time.sleep(1)

    #select camera
    def selectionchange(self):
        i=self.comboBox.currentIndex()
        print("Current index",i,"selection changed ",self.comboBox.currentText())

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
                # capture using cv2.CAP_DSHOW (in windows7 opencv could not display video while using third party camera)
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
                print(label)

                emotions = ('anger', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'natural')

                cv2.putText(flip_img, emotions[label], (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                self.mood_lable.setText(emotions[label])

            resized_img = cv2.resize(flip_img, (1000, 700))

            # get image infos
            height, width, channel = flip_img.shape
            step = channel * width
            # create QImage from image
            qImg = QImage(flip_img.data, width, height, step, QImage.Format_RGB888)
            # show image in label
            self.video_label.setPixmap(QPixmap.fromImage(qImg))

        # cap.release()
        # cv2.destroyAllWindows

    # def video(self):
        # # self.timer.start(5)
        # cam = self.comboBox.currentIndex()
        # cap = cv2.VideoCapture(cam, cv2.CAP_DSHOW)
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
        # # read image in BGR format
        # while (cap.isOpened()):
        #     ret, image = cap.read()
        #     # convert image to RGB format
        #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #     # get image infos
        #     height, width, channel = image.shape
        #     step = channel * width
        #     # create QImage from image
        #     qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        #     # show image in img_label
        #     # cv2.imshow('image', image)
        #     self.video_label.setPixmap(QPixmap.fromImage(qImg))
    #
    #     cap.release()
    #     cv2.destroyAllWindows()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI1_Dialog()
    ui.show()
    sys.exit(app.exec_())