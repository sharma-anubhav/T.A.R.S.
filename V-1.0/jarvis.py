import tkinter as tk
import requests, webbrowser
from bs4 import BeautifulSoup
import speech_recognition as sr
import pickle
import copy
import os
from pyttsx3 import *
import subprocess
import keyboard
import urllib
import json
import datetime
import eel
import os
import random
import pyttsx3
from num2words import num2words
import wikipedia


r = sr.Recognizer()
engine = pyttsx3.init()
engine.say("Hello!")
engine.runAndWait()
eel.init('web')


@eel.expose  # Expose this function to Javascript

def button_handler_py():
    speak("What would you like me to do?")
    com = listen()
    rcom = copy.deepcopy(com)

    if com.startswith("open") or com.startswith("Open"):
        com = com.replace("open ", "")
        subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "/Applications/{name}.app".format(name = com)])
        return rcom

    if com.startswith("google") or com.startswith("Google"):
        com = com.replace("google ", "")
        Web_Search(com,1)
        return rcom

    if com.startswith("search") or com.startswith("Search"):
        com = com.rsplit("for ")
        com = com[1]
        speak("What kind of results do you want?, Web, news, video, shopping")
        com2 = listen()
        if com2 in ["Web","web","results","pages"]:
            Web_Search(com, 1)
        if com2 in ["News", "news", "Breaking news", "breaking news"]:
            Web_Search(com, 2)
        if com2 in ["Video", "video", "Youtube", "youtube"]:
            Web_Search(com, 3)
        return rcom

    if com.startswith("play") or com.startswith("Play"):
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
        try:
            com = com.rsplit("in ")
            com = com[1]
            w = weather(com)
            return w
        except:
            return "Sorry! didnt understand, Try asking: What is the weather in Patiala?"

    elif com.startswith("shutdown") or com.startswith("Shutdown"):
        print("Shutdown")
        return rcom

    elif "date" in com or "day" in com or "Date" in com or "Day" in com :
        x = datetime.datetime.now()
        ans = "today is" + x.strftime("%A") + "," + num2words(x.strftime("%d")) + x.strftime("%B") + num2words(
            x.strftime("%Y"))
        speak(ans)
        return ans

    elif "information" in com or "info" in com or "Information" in com or "Info" in com:
        try:
            com = com.rsplit(" on ")
            com = com[1]
        except:
            com = com.rsplit(" about ")
            com = com[1]
        print(com)
        w = wiki(com)
        return w

    elif "brightness" in com or "Brightness" in com:
        try:
            com = com.rsplit("to ")
            com = com[1]
            brightness(com)
        except:
            rcom = "Kindly Try Saying Set Brightness to 50"
        return rcom

    else:
        try:
            url = "https://robomatic-ai.p.rapidapi.com/api.php"
            query = com
            payload = "SessionID=RapidAPI1&in={}&op=in&cbid=1&cbot=1&ChatSource=RapidAPI&key=RHMN5hnQ4wTYZBGCF3dfxzypt68rVP".format(
                query)
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'x-rapidapi-key': "90453fa90emshc6459bcf8c3984ep17a855jsn025e5388d417",
                'x-rapidapi-host': "robomatic-ai.p.rapidapi.com"
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            response = response.json()
            print(response["out"])
            speak(response["out"])
            return response["out"]
        except:
            print("PLease try again!")
            speak("PLease try again!")
            return "Please try again"

def speak(audio_string):
    engine.say(audio_string)
    engine.runAndWait()
    engine.stop()
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
        com = "Could not understand, PLease try again"
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return "Could not request results "
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
            results = soup.select('.rc a')
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
            for link in results[:1]:
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


def wiki(search):
    results = wikipedia.search(search)
    print(wikipedia.summary(results[0]))
    speak(wikipedia.summary(results[0])[:600])
    return wikipedia.summary(results[0])

def shutdown():
    import subprocess
    subprocess.call(["shutdown", "-f", "-s", "-t", "60"])
    return

def brightness(brightness):
    try:
      # percentage [0-100] For changing thee screen
        c = wmi.WMI(namespace='wmi')
        methods = c.WmiMonitorBrightnessMethods()[0]
        methods.WmiSetBrightness(int(brightness), 0)
    except:
        s_converter.say("Pleae say a brightness level between 1-100")
        s_converter.runAndWait()
    return
eel.start('button.html', size=(1200, 800))    # Start


# 5https://www.google.com/search?q=anubhav&tbm=isch&
#python -m eel chat.py web --onefile --hidden-import=pkg_resources.py2_warn  --hidden-import=pyttsx3.drivers --hidden-import=pyttsx3.drivers.dummy --hidden-import=pyttsx3.drivers.espeak --hidden-import=pyttsx3.drivers.nsss --hidden-import=pyttsx3.drivers.sapi5 --icon=icon.ico
'''
async function button_handler() {
  let return_value = await eel.button_handler_py()();
  document.getElementById('output').value = return_value;
}
'''