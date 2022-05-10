import sys
sys.path.append('../venv/Lib/site-packages')
import fnmatch
import os,random
import subprocess
import threading
import urllib
from datetime import datetime
# import pyaudio

import pyttsx3
# from urllib.request import urlretrieve
import speech_recognition as sr
import wikipedia
from playsound import playsound

listener = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)


# from numpy.lib.utils import source

billie_talk = 'None'

# check for internet
def is_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=1)
        print('---------internet connected')
        return True
    except urllib.request.URLError:
        print('---------internet error_function')
        return False

#convert text to audio
def talk(text):
    print('Converting text to audio---------')
    engine.say(text)
    print(text)
    engine.runAndWait()
    print('run and wait')
    playsound('Audios/2_Voice_stop.mp3')


#audio to text
def getAudio():
    try:
        command=''
        with sr.Microphone() as source:
            print('---------Calibrating microphone... ---------')
            print_val='Calibrating microphone.....'
            listener.adjust_for_ambient_noise(source,1)
            print('Listening... ---------')
            print_val = 'Listening.....'
            voice = listener.listen(source)
            print('audio get from user---------')
            try:
                print_val = 'Recognizing.....'
                command = listener.recognize_google(voice)
                print('audio recognized---------')
                # playsound('Audios/1_Voice_start.mp3')
                command = command.lower()
                print('recognized audio = ',command)
            except:
                if is_internet():
                    print('unable to understand')
                    # playsound('Audios/2_Voice_stop.mp3')
                    print_val = 'unable to understand'
                else:
                    print_val = 'internet error'
                    billie_talk = '\n----------internet error. please check your internet connection\n'
                    # print('internet error')

    except:
        pass
        print_val = 'Error.....'
        print('error1')

    return command, print_val


def runCommand():
    command, val= getAudio()
    if 'time' in command:
        time = datetime.now().strftime('%I:%M %p')
        talk('Its ' + time)
        billie_talk = f"Billie:- Its {time}\n\n"

    elif 'thank you' in command:
        talk('You are wellcome.')
        billie_talk = f"Billie:- You are wellcome\n\n"

    elif 'who is' in command:
        person = command.replace('who is', '')
        person = command.replace('tell me who is', '')
        print('serching for '+ person)
        talk('serching for '+ person)
        billie_talk = f"Billie:- serching for {person}\n\n"
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)
        billie_talk = f"Billie:- According to wikipedia {info}\n\n"

    elif 'play music' in command or 'play song' in command or 'play a song'in command:
        talk('playing music on windows midea player ')
        billie_talk = f"Billie:- Playing music on windows midea player\n\n"
        play_music()

    elif 'play' in command:
        song = command.replace('play', '')
        talk('playing' +song+' in you tube')
        print('playing' +song+' in you tube')
        billie_talk = f'Billie:- playing {song}\n\n'
        youtube(song)

    else:
        if is_internet():
            print('Undefined command---------')
            billie_talk = f"Billie:- Undefined command\n\n"
            playsound('Audios/2_Voice_stop.mp3')
            # talk('Sorry I couldnt understand it')
            # quit()
        else:
            billie_talk = '\n----------internet error. please check your internet connection\n'


    return command, billie_talk

def play_music():
    # mp = 'C:/Program Files (x86)/Windows Media Player/wmplayer.exe'
    music_dir = 'C:/Users/user/Music/ENGLISH/'
    randome=random.choice(fnmatch.filter(os.listdir(music_dir),'*.mp3'))
    file=(music_dir+randome)
    print(file)
    # subprocess.call([mp, file])
    os.startfile(os.path.join(music_dir, file))

def youtube(song):
    if is_internet():
        import pywhatkit
        pywhatkit.playonyt(song)



def get_mood(mood):
    moodd=mood
    mood(moodd)
    print('mooooooood')
    # t1=threading.Thread(target=mood(mood))
    # t1.start()

def mood(mood):
    mood=mood
    print('mood--------',mood)
    if mood == 'Recognizing...':
        print('')
    else:
        talk('Its time to break')
        if mood == 'sad' or mood == 'anger' or mood == 'disgust':
            talk('Its seems you are in sad. It s better to have a small break. Let me play a song for you')
            youtube('relax music/ relax songs')
            # do you need to hear a jock
            print('mood------',mood)
        elif mood == 'happy' or mood == 'natural':
            talk('Did you know that staring at a computer screen for more than twenty minutes is bad for your eyes?')


def selct_music_path():
    return None

def time_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
# is_internet()
# runCommand()
# play_music()