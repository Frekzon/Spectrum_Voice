import pyttsx3
import speech_recognition as sr
import time
from fuzzywuzzy import fuzz
import datetime
import random
import logging
import requests
import subprocess
import webbrowser
from win10toast import ToastNotifier


logging.basicConfig(level=logging.INFO, filename="LogSpectrum.log")
logging.info("Запуск помощника")

opts = {
    "alias": ('spectrum', 'спектрум'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'давай поиграем в', 'подбрось', 'включай', 'кинь', 'сколько выпало на', 'открой', 'включи', 'создай', 'открой окно', 'подкинь', 'какое', 'открой вкладку', 'загадай', 'нужен'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас время', 'сейчас', 'время', 'времени'),
        "hello": ('привет', 'здравствуй'),
        "money": ('монету', 'орел и решка', 'орла и решку',),
        "d20": ('дайс', 'кубик d20', '', 'кубике d20'),
        #"cmds": ('командную строку', 'cmd', 'цмд', 'строку', 'командной строки'),
        "notify": ('уведомление', 'таймер'),
        "exp": ('проводник', 'проводника'),
        "yt": ('ютуб', 'youtube'),
        "weather": ('погоду', 'погода', 'погодой'),
        "mylove": ('Витебск','к Саше'),
        "calc": ('подсчёт')
 
    }
}
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        logging.info("[log] Речь распознана")
        logging.info("Ваша фраза: " + voice)

        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        #print("[log] Я вас не понял. Повторите пожалуйста")
        logging.warning("[log] Не распознана речь")
    except sr.RequestError as e:
        print("Ошибка сервиса: {0}".format(e))
        logging.error("Ошибка сервиса: {0}".format(e) + "Проверьте подключение к интернету")
       

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC

def execute_cmd(cmd):

    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'hello':
        speak("Привет, пользователь")

    elif cmd == 'money':
        rw = ['Орел', 'Решка']
        random_money = random.choices(rw)
        speak("Выпало :" + str(random_money))

    elif cmd == 'd20':
        d20_res = random.randint(1,20)
        speak(str(d20_res))

    elif cmd == 'yt':
        webbrowser.open('https://www.youtube.com')
    
    elif cmd == 'weather':
        print("Напишите город:")
        weather_input = input()
        city = weather_input
        url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=3456493edcef4076ece5155ecddda5f8'
        weather_data = requests.get(url).json()
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        print('Сейчас в городе', city, str(temperature), '°C')
        print('Ощущается как', str(temperature_feels), '°C')
        logging.info("Выдало погоду")
    
        
    elif cmd == 'notify':
        speak("Напишите что нужно вывести")
        response_title = input()
        speak("Через сколько мне вывести уведомление?(минут)")
        time_min = input()
        time_sec =int(time_min) * 60
        print(time_sec)
        time.sleep(int(time_sec))

        toast = ToastNotifier()
        toast.show_toast("Spectrum", response_title, duration=10, icon_path="")
        logging.info("уведомление сработало")

    elif cmd == 'exp':
        subprocess.Popen('C:/Windows/explorer.exe')

        
    
        
    
    else:
        logging.warning("Команда не была распозанана. Повторите попытку")

r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[1].id)



speak("Привет, пользователь!")
logging.info("Старт")



# Цикл для работы скрипта
while True:
    with m as source:
        audio = r.listen(source)
        callback(r, audio)
