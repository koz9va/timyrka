import logging
import requests
from telegram.ext import Updater, CommandHandler

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )
updater = Updater('APIKEY')

updater.dispatcher.add_handler(CommandHandler('hello', hello))

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()