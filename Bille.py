
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def talk(text):
    #engine.say('Hello. I am billie. what can I do for you?')
    #engine.runAndWait()
    engine.say(text)
    engine.runAndWait()

def getCommand():
    try:
        with sr.Microphone() as source:
            print('2')
            listener.adjust_for_ambient_noise(source,duration=3)
            print('say anything : ')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
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


while True:
    runCommand()