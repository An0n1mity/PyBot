from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InputFile
from bot_functions.functions import Website_choice, Password_Viewer, Weather, YoutubetoMP3
import base64
import logging
import io

updater = Updater(token='1143237883:AAGtv7aPHWxDMWqQHewfh-Luqw-pvy1hDbE', use_context=True)
dispatcher = updater.dispatcher

def progress(current, total):
    print("{:.1f}%".format(current * 100 / total))

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bonjour, je suis PyBot ! Que puis faire pour vous aider ?")

def Spassword(update, context):
    website_list = Website_choice()
    master_password = context.args[0]
    website_choice = int(context.args[1])
    password = Password_Viewer(master_password, website_choice)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Le mot de passe pour {} est {}".format(website_list[website_choice],password))

def Cpassword(update, context):
    website_list = Website_choice()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Liste des sites :')
    for i in range(0, len(website_list)):
        text = '{} : {}'.format(i,website_list[i])
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def ytpmp3(update, context):
    url = context.args[0]
    YoutubetoMP3(url)
    
def weather(update, context):
    user_message = update.message.text
    if 'météo' in user_message or 'meteo' in user_message:
        weather_conditions = Weather()
        for i in range(0, len(weather_conditions)):
            if i == 0:
                if weather_conditions[i] == "Clouds":
                    context.bot.send_message(chat_id=update.effective_chat.id, text='General : {}'.format("\U00002601"))
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text='General : {}'.format(weather_conditions[i]))

            elif i == 2:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Temperature : {} C°'.format(weather_conditions[i]))
            elif i == 1:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Pression : {}'.format(weather_conditions[i]))
    else:
        pass

youtubemp3_handler = CommandHandler('youtubemp3', ytpmp3)
dispatcher.add_handler(youtubemp3_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

Cpassword_handler = CommandHandler('Cpassword', Cpassword)
dispatcher.add_handler(Cpassword_handler)

Spassword_handler = CommandHandler("Spassword", Spassword)
dispatcher.add_handler(Spassword_handler)

weather_handler = MessageHandler(Filters.text, weather)
dispatcher.add_handler(weather_handler)

updater.start_polling()
