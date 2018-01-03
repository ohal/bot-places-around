#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler
import logging

TOKEN = '429534900:AAFsqskQ7q6paCblWGN2NoB1JWX_lmCAL0Q'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
	bot.send_message(chat_id = update.message.chat_id, text="I'm a bot, please talk to me!")
	#update.message.reply_text('Hi!')

def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher

	start_handler = CommandHandler('start', start)
	dp.add_handler(start_handler) 

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()

