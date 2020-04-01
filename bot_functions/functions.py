from __future__ import unicode_literals
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import fileinput
import requests
from pprint import pprint
import youtube_dl
import datetime
import time


def Password_Viewer(master_password, website_choice):
    #Ouverture du fichier data.txt
    password = master_password.encode()
    salt = b'156'
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=1000,
    backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    password_file = open('data.txt', "r")
    password_Flist = [password_file.read()]
    password_Flist = ",".join(password_Flist)
    password_Flist = password_Flist.split(",")
    password_list = []

    # Crée une liste avec tout les mots de passe 
    i=0
    a=2
    while i < len(password_Flist):
        if i==a:
            a+=4
            password_list.append(password_Flist[i].replace(" ", ""))
            pass
        i+=1

    password = password_list[website_choice].replace(" ", "")
    password = password.encode()             #Transforme str en byte
    try:
        your_password = f.decrypt(password) #Decryptage du mot de passe
    except:
        print("Vous n'avez pas le mot de passe maitre permettant le decodage...")
        return
        
    return your_password.decode()

def Website_choice():
    password_file = open('data.txt', "r")
    password_Flist = [password_file.read()]
    password_Flist = ",".join(password_Flist)
    password_Flist = password_Flist.split(",")
    password_list = []

    # Crée une liste avec tout les mots de passe 
    i=0
    a=2
    while i < len(password_Flist):
        if i==a:
            a+=4
            password_list.append(password_Flist[i].replace(" ", ""))
            pass
        i+=1

    # Crée une liste avec tout les noms des applications
    b=0
    c=4
    website_list = []
    while b < len(password_Flist):
        if b == c:
            c+=4
            website_list.append(password_Flist[b].replace("\n", ""))
            pass
        elif b==0:
            website_list.append(password_Flist[b].replace("\n",""))
            pass
        b+=1
    if website_list[len(website_list)-1] == '':
        del website_list[len(website_list)-1]
        pass
    
    return website_list

def Weather():
    token = #Insert API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    current_city = "Guadeloupe"
    final_url = base_url + "q=" + current_city + "&appid=" + token
    weather_data = requests.get(final_url).json()
    humidity = weather_data['main']['humidity']
    weather_general = weather_data['weather'][0]['main']
    temperature = weather_data['main']['temp']
    temperatureC = int(temperature)-273
    weather = [weather_general, humidity, temperatureC]
    return weather

def YoutubetoMP3(url):
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': '.mp3',
        'preferredquality': '192',
    }],
}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def Surf_Forecast(spot, context, update):
    key = #Insert API key
    url = "http://magicseaweed.com/api/" + key + "/forecast/?spot_id=" + spot + "&units=eu"
    surf_data = requests.get(url).json() #List de dictionnaire
    local_time_day = int(str(datetime.datetime.utcfromtimestamp(int(time.time())))[8:10])
    star = "\U00002B50"
    dic_local_star_rating = {}
    dic_local_swell_maxBreakingHeight = {}
    dic_local_swell_minBreakingHeight = {}
    dic_local_wind_speed = {}
    dic_local_combined_height = {}

    #Indiquer les conditions actuelles
    for i in range(0, len(surf_data)):
        print(i)
        localTimestamp = surf_data[i]["localTimestamp"] 
        try:
            local_time_day_forecast = int(str(datetime.datetime.utcfromtimestamp(int(localTimestamp)))[8:10])
            local_time_hour = int(str(datetime.datetime.utcfromtimestamp(int(localTimestamp)))[11:13])
        except Exception as e:
            print(e)

        print(local_time_day_forecast)
        if local_time_day_forecast == local_time_day:
            star_rating = surf_data[i]['fadedRating']
            swell_maxBreakingHeight = surf_data[i]['swell']['maxBreakingHeight']
            swell_minBreakingHeight = surf_data[i]['swell']['minBreakingHeight']
            wind_speed = surf_data[i]['wind']['speed']
            combined_height = surf_data[i]['swell']['components']['combined']['height']
            dic_local_combined_height[local_time_hour] = combined_height
            dic_local_wind_speed[local_time_hour] = wind_speed
            dic_local_swell_maxBreakingHeight[local_time_hour] = swell_maxBreakingHeight
            dic_local_swell_minBreakingHeight[local_time_hour] = swell_minBreakingHeight
            dic_local_star_rating[local_time_hour] = star_rating
            print(dic_local_star_rating)
        
    for hour in dic_local_star_rating:
        context.bot.send_message(chat_id=update.effective_chat.id, text='{} heure : {} | {}-{}m | {}m |{} kph'.format(hour, star, dic_local_swell_minBreakingHeight[hour], dic_local_swell_maxBreakingHeight[hour], dic_local_combined_height[hour] ,dic_local_wind_speed[local_time_hour])) #dic_local_star_rating[local_time_hour]*
    #Indiquer à quelle date il est le plus optimal de surfer
