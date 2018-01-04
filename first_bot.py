#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import logging, json, requests

TOKEN = '429534900:AAFsqskQ7q6paCblWGN2NoB1JWX_lmCAL0Q'
url = 'https://api.foursquare.com/v2/venues/explore'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
	
	# bot.send_message(chat_id = update.message.chat_id, text="I'm a bot, please talk to me!")
	update.message.reply_text('Hi!')

def location(bot, update):
	user = update.message.from_user
	user_location = update.message.location
	logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
	longitude = user_location.longitude
	update.message.reply_text('Maybe I can visit you sometime! '
'At last, tell me something about yourself.')
	params = dict(
		client_id='NLB5P2KIROZUMLVZMTZK4L5FRJ1WXPXNABP5FABPQBVWWI0D',
		client_secret='NO11HX0UNHRTHOYXBFG4SLOJQOIUCWD15XNNB51XBMCS54PV',
		v='20180401',
		ll=''+str(user_location.latitude)+ ',' +str(user_location.longitude),
		query='coffee',
		#limit=5
		)
	resp = requests.get(url=url, params=params)
	# data = json.loads(resp.text)
	# print  json.dumps(data, indent=4, sort_keys=True)
	data = resp.json()
	items = data["response"]["groups"][0]["items"]
	for item in items:
		place_name = item["venue"]["name"].encode("utf-8")
		place_address = item["venue"]["location"]["address"].encode("utf-8")
		place_hours = item["venue"]["hours"]["status"]
		place_rating = item["venue"]["rating"]
		#place_url = item["venue"]["url"]
		print place_name, place_rating
		print place_address
		print place_hours
		#print place_url
		print "\n"

def type(bot, update): 
	keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Please choose: ', reply_markup=reply_markup)

def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
message_id=query.message.message_id)


def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher

	start_handler = CommandHandler('start', start)
	dp.add_handler(start_handler) 

	type_handler = CommandHandler('type', location)
	dp.add_handler(type_handler)
	dp.add_handler(CallbackQueryHandler(button))

	location_handler = MessageHandler(Filters.location, location)
	dp.add_handler(location_handler)
	#dp.add_handler(CallbackQueryHandler(button_location))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()

