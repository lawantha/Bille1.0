import sys,threading
from datetime import datetime
import time
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QDate
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
# from Packages import main


class UI1_Dialog(QMainWindow):
    def __init__(self):
        super(UI1_Dialog, self).__init__()
        loadUi("../UIs/UI_1.ui", self)
        print('open UI1')
        t = threading.Thread(target=self.date)
        t.start()

        # Update time
    def date(self):
        while True:
            date = datetime.now().strftime("%d/%m/%Y        %H:%M:%S")
            time_ = datetime.now().strftime("%H:%M:%S")
            self.date_label.setText(date)
            print(date)
            time.sleep(1)


    # def name(self):


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI1_Dialog()
    ui.show()
    sys.exit(app.exec_())