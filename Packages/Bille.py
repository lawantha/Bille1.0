import urllib
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
from playsound import playsound
from urllib.request import urlretrieve
from gtts import gTTS
from functions import getAudio

listener = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)


#convert text to audio
def talk(text):
    print('---------Converting text to audio')
    #engine.say('Hello. I am billie. what can I do for you?')
    #engine.runAndWait()
    engine.say(text)
    print(text)
    engine.runAndWait()
    print('run and wait')
    playsound('../Audios/2_Voice_stop.mp3')

def print_command(comm):
    pc=comm
    print(comm)

#get command from user
def getCommand():
    try:
        command= getAudio()
        print(command)

        if 'billi' in command:
            #talk(command)
            talk('Hello. what can I do for you?')
            # command = command.replace('billi','')
            # runCommand()
            # print_command(command)
            print('3')
            # command = getCommand()
            # print(command)
            command = getAudio()
            print(command)
            print_command('command2---',command)
            if 'play' in command:
                song = command.replace('play', '')
                talk('playing' + song)
                print('playing' + song)
                pywhatkit.playonyt(song)

            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                talk('Its ' + time)

            elif 'thank you' in command:
                talk('You are wellcome')

            elif 'who' in command:
                person = command.replace('who is', '')
                print('serching for ' + person)
                talk('serching for ' + person)
                info = wikipedia.summary(person, 2)
                print(info)
                talk(info)

            else:
                print('Undefined command')
                # talk('Sorry I couldnt understand it')
        else:
            print('---------undefined')
    except:
        pass
        print('error')
    return command

def runCommand():
    print('3')
    # command = getCommand()
    # print(command)
    print('---------Calibrating microphone 1...')
    listener.adjust_for_ambient_noise(source, duration=1)
    print('---------Listening 1... ')
    voice = listener.listen(source)
    print('---------audio get from user 1')
    command = listener.recognize_google(voice)
    print('---------audio recognized 1')
    print_command(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' +song)
        print('playing' +song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Its ' + time)

    elif 'thank you' in command:
        talk('You are wellcome')

    elif 'who' in command:
        person = command.replace('who is', '')
        print('serching for '+ person)
        talk('serching for '+ person)
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)
    else:
        print('Undefined command')
        # talk('Sorry I couldnt understand it')


while True:
    getCommand()