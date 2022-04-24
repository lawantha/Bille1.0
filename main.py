# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Lawantha')

lookup = {
    '01': 'st',
    '21': 'st',
    '31': 'st',
    '02': 'nd',
    '22': 'nd',
    '03': 'rd',
    '23': 'rd'}
print(f"{datetime.now(): %B %d{lookup.get('%B', 'th')} %Y}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from playsound import playsound

playsound('Audios/1_Voice_start.mp3')
print('playing sound using native player')
playsound('Audios/2_Voice_stop.mp3')

sum = 0
for n in range(0,4):
    sum += 3*n


print (sum)