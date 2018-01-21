#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import logging, json, requests

TOKEN = '429534900:AAFsqskQ7q6paCblWGN2NoB1JWX_lmCAL0Q'
url = 'https://api.foursquare.com/v2/venues/explore'
type_of_place = None

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

latitude = ""
longitude = ""

def start(bot, update): 
    # bot.send_message(chat_id = update.message.chat_id, text="I'm a bot, please talk to me!")
    update.message.reply_text('Hi!')

def location(bot, update):
    global latitude
    global longitude
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    longitude = user_location.longitude
    latitude = user_location.latitude
    # update.message.reply_text('Maybe I can visit you sometime!' 'At last, tell me something about yourself.')

    keyboard = [[InlineKeyboardButton("Ресторан", callback_data='restaurant'),
                 InlineKeyboardButton("Кафе", callback_data='coffee'),
                 InlineKeyboardButton("Бар", callback_data='bar')],
                [InlineKeyboardButton("Обід", callback_data='lunch'), 
                 InlineKeyboardButton("Вечеря", callback_data='dinner')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Оберіть тип закладу: ', reply_markup=reply_markup)

    
def button(bot, update):
    query = update.callback_query
    type_of_place = query.data
    bot.edit_message_text(text="Ви обрали наступний тип закладу: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    params = dict(
        client_id='NLB5P2KIROZUMLVZMTZK4L5FRJ1WXPXNABP5FABPQBVWWI0D',
        client_secret='NO11HX0UNHRTHOYXBFG4SLOJQOIUCWD15XNNB51XBMCS54PV',
        v='20180401',
        ll=''+str(latitude)+ ',' +str(longitude),
        query=type_of_place,
        limit=3,
        )
    resp = requests.get(url=url, params=params)
    # data = json.loads(resp.text)
    # print  json.dumps(data, indent=4, sort_keys=True)
    data = resp.json()
    items = data["response"]["groups"][0]["items"]
    for item in items:
        reply_text = ""
        place_url = None
        place_hours = None
        place_phone = None
        place_name = item["venue"]["name"].encode("utf-8")
        place_address = item["venue"]["location"]["address"].encode("utf-8")
        reply_text += str(place_name) + '\n' + str(place_address) + '\n'
        
        if "isOpen" in item["venue"]["hours"]:
            place_hours = item["venue"]["hours"]["isOpen"]
            reply_text += '\nВідкрито зараз: '
            if place_hours == True:
                reply_text += 'Так'
            else:
                reply_text += 'Ні'

        if "formattedPhone" in  item["venue"]["contact"]:
            place_phone = item["venue"]["contact"]["formattedPhone"]
            reply_text += '\nНомер телефону: ' +str(place_phone)

        if "rating" in item["venue"]: 
            place_rating = item["venue"]["rating"]
            reply_text += '\nРейтинг: ' + str(place_rating) + '\n'
    
        if "url" in item["venue"]:
            place_url = item["venue"]["url"]
            reply_text += 'Сайт: ' + str(place_url)
            print place_url

        bot.send_message(text=reply_text, 
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        print "\n"
    


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler) 

    type_handler = CommandHandler('type', type)
    dp.add_handler(type_handler) 
    dp.add_handler(CallbackQueryHandler(button))

    typel_handler = MessageHandler(Filters.location, location)
    dp.add_handler(typel_handler) 
    dp.add_handler(CallbackQueryHandler(button))
    # location_handler = MessageHandler(Filters.location, location)
    # dp.add_handler(location_handler)

    #dp.add_handler(CallbackQueryHandler(button_location))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

