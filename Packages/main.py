# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import urllib
from playsound import playsound
from datetime import datetime
from urllib.request import urlretrieve
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
# from UIs import UI1

name = 'lawantha'

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Lawantha')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def play_sound():
    playsound('../Audios/1_Voice_start.mp3')
    print('playing sound using native player')
    playsound('../Audios/2_Voice_stop.mp3')

sum = 0
for n in range(0,4):
    sum += 3*n


print (sum)

def time():
    lookup = {
        '01': 'st',
        '21': 'st',
        '31': 'st',
        '02': 'nd',
        '22': 'nd',
        '03': 'rd',
        '23': 'rd'}
    # global datee
    datee = (f"{datetime.now(): %B %d{lookup.get('%B', 'th')} %Y}")
    print(datee)
    return datee



def is_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=1)
        print('internet connected')
        return True
    except urllib.request.URLError:
        print('internet error')
        return False

class UI_1(QDialog):
    def __init__(self):
        super(UI_1, self).__init__()
        loadUi("../UIs/UI_1.ui", self)


if __name__ == "__main__":
    is_internet()
    play_sound()
    # UI1.main()