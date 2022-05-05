import urllib
from datetime import datetime
from urllib.request import urlretrieve
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
from playsound import playsound
from gtts import gTTS

listener = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)
print('---------internet connected')
# check for internet
# from numpy.lib.utils import source


def is_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=1)
        return True
    except urllib.request.URLError:
        print('---------internet error_function')
        return False

# if is_internet():
#     import speech_recognition as sr
#     import pyttsx3
#     import pywhatkit
#     import datetime
#     import wikipedia
#     from playsound import playsound
#     from gtts import gTTS
#
#     listener = sr.Recognizer()
#     engine = pyttsx3.init(driverName='sapi5')
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[0].id)
#     engine.setProperty('rate', 150)
#     print('---------internet connected')
# else:
#     print('unable to connect internet')


#convert text to audio
def talk(text):
    print('---------Converting text to audio')
    engine.say(text)
    print(text)
    engine.runAndWait()
    print('run and wait')
    playsound('../Audios/2_Voice_stop.mp3')


#audio to text
def getAudio():
    try:
        command=''
        with sr.Microphone() as source:
            # print('---------Calibrating microphone...')
            # listener.adjust_for_ambient_noise(source,duration=1)
            print('---------Listening... ')
            print_val = 'Listening.....'
            voice = listener.listen(source)
            print('---------audio get from user')
            try:
                print_val = 'Recognizing.....'
                command = listener.recognize_google(voice)
                print('---------audio recognized')
                playsound('../Audios/1_Voice_start.mp3')
                command = command.lower()
                print('command-----',command)
            except:
                if is_internet(bool(False)):
                    print_val = 'internet error'
                    print('internet error')
                else:
                    print('unable to understand')
                    print_val = 'unable to understand'

    except:
        pass
        print_val = 'Error.....'
        print('---------error')

    return command, print_val

billie_talk = 'None'
def runCommand():
    command, val = getAudio()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' +song)
        print('playing' +song)
        billie_talk = f"Billie:- playing {song}\n\n"
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.now().strftime('%I:%M %p')
        talk('Its ' + time)
        billie_talk = f"Billie:- Its {time}\n\n"

    elif 'thank you' in command:
        talk('You are wellcome')
        billie_talk = f"Billie:- You are wellcome\n\n"

    elif 'who' in command:
        person = command.replace('who is', '')
        person = command.replace('tell me who is', '')
        print('serching for '+ person)
        talk('serching for '+ person)
        billie_talk = f"Billie:- serching for {person}\n\n"
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)
        billie_talk = f"Billie:- According to google {info}\n\n"
    else:
        print('Undefined command')
        billie_talk = f"Billie:- Undefined command\n\n"
        # talk('Sorry I couldnt understand it')
        # quit()

    return command, billie_talk



# is_internet()
# getAudio()