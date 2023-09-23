import speech_recognition as sr
import pyttsx3
import pywhatkit
from datetime import datetime, date, timedelta
from time import time
import pyjokes
import AVMSpeechMath as sm
import subprocess as sub

start_time = time()
engine = pyttsx3.init()

#Colors
green_c = "\033[1;32;40m"
red_c = "\033[1;31;40m"
reset_c = "\033[0;37;40m"

#Name
name = 'alexa'
attempts = 0

#Common Websites
sites = {

    'google':'google.com',
    'youtube':'youtube.com',
    'chat gpt':'chat.openai.com',
    'colab':'colab.research.google.com'
}


#Voice config
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#Rate & Volume
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)

#Language iteration
day_es = [line.rstrip('\n') for line in open('day_es.txt')]
day_en = [line.rstrip('\n') for line in open('day_en.txt')]

#English - Spanish
def iterateDays(now):
    for i in range(len(day_en)):
        if day_en[i] in now:
            now = now.replace(day_en[i], day_es[i])
    return now

#Date
def getDay():
    now = date.today().strftime("%A, %d de %B del %Y").lower()
    return iterateDays(now)

#Talk
def talk(text):
    engine.say(text)
    engine.runAndWait()

#Voice recognizement
def get_audio():
    r = sr.Recognizer()
    status = False

    with sr.Microphone() as source:
        print(f"{green_c}({attempts}) Escuchando... {reset_c}")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""
        
        try:
            rec = r.recognize_google(audio, language='es-ES').lower()

            if name in rec:
                rec = rec.replace(f"{name} ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                status = True
            else:
                print(f"Vuelve a intentarlo, no reconozco {rec}")
        except:
            pass
    return {'text':rec, 'status':status}


#Life cycle
while True:
    rec_json = get_audio()

    rec = rec_json['text']
    status = rec_json['status']


    if status:
        #Verify if it's online
        if 'estas ahi' in rec:
            talk('Claro')

        #Play music on Youtube
        elif 'reproduce' in rec:
            if 'youtube' in rec:
                music = rec.replace('reproduce', '')
                talk(f'Reproduciendo {music}')
                pywhatkit.playonyt(music)
            
        #Check out date/time
        elif 'que' in rec:
            if 'hora' in rec:
                hora = datetime.now().strftime('%I:%M %p')
                talk(f"Son las {hora}")

            elif 'dia' in rec:
                talk(f"Hoy es {getDay()}")

        #Tell a joke
        elif 'chiste' in rec:
            chiste = pyjokes.get_joke("es")
            talk(chiste)
        
        #Math operations
        elif 'cuanto es' in rec:
            talk(sm.getResult(rec))
        
        #Open websites
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start brave.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
 
        #End program
        elif 'adios' in rec:
            talk("Hasta luego...")
            break

        else:
            print(f"Vuelve a intentarlo, no reconozco: {rec}")

        attempts = 0
    else:
        attempts += 1

print(f"{red_c} PROGRAMA FINALIZADO CON UNA DURACION DE: { int(time() - start_time)} SEGUNDOS {reset_c}")
