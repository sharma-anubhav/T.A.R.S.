import tkinter as tk
import requests, webbrowser
from bs4 import BeautifulSoup
import speech_recognition as sr
import pickle
import copy
import os
import subprocess
import urllib
import json
import datetime
import eel
import os
from gtts import gTTS
import playsound # to play an audio file
import random
from num2words import num2words
import wikipedia

r = sr.Recognizer()
tts = gTTS(text="Hey There!, I'm Alexa", lang='en-ca')  # text to speech(voice)
r = random.randint(1, 20000000)
audio_file = 'audio' + str(r) + '.mp3'
tts.save(audio_file)  # save as mp3
playsound.playsound(audio_file)  # play the audio file
os.remove(audio_file)

eel.init('web')

@eel.expose  # Expose this function to Javascript

def button_handler_py():
    speak("What would you like me to do?")
    com = listen()
    rcom = copy.deepcopy(com)

    if com.startswith("open"):
        com = com.replace("open ", "")
        subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "/Applications/{name}.app".format(name = com)])
        return rcom

    if com.startswith("google"):
        com = com.replace("google ", "")
        Web_Search(com,1)
        return rcom
    if com.startswith("search"):
        com = com.rsplit("for ")
        com = com[1]
        speak("What kind of resuls do you want?, Web ,news ,video , shopping")
        com2 = listen()
        if com2 in ["Web","web","results","pages"]:
            Web_Search(com, 1)
        if com2 in ["News", "news", "Breaking news", "breaking news"]:
            Web_Search(com, 2)
        if com2 in ["Video", "video", "Youtube", "youtube"]:
            Web_Search(com, 3)
        return rcom

    if com.startswith("play"):
        com = com.replace("play ", "")
        Web_Search(com, 3)
        return rcom

    if com.startswith("take note") or com.startswith("note"):
        try:
            Notes = pickle.load(open('/Users/anubhavsharma/Desktop/Notes.txt', 'rb'))
        except IOError:
            Notes = []

        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("Recording!")

            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            Notes.append(text)
            with open('/Users/anubhavsharma/Desktop/Notes.txt', 'wb') as fh:
                pickle.dump(Notes, fh)
        except sr.UnknownValueError:
            speak("Could not understand, PLease try again")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        return text

    elif "weather" in com:
        com = com.rsplit("in ")
        com = com[1]
        w = weather(com)
        return w

    elif com.startswith("shutdown"):
        print("Shutdown")
        return rcom

    elif "date" in com or "day" in com:
        x = datetime.datetime.now()
        ans = "today is" + x.strftime("%A") + "," + num2words(x.strftime("%d")) + x.strftime("%B") + num2words(
            x.strftime("%Y"))
        speak(ans)
        return ans

    elif "information" in com or "info" in com:
        try:
            com = com.rsplit("on ")
        except:
            com = com.rsplit("about ")
            com = com[1]
        w = wiki(com)
    return w

def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en-ca') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"Alex: {audio_string}") # print what app said
    os.remove(audio_file)
    return

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("speak!")
        audio = r.listen(source)
        print('done!')
    try:
        com = r.recognize_google(audio)
        print("You said: " + com)
    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("Could not understand, PLease try again")

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    return com



def Web_Search(search,int):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    query = search
    query = query.replace(' ', '+')
    choice = int
    if choice == 1 :
        URL = f"https://google.com/search?q={query}"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            results = soup.select('.r a')
            for link in results[:3]:
                actual = link.get('href')
                print(actual)
                webbrowser.open(actual)

    elif choice == 2:
        URL = f"https://google.com/search?q={query}" + "&tbm=nws&"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            results = soup.select('.dbsr a')
            for link in results[:4]:
                actual = link.get('href')
                print(actual)
                webbrowser.open(actual)

    elif choice == 3:
        URL = f"https://google.com/search?q={query}" + "&tbm=vid&"
        print(URL)
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            results = soup.select('.rGhul')
            for link in results[:2]:
                actual = link.get('href')
                print(actual)
                webbrowser.open(actual)
    return
def weather(city):
    api_key = "69071fdb03e975dc4806bd5dd2aa2a49"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = city

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name


    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":

        y = x["main"]

        current_temperature = y["temp"]
        current_pressure = y["pressure"]

        current_humidiy = y["humidity"]
        z = x["weather"]

        weather_description = z[0]["description"]

        final_weather = (" Temperature right now is " +
              num2words(int(current_temperature) - 273) + " Degree Celcius," +
              "\n atmospheric pressure (in hPa unit) is " +
              num2words(current_pressure) +","+
              "\n humidity is " +
              num2words(current_humidiy) +"Percent,"
              "\n description  " +
              str(weather_description))
    else:
        final_weather = "City Not Found"
    print(final_weather)
    speak(final_weather)
    return final_weather

def shutdown():
    import subprocess
    subprocess.call(["shutdown", "-f", "-s", "-t", "60"])
    return

def wiki(search):
    results = wikipedia.search(search)
    speak(wikipedia.summary(results[0]))
    return wikipedia.summary(results[0])


eel.start('button.html', size=(800, 800), host='localhost', port=8274)    # Start


# 5https://www.google.com/search?q=anubhav&tbm=isch&
#python -m eel search.py web --onefile --hidden-import=pkg_resources.py2_warn --noconsole
'''
async function button_handler() {
  let return_value = await eel.button_handler_py()();
  document.getElementById('output').value = return_value;
}
'''