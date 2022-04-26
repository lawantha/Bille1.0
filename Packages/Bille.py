import urllib
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
from playsound import playsound
from urllib.request import urlretrieve
from gtts import gTTS

listener = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

#check for internet
def is_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=1)
        print('internet connected')
        return True
    except urllib.request.URLError:
        print('internet error')
        return False

#convert text to audio
def talk(text):
    print('1')
    #engine.say('Hello. I am billie. what can I do for you?')
    #engine.runAndWait()
    engine.say(text)
    engine.runAndWait()
    playsound('../Audios/2_Voice_stop.mp3')

#get audio from user
def getCommand():
    try:
        command=''
        with sr.Microphone() as source:
            print('Calibrating microphone...')
            listener.adjust_for_ambient_noise(source,duration=3)
            print('Listening... ')
            voice = listener.listen(source)
            print('get')
            command = listener.recognize_google(voice)
            print('recognized')
            playsound('Audios/1_Voice_start.mp3')
            command = command.lower()
            print(command)
            if 'billi' in command:
                #talk(command)
                talk('Hello. what can I do for you?')
                command = command.replace('billi','')
                print(command)
            else:
                print('undefined')

    except:
        pass
        print('error')
    return command

def runCommand():
    print('3')
    command = getCommand()
    print(command)
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
        talk('Sorry I couldnt understand it')


while True:
    runCommand()