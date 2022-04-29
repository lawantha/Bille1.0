import urllib
from urllib.request import urlretrieve

# check for internet
def is_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=1)
        return True
    except urllib.request.URLError:
        print('---------internet error_function')
        return False

if is_internet():
    import speech_recognition as sr
    import pyttsx3
    import pywhatkit
    import datetime
    import wikipedia
    from playsound import playsound
    from gtts import gTTS

    listener = sr.Recognizer()
    engine = pyttsx3.init(driverName='sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    print('---------internet connected')
else:
    print('unable to connect internet')


#audio to text
def getAudio():
    try:
        command=''
        with sr.Microphone() as source:
            print('---------Calibrating microphone...')
            listener.adjust_for_ambient_noise(source,duration=1)
            print('---------Listening... ')
            voice = listener.listen(source)
            print('---------audio get from user')
            try:
                command = listener.recognize_google(voice)
                print('---------audio recognized')
                playsound('../Audios/1_Voice_start.mp3')
                command = command.lower()
                print('command-----',command)
            except:
                if isInernet(bool(False)):
                    print('internet error')
                else:
                    print('unable to understand')

    except:
        pass
        print('---------error')
    return command

is_internet()
getAudio()